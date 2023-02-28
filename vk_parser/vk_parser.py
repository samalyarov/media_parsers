# wall.get method documentation: https://dev.vk.com/method/wall.get%D0%BF

# Importing libraries:
import vk
import pandas as pd
import json
from datetime import datetime
import time

# Waiting time needs to be inserted between queries due to VK limitations. The size can be changed as the limits change. 
# There is no limit on paid version 

# Constants:
LOAD_ALL_POSTS = 0 # If set to '1' then loads all posts from each group disregarding the following group setup. Can be impractical.
WAITING_TIME = 0.3 # Waiting time needs to be inserted between queries due to VK limitations. The size can be changed as the limits change. 
FINAL_DATE = '2021-09-01 00:00:00' # Posts up to which date are to be loaded. (Format: YYYY-MM-DD HH-MM-SS)
final_date = datetime.strptime(FINAL_DATE, '%Y-%m-%d %H:%M:%S')

# Adding post date into post data:
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

# Enter the API data:
session = vk.Session(access_token='SAMPLE_TOKEN_CHANGE')
vkapi = vk.API(session)

# Get a list of groups to load:
groups_excel = pd.read_excel('vk_groups.xlsx')
groups_list = groups_excel['Channel ID'].tolist()
groups_names = groups_excel['Group name'].tolist()
print('Loading Groups: ' + str(groups_names))

limit = 100 # Current VK limit on loading if using free clients. May change in the future.

# Separate function for parsing comments
def parse_comments(owner_id, post_id, comment_count):
    count = 0
    for comm_off in range(0, comment_count + 1, limit):

        comments = vkapi.wall.getComments(owner_id=owner_id, post_id=post_id, count=limit, offset=comm_off,v=5.131)
        comments = comments['items']

        for comment in comments:
            all_comments.append(comment)
            if comment:
                count += 1
                    
        time.sleep(WAITING_TIME)  # Added to avoid request limits
    return count

# Loading the posts from each group in the list:
for group in groups_list:
    print(f'Currently loading posts from group: {group}')
    number_of_posts = vkapi.wall.get(owner_id=-group, count=1, offset=1, v=5.131)['count']  # How many posts total
    all_posts = []
    all_comments = []
    print(f'Всего постов в группе: {number_of_posts}')

    # Saving the posts
    post_count = 0
    for off in range(0, number_of_posts + 1, limit):
        print("Скачиваем посты начиная с поста №{}".format(off))
        wall_posts = vkapi.wall.get(owner_id=-group, count=limit, offset=off, v=5.131)
        wall_posts = wall_posts['items']  # data[0] is total number of posts in the community

        for post in wall_posts:
            all_posts.append(post)

            if post["text"]:
                # Removing <br> tag, which appeared in some posts
                post_count += 1
                comment_count = vkapi.wall.getComments(owner_id=-group, post_id=post['id'], count=1, offset=1, v=5.131)['count']
                if comment_count > 0:
                    comm_count = parse_comments(owner_id=-group, post_id=post['id'], comment_count=comment_count)
                    post_count += comm_count
            time.sleep(WAITING_TIME)    
            
        # If the last post is dated earlier than pre-set 'last_date' - break the cycle
        if LOAD_ALL_POSTS == 1:
            last_post_date = wall_posts[-1]['date']
            last_post_date_dt = datetime.fromtimestamp(last_post_date)
            if last_post_date_dt < final_date:
                print("Загружены все посты до указанной даты")
                break
            


    with open(mode = 'a', file='Posts/' + str(group) + '_vk_posts.json') as outfile:
            json.dump(all_posts, outfile, cls=DateTimeEncoder)

    with open(mode = 'a', file='Posts/' + str(group) + '_vk_comments.json') as outfile:
        json.dump(all_comments, outfile, cls=DateTimeEncoder)
