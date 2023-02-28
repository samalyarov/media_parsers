# Importing libraries
import pandas as pd
import glob

# Determining the files for concatenating

data_posts = pd.concat(map(pd.read_json, glob.glob('Posts/*_posts.json')))
data_comments = pd.concat(map(pd.read_json, glob.glob('Posts/*_comments.json')))

# Getting 2 CSVs - with posts and comments
data_posts.to_csv('All_Data/All_Posts.csv')
data_comments.to_csv('All_Data/All_Comments.csv')
print("Done!")