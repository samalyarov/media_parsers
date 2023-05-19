# Importing libraries
import pandas as pd
import numpy as np
import re

# Importing data
all_users = pd.read_csv('all_users.csv')

# Setting up functions for editing
def str_to_dict(string, column):
    '''
    Create a dict out of a string shaped like one
    '''
    # remove the curly braces from the string
    string = string.strip('{}')
 
    # split the string into key-value pairs
    pairs = string.split(', ')
 
    # use a dictionary comprehension to create the dictionary, converting the values to integers and removing the quotes from the keys
    curr_dict = {key[1:-1]: value for key, value in (pair.split(': ') for pair in pairs)}
    
    return curr_dict[column]

def clarify_hometown(string):
    '''
    Get a proper hometown name out of the text
    '''
    
    string = string.replace('users_lists', '')
    string = string.replace('\\','')
    string = string.replace ('_users.json', '')
    
    return string

def clarify_current_city(string):
    '''
    Get a proper current city name (remove the ' sign)
    '''
    string = re.sub('[^a-zA-Z]+', '', string)
    return string

# Create a column with proper city IDs
all_users['city_id'] = all_users['city'].map(lambda x: str_to_dict(x, 'id') if type(x) == str else np.nan)

# Create a column with proper city names
all_users['city_name'] = all_users['city'].map(lambda x: str_to_dict(x, 'title') if type(x) == str else np.nan)
all_users['city_name'] = all_users['city_name'].map(lambda x: clarify_current_city(x) if type(x) == str else np.nan)

# Create a column with readable last_seen timestamp (no unix time)
all_users['last_seen_datetime'] = all_users['last_seen'].map(lambda x: str_to_dict(x, 'time') if type(x) == str else np.nan)
all_users['last_seen_datetime'] = pd.to_datetime(all_users['last_seen_datetime'], errors='ignore', unit='s')

# Fix the column with 'hometown' value that was used to find the user
all_users['search_hometown'] = all_users['search_hometown'].map(lambda x: clarify_hometown(x) if type(x) == str else np.nan)

# Delete unnecessary columns
all_users.drop(columns=['city','last_seen', 'track_code','Unnamed: 0', 'can_access_closed', 'is_closed'], inplace=True)

# Get a list of cities (same as in parser):
monitor_cities = {"city_1":111,
                  "city_2":222
                  }

# Filter by ID
all_users_filtered = all_users[~all_users['city_id'].isin(monitor_cities.values())]

# Filter by city name
all_users_filtered = all_users[~all_users['city_name'].isin(monitor_cities.keys())]

# Save the resulting dataframe as a separate file:
all_users_filtered.to_csv('all_users_filtered.csv')