from twilio.rest import Client
from os import getenv

class SMSMessager(object):
    def __init__(self, number_from, number_to):
        self.__number_from = number_from
        self.__number_to = number_to
        self.__client = Client(getenv('TWILIO_SID'), getenv('TWILIO_AUTH'))
    
    def message(self, message):
        self.__client.messages.create(
            body=message,
            from_=self.__number_from,
            to=self.__number_to
        )