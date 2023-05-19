# User.search method documentation - https://vk.com/dev/users.search

# Importing libraries
import vk
import pandas as pd
import json
import time

# Setting up the connection data
session = vk.Session(access_token='insert_your_access_token_here')
vkapi = vk.API(session)


# Listing the cities of interest and their IDs
monitor_cities = {"city_1":111,
                  "city_2":222
                  }

# Setting up the parsing parameters
max_user_count = 1000 # How many users to load each cycle. Current VK API limit is 1000.
waiting_time = 1 # Wait time betweeen queries (VK API limits)

# Creating a list of users of interest and a counter for them
users_of_interest = []
total_users = 0
filtered_total_users = 0

# Iterate for each city in a list
for hometown in monitor_cities.keys():
    user_count = vkapi.users.search(hometown=hometown, v=5.131)['count']
    filtered_user_count = vkapi.users.search(hometown=hometown, age_from=20, age_to=25, v=5.131)['count']

    print(f'Total number of users with hometown set to {hometown} is {user_count}')
    print(f'Total number of users in selected age group {filtered_user_count}')
    total_users += user_count
    filtered_total_users += filtered_user_count

    # Getting the users:
    for off in range(0, user_count + 1, max_user_count):
        print("Loading users beginning with user #{}".format(off))
        current_users = vkapi.users.search(offset=off, # Current offset
                                           count=max_user_count, # How many users to return each cycle
                                           fields=['city', 'last_seen', 'home_town'], # What extra data to return
                                           age_from=15,
                                           age_to=25,
                                           hometown=hometown,
                                           v=5.131
                                           )['items'] # Working with the user list
        
        # Adding the users to a list
        for user in current_users:
                users_of_interest.append(user)
        
        time.sleep(waiting_time)  # Avoiding request limits

    # Dumpint the data for each town into a separate JSON
    with open(mode = 'a', file=f'users_lists/{hometown}_users.json') as outfile:
        json.dump(users_of_interest, outfile)

# Final info on script completion
print('Loading complete!')
print(f'Total number of users with hometowns from the list: {total_users}')
print(f'Total number of users in selected age group: {filtered_total_users}')
        


