import json

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
    subreddits = gatherer.fetchSubreddits(SubredditGathering.Popular, nbLimit=10)
    for subreddit in subreddits:
        gatherer.extractSubredditInfo(subreddit)
        submissions = gatherer.fetchSubmissions(subreddit,SubmissionGathering.Hot, nbLimit=10)
        for submission in submissions:
            gatherer.extractAuthorInfos(submission.author)
            comments = gatherer.fetchCommentsLastXMinutes(submission)
            gatherer.extractCommentsInfos(comments)
        mongo.exportAuthorsInfos(gatherer.extractedAuthors)
        mongo.exportCommentsInfos(gatherer.extractedComments)
        mongo.exportSubredditInfos(gatherer.subreddit)
        gatherer.resetBuffers()
    mongo.sampleComments()
    mongo.sampleAuthors()
    mongo.sampleSubreddits()
    # mongo.removeEverythingFromEveryCollection()


if __name__ == "__main__":
    cli()