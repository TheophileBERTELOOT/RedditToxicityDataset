import praw
import json



with open("../../../config.json", "r") as jsonfile:
    config = json.load(jsonfile)

def cli():
    reddit = praw.Reddit(
    client_id=config['client_id'],
    client_secret=config['client_secret'],
    password=config['password'],
    user_agent="Comment Extraction (by u/USERNAME)",
    username=config['username'],
)

    subreddits = reddit.subreddits.popular()
    print(subreddits)
    for subereddit in subreddits:
        for collection in subereddit.collections:
            for submission in collection:
                print(submission.title)
                for comment in submission.comments:
                    print(comment.author,comment.parent_id,comment.body)
if __name__ == "__main__":
    cli()