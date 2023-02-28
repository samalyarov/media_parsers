# Importing libraries

from numpy import number
import vk
import pandas as pd
import time
import json
import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

### Getting the followers stats:

# Enter the API data:
session = vk.Session(access_token='SAMPLE_TOKEN_CHANGE')
vkapi = vk.API(session)

# Get a list of groups to load:
groups_excel = pd.read_excel('vk_groups.xlsx')
groups_list = groups_excel['Channel ID'].tolist()
groups_names = groups_excel['Group name'].tolist()


groups_followers = []
followers_accessable = []
limit = 1000 # How many followers to load at once (current VK limit is 1000)

### Getting the stats on followers from open groups:
for i in range(len(groups_list)):
    try:
        number_of_followers = vkapi.groups.getMembers(group_id=groups_list[i], offset=0, v=5.131)['count']
        print(f'В группе "{groups_names[i]}" подписчиков: {number_of_followers}')
        followers_accessable.append([groups_list[i], number_of_followers])
        time.sleep(0.2)

    except:
        print(f'Группа {groups_names[i]} скрывает пользователей.')
    
# Concat and get the number of total unique users:

all_followers = []
print("Приступаем к выгрузке пользователей...")
for i in range(len(followers_accessable)):
    curr_group_followers = []
    for off in range(0, followers_accessable[i][1]+1, limit):
        followers = vkapi.groups.getMembers(group_id=followers_accessable[i][0], count=limit, offset=off, v=5.131)
        followers = followers['items']
        for k in followers:
            curr_group_followers.append(k)
        time.sleep(0.2)
    all_followers.append(curr_group_followers)
    
with open(mode = 'a', file='Followers/All_Followers.json') as outfile:
    json.dump(all_followers, outfile, cls=DateTimeEncoder)

print("Готово!")