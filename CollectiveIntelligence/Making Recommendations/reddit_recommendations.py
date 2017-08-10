import praw
import os

client_id = os.environ.get('reddit_client_id')
client_secret= os.environ.get('reddit_client_key')

password = os.environ.get('reddit_password')
username = os.environ.get('reddit_username')


reddit = praw.Reddit(client_id=client_id,
                    client_secret=client_secret,
                    password=password,
                    user_agent='reddit_recommender/v1',
                    username=username)


print(reddit.user.me())

items = []
for i in reddit.subreddit('google').hot():
    print(i.author)
    print(type(i.author.name))
    items.append(i)


print(', '.join(dir(items[0])))
print(', '.join(dir(items[0].author)))

