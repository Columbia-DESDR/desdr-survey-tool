import re
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import datetime
from dateutil.relativedelta import relativedelta

# IRI Account
# Your Account SID from twilio.com/console
account_sid = "Dummy"
# Your Auth Token from twilio.com/console
auth_token = "Dummy"
client = Client(account_sid, auth_token)


def extract_number(body):
    number = ""
    digits = re.findall("\d+", body)
    for d in digits:
        number += d
    if number:
        return int(number)


def send_message(message, to_number, from_number):
    try:
        # This could potentially throw an exception!
        message = client.messages.create(
            to=to_number,
            from_=from_number,
            body=message)
    except TwilioRestException as e:
        # Implement your fallback code
        print(e)
        print("Error from Message")


def get_next_date_from_delay(value):
    next_date = datetime.date.today()
    if 'months' in value:
        months = value[:-7]
        next_date = next_date + relativedelta(months=int(months))
    if 'days' in value:
        days = value[:-5]
        next_date = next_date + relativedelta(days=int(days))
    if 'years' in value:
        years = value[:-6]
        next_date = next_date + relativedelta(years=int(years))
    next_date = next_date.strftime('%Y-%m-%d')
    return next_date
