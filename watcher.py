from timer import RepeatedTimer
from datetime import datetime
from requests import get

class DowntimeInfo(object):
    def __init__(self, error_code):
        self.down_start = datetime.now()
        self.notifications = 0
        self.error_code = error_code

class URLWatcher(object):
    """Watcher object that oversees monitoring of a URL
    """

    def __init__(self, messager, check_interval=60, notify_interval=86400):
        """
        Arguments:
            messender {[SMSMessenger]} -- Twilio messenger used to send SMS notifications
        
        Keyword Arguments:
            check_interval {int} -- number of seconds between HTTP requests (default: {60})
            notify_interval {int} -- number of seconds between notifications (default: {86400})
        """
        self.__messager = messager
        self.__timer = RepeatedTimer(check_interval, self.__check)
        self.downtime_info = None
        self.__notify_interval = notify_interval
    
    def watch(self, url):
        """Starts periodic checking on this URL. Replaces any previous URL.
        
        Arguments:
            url {[str]} -- new URL to watch
        """
        self.__url = url
        self.downtime_info = None
        self.__timer.start()

    def __check(self):
        """Check if the watched URL is down by checking the status code.

        If it's anything other than 200, the website is considered "down".
        """
        response = get(self.__url)
        if response.status_code == 200:
            if self.downtime_info:
                self.__notify_up()
            self.downtime_info = None
        else:
            if not self.downtime_info:
                self.downtime_info = DowntimeInfo(response.status_code)
            seconds = (datetime.now() - self.downtime_info.down_start).total_seconds()
            if seconds // self.__notify_interval >= self.downtime_info.notifications:
                self.__notify_down()
                
    
    def __notify_down(self):
        if self.downtime_info:
            if not self.downtime_info.notifications:
                self.__messager.message('Downtime Notification:\n\n{} just went down! Error code: {}'.format(
                    self.__url,
                    self.downtime_info.error_code
                ))
            else:
                self.__messager.message('Downtime Notification:\n\n{} is still down. It has been down since {}.'.format(
                    self.__url,
                    self.downtime_info.down_start.strftime(
                        '%A %b {}, %Y at {}:%M%p UTC'
                    ).format(6, datetime.now().hour%12)
                ))
            self.downtime_info.notifications += 1
        else:
            raise Exception('No downtime information!')
    
    def __notify_up(self):
        self.__messager.message('Downtime Notification:\n\n{} is back up and running!'.format(
            self.__url
        ))