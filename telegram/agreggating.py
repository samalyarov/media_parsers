#Importing libraries
import pandas as pd
import glob
from pandas import concat, json_normalize

# Concatenating the files into a single dataframe

df = pd.concat(map(pd.read_json, glob.glob('Messages/*.json')))

header = df.head(10)

print(header)

# Exporting the resulting dataframe into a .csv file for further analysis:
df.to_csv('Messages/Aggregated Data.csv')
print("Done!")

