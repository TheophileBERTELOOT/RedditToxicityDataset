import json

from Enums.CollectionsNames import CollectionNames
from Enums.SubmissionsGathering import SubmissionGathering
from Enums.SubredditGathering import SubredditGathering
from Gatherer import Gatherer
from MongoHandler import MongoHandler

# FIXME : better with environment variables and not a json file.
# with open("/home/lbaret/projects/RedditToxicityDataset/redditDataset/redditdataset/config.json", "r") as jsonfile:
#     config = json.load(jsonfile)
    
with open("../../../config.json", "r") as jsonfile:
    config = json.load(jsonfile)

mongo = MongoHandler(verbose=True)

def cli():
    gatherer = Gatherer(config)
    subreddits = gatherer.fetchSubreddits(SubredditGathering.Popular, nbLimit=1)
    for subreddit in subreddits:
        gatherer.extractSubredditInfo(subreddit)
        submissions = gatherer.fetchSubmissions(subreddit,SubmissionGathering.Hot, nbLimit=2)
        for submission in submissions:
            gatherer.extractAuthorInfos(submission.author)
            comments = gatherer.fetchComments(submission)
            gatherer.extractCommentsInfos(comments)
        mongo.exportAuthorsInfos(gatherer.extractedAuthors)
        mongo.exportCommentsInfos(gatherer.extractedComments)
        mongo.exportSubredditInfos(gatherer.subreddit)
        gatherer.resetBuffers()
    mongo.sampleComments()
    mongo.sampleAuthors()
    mongo.sampleSubreddits()
    mongo.removeEverythingFromEveryCollection()


if __name__ == "__main__":
    cli()