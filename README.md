# downtime-alerter
SMS notification service that watches a URL and notifies during downtime

## Requirements

![language](https://img.shields.io/badge/python-3.6-yellow.svg?cacheSeconds=2592000)

This application uses the Twilio API to send SMS messages. It requires an SID, auth token, and phone number, all stored within environment variables as `TWILIO_SID`, `TWILIO_AUTH`, and `TWILIO_NUM` respectively. Learn more about how to get started with Twilio [here](https://www.twilio.com/docs/usage/api#working-with-twilios-apis)

All `python` dependency packages are outlined [here](requirements.txt)

## Usage
`downtime_alerter.py url phone#`

Running `downtime_alerter.py` starts the service by creating a `URLWatcher` and making it watch the given `url`. It will make periodic `GET` requests to the URL, and if the response is anything other than a `200`, an SMS is sent to `phone#` using the Twilio API

By default, a `URLWatcher` will check every `60` seconds on the health of the URL, and notify again every `86400` seconds (1 day) that it's down