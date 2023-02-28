# Telegram Parser

# Importing libraries
import configparser
import json
import pandas as pd

from datetime import datetime

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel



# Adding post date:
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading an attached config file with data
config = configparser.ConfigParser()
config.read("config.ini")

# Setting up the connection parameters (getting them from config.ini)
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']
password = config['Telegram']['password']


# Creating a channel - and connecting
client = TelegramClient(username, api_id, api_hash)

# Getting the list of channels to parse from a .xlsx file:
channels_excel = pd.read_excel('t_channels.xlsx')
channels_list = channels_excel['Channel Link'].tolist()
print('Loading Channels: ' + str(channels_list))

# Load the data from every channel:
curr_channel_id = 0

for channel in channels_list:
    user_input_channel = channel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    async def main(phone):
        await client.start()
        print("Client Created")

        # Authorizing with a pop-up:
        if await client.is_user_authorized() == False:
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=password)

        me = await client.get_me()

        my_channel = await client.get_entity(entity)

        offset_id = 0
        limit = 500                 # How many posts to load every cycle
        all_messages = []
        total_messages = 0
        total_count_limit = 2000     # How many posts to load (0 means 'everything')

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = await client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message.to_dict())
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        global curr_channel_id
        curr_channel_id +=1

        with open(mode = 'a', file='Messages/' + str(curr_channel_id) + '_telegram_messages.json') as outfile:
            json.dump(all_messages, outfile, cls=DateTimeEncoder)


    with client:
        client.loop.run_until_complete(main(phone))

print("Done!")
