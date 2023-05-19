# The aggregating script is actually like 50% chatGPT's work :)

# Importing libraries
import pandas as pd
import glob

# Get a list of .jsons to concatenate
items = glob.glob('users_lists/*.json')

# Create an empty list for concatenating dataframes:
dfs = []

# Iterate through all the files in target directory
for filename in items:
        df = pd.read_json(filename)
        # Add a column indicating the source file
        df['search_hometown'] = filename
        # Append the DataFrame to the list
        dfs.append(df)
        
# Concatenate all the DataFrames into a single DataFrame
concatenated_df = pd.concat(dfs)

# Save the resulting dataframe into a .csv file
concatenated_df.to_csv('all_users.csv')