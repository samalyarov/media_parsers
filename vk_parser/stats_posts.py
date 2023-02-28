print("Начинаем сбор данных")

# Importing libraries

import vk
import pandas as pd
import time
import datetime

# Get overall stats - how many posts to load:

# Enter the API data:
session = vk.Session(access_token='SAMPLE_TOKEN_CHANGE')
vkapi = vk.API(session)

# Get a list of groups to load:
groups_excel = pd.read_excel('vk_groups.xlsx')
groups_list = groups_excel['Channel ID'].tolist()
groups_names = groups_excel['Group name'].tolist()

print('Acquiring stats for groups:: ' + str(groups_names))

total_posts = 0
for i in range(len(groups_list)):
    number_of_posts = vkapi.wall.get(owner_id=-groups_list[i], count=1, offset=1, v=5.131)['count']
    total_posts += number_of_posts
    print(f'В группе "{groups_names[i]}" постов для скачивания: {number_of_posts}')
    time.sleep(0.2)

print(f'Всего постов для скачивания в предоставленном списке: {total_posts}')
loading_time = (total_posts/100) * 30
loading_time_proper = datetime.timedelta(seconds=loading_time)
print(f'Примерное время скачивания: {str(loading_time_proper)}')
