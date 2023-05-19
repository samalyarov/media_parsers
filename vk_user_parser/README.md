# Basic VK user parsing script 

A script is based on vk API (currently free for use) and parses users with the use of `user.search` method based on select criteria. Within the given example the criteria is the user's hometown and age (the processing script return a dataframe with people that currently live in cities other then ones in the list of hometowns) as the research interest lies in contacting people that moved away from a particular region. Data is thus aggregated into .csv file for ease of analysis and forwarding.

Files included in repository:

- `user_parser.py` is a parser script itself. Performs the parsing of VK users based on search criteria (exact documentation and potential criteria can be found here - https://vk.com/dev/users.search) and saves the data collected for each hometown into a separate .json file.
- `aggregator.py` is an aggregating script that takes these .json files and concatenates them into a single .csv file for ease of analysis and forwarding. Technically, since the saving itself is done via the pandas library it can be easily changed to save into a number of other formats supported by pandas library as well.
- `pre_editing.py` is a script that pre-processes the data for further use by removing unnecessary columns and editing data within others. The result is a separate .csv file.

*Libraries used: vk, pandas, numpy, json, glob, re, time*
