import os
import sys
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()
VK_API_VERSION = 5.92
VK_API_URL = 'https://api.vk.com/method/'
VK_API_METHODS = {'users_get': 'users.get'}
VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
VK_STATUS = 'online'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'access_token': VK_ACCESS_TOKEN,
        'v': VK_API_VERSION,
        'fields': VK_STATUS
    }
    try:
        user_status_request = requests.post(
            f'{VK_API_URL}{VK_API_METHODS["users_get"]}',
            params=params
        ).json()
    except requests.RequestException:
        raise sys.exit()
    return user_status_request['response'][0][VK_STATUS]


def send_sms(sms_text):
    message = client.messages.create(
        to=NUMBER_TO,
        from_=NUMBER_FROM,
        body=sms_text,
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id: ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
