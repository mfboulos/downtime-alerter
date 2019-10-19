from watcher import URLWatcher
from messager import SMSMessager

from os import environ
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Missing required command line argument.\n')
        print('Usage: downtime_alerter.py url phone#')
        sys.exit(0)
    urlwatcher = URLWatcher(SMSMessager(environ['TWILIO_NUM'], sys.argv[2]))
    urlwatcher.watch(sys.argv[1])