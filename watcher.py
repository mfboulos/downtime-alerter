from timer import RepeatedTimer
from datetime import datetime
from urllib.request import urlopen

class DowntimeInfo(object):
    def __init__(self, down_code):
        self.down_start = datetime.now()
        self.notifications = 0
        self.error_code = error_code

class URLWatcher(object):
    """Watcher object that oversees monitoring of a URL
    """

    def __init__(self, url, messager, check_interval=60, notify_interval=86400):
        """URL and intervals for watching and notification
        
        Arguments:
            url {[str]} -- url to watch
        
        Keyword Arguments:
            check_interval {int} -- number of seconds between HTTP requests (default: {60})
            notify_interval {int} -- number of seconds between notifications (default: {86400})
        """
        self.__url = url
        self.__messager = messager
        self.__timer = RepeatedTimer(check_interval, self.__check)
        self.downtime_info = None
        self.__notify_interval = notify_interval
    
    def watch(self, url):
        """Replaces the URL currently being watched with the new URL
        
        Arguments:
            url {[str]} -- new URL to watch
        """
        self.__url = url
        self.downtime_info = None

    def __check(self):
        """Check if the watched URL is down by checking the status code.

        If it's anything other than 200, the website is considered "down".
        """
        response = urlopen(self.__url)
        if response.getcode() == 200:
            if self.downtime_info:
                self.__notify_up()
            self.downtime_info = None
        else:
            if not self.downtime_info:
                self.downtime_info = DowntimeInfo(response.getcode())
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
                self.__messager.message('Downtime Notification:\n\n{} has been down since {}.'.format(
                    self.__url,
                    str(self.downtime_info.down_start)
                ))
                self.downtime_info.notifications += 1
        else:
            raise Exception('No downtime information!')
    
    def __notify_up(self):
        self.__messager.message('Downtime Notification:\n\n{} is back up and running!'.format(
            self.__url
        ))