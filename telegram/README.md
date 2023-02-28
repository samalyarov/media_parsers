# Basic Telegram parsing script 

A script is based on telethon library and utilizes a personal Telegram account for acquiring messages from open channels or channel to which the user has access. Data can be collected from multiple channels (from a list in separate files) and transformed into a single .csv file. 

Files included in repository:

- `t_channels.xlsx` is a list of channels (with names and links) from which the posts are to be loaded. The list is done in a .xlsx file for ease of communicating with colleagues and leaving comments and remarks.
- `config.ini` is a config file listing username, password, phone number of a user as well as bot API settings for connection. 
- `telegram_parser.py` is a parser script itself
- `aggregating.py` is an aggregator script. After the messages have been loaded in merges them into a single .csv file for further analysis or forwarding.
