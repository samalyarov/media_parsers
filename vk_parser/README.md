# Basic VK parsing script 

A script is based on vk API (currently free for use) and utilizes and loads posts and comments from a select list of groups|channels|profiles. Data can then be aggregated into .csv files for ease of analysis and forwarding.

Files included in repository:

- `vk_groups.xlsx` is a list of groups (with names) from which the posts are to be loaded. The list is done in a .xlsx file for ease of communicating with colleagues and leaving comments and remarks. The list also features several parameters that are used in further analytics (dividing groups by their type, locality etc.)
- `id_acquisition.py` is a script for acquirint the channel IDs (needed for interaction with VK API) using an external website and selenium webdriver. Channel links need to be provided for it.
- `stats_followers.py` is a script for analysing the total number of unique followers in total groups. Not always useful due to some VK groups making their follower list private but can provide an insight into a size of target audience.
- `stats_posts.py` is a script for preliminary analysis - how many posts are to be loaded within groups provided. Useful for asessing how much time will be necessary.
- `vk_parser.py` is a parser script itself. It loads posts up to a select date from a list of channel IDs provided in a separate file. Can load all posts from given groups or only posts up to a certain date.
- `aggregating.py` is an aggregator script. After the posts and comments have been loaded - it merges them into a two .csv files for further analysis or forwarding.
