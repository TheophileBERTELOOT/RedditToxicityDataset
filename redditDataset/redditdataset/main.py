import json

import praw

# FIXME : better with environment variables and not a json file.
with open("/home/lbaret/projects/RedditToxicityDataset/redditDataset/redditdataset/config.json", "r") as jsonfile:
    config = json.load(jsonfile)
    
# with open("../../../config.json", "r") as jsonfile:
#     config = json.load(jsonfile)

def cli():
    reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        password=config['password'],
        user_agent="Comment Extraction (by u/Lobarten and u/DrMygalon)",
        username=config['username'],
    )

    subreddits = reddit.subreddits.popular()
    for subreddit in subreddits:
        print(f"From : {subreddit.title}")
        for comment in subreddit.comments(limit=5):
            print(comment.author)
        
        print(f"End for : {subreddit.title}\n")

if __name__ == "__main__":
    cli()