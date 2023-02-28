# Function for checking which posts from the list have been loaded
# and which have been skipped during manual check-up

import pandas as pd
import os
import re

#Determining the already-loaded files and getting a list of loaded IDs

file_names = os.listdir('Posts/')
names_only = []

for file in file_names:
    file = re.sub('_vk_posts.json', '', file)
    file = re.sub('_vk_comments.json', '', file)
    file=int(file)
    names_only.append(file)
names_only = list(set(names_only))

#Getting the list of supposed loaded files:

groups_excel = pd.read_excel('vk_groups_full.xlsx')
groups_ids = groups_excel['Channel ID'].astype(int).tolist()

#Creating a list with groups to load:
print(f'Всего групп в списке: {len(groups_ids)}')
print(f'Уже скачано групп: {len(names_only)}')

groups_to_load = [elem for elem in groups_ids if elem not in names_only]

print(f'Скачать осталось {len(groups_to_load)} групп')

#Exporting the list to excel for further loading:
df = pd.DataFrame(groups_to_load)
writer = pd.ExcelWriter(path='groups_to_load.xlsx', engine='xlsxwriter')
df.to_excel(writer)
writer.close()

print('Done!')