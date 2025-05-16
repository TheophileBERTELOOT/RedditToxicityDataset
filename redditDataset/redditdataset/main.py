import json
import time

from redditDataset.redditdataset.Enums.CollectionsNames import CollectionNames
from redditDataset.redditdataset.Enums.SubmissionsGathering import SubmissionGathering
from redditDataset.redditdataset.Enums.SubredditGathering import SubredditGathering
from redditDataset.redditdataset.Gatherer import Gatherer
from redditDataset.redditdataset.MongoHandler import MongoHandler

# FIXME : better with environment variables and not a json file.
# with open("/home/lbaret/projects/RedditToxicityDataset/redditDataset/redditdataset/config.json", "r") as jsonfile:
#     config = json.load(jsonfile)
    
with open("../config.json", "r") as jsonfile:
    config = json.load(jsonfile)

mongo = MongoHandler(verbose=True)

def cli():
    gatherer = Gatherer(config)
    subreddits = gatherer.fetchSubreddits(SubredditGathering.Popular, nbLimit=20)
    for subreddit in subreddits:
        print('new subreddit : ' + subreddit.display_name)
        gatherer.extractSubredditInfo(subreddit)
        submissions = gatherer.fetchSubmissions(subreddit,SubmissionGathering.Hot, nbLimit=5)
        for submission in submissions:
            #gatherer.extractAuthorInfos(submission.author)
            comments = gatherer.fetchCommentsLastXMinutes(submission)
            gatherer.extractCommentsInfos(comments)
            time.sleep(1)
        mongo.exportSubredditInfos(gatherer.subreddit)
        mongo.exportCommentsInfos(gatherer.extractedComments)
        mongo.exportAuthorsInfos(gatherer.extractedAuthors)
        time.sleep(1)
        

        gatherer.resetBuffers()

    #mongo.sampleComments()
    #mongo.sampleAuthors()
    #mongo.sampleSubreddits()
    # mongo.removeEverythingFromEveryCollection()


if __name__ == "__main__":
    cli()