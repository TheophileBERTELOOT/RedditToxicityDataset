import praw
import typing 
from datetime import datetime, timedelta

from redditDataset.redditdataset.Types.Authors import Author
from redditDataset.redditdataset.Types.Comments import Comments
from redditDataset.redditdataset.Types.Subreddits import Subreddits

from redditDataset.redditdataset.Enums.SubredditGathering import SubredditGathering
from redditDataset.redditdataset.Enums.SubmissionsGathering import SubmissionGathering

class Gatherer:
    def __init__(self,config):
        self.reddit = praw.Reddit(
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        password=config['password'],
        user_agent="Comment Extraction (by u/Lobarten and u/DrMygalon)",
        username=config['username'],
    )
        self.extractedAuthors = []
        self.extractedAuthorsIds = []
        self.extractedComments = []
        self.subreddit = None
        
        
    def resetBuffers(self):
        self.extractedAuthors = []
        self.extractedAuthorsIds = []
        self.extractedComments = []
        self.subreddit = None
        

    def fetchSubreddits(self,gatheringType:SubredditGathering,searchQuery:str='',nbLimit:int=None) -> typing.Iterator[praw.models.Subreddit]|bool:
        match gatheringType:
            case SubredditGathering.Popular:
                return self.reddit.subreddits.popular(limit=nbLimit)
            case SubredditGathering.Search:
                return self.reddit.subreddits.search(searchQuery,limit=nbLimit)
            case _:
                print('unknown subreddits gathering type')
                return False
    
    def fetchSubmissions(self,subreddit:praw.models.Subreddit,gatheringType:SubmissionGathering,nbLimit:int=None):
        match gatheringType:
            case SubmissionGathering.Hot:
                return subreddit.hot(limit=nbLimit)
            case SubmissionGathering.Controversial:
                return subreddit.controversial(limit=nbLimit)
            case SubmissionGathering.New:
                return subreddit.new(limit=nbLimit)
            case SubmissionGathering.Random:
                return subreddit.random(limit=nbLimit)
            case SubmissionGathering.Rising:
                return subreddit.rising(limit=nbLimit)
            case SubmissionGathering.Sticky:
                return subreddit.sticky(limit=nbLimit)
            case SubmissionGathering.Top:
                return subreddit.top(limit=nbLimit)
            case _:
                print('unknown submission gathering type')
                return False
            
    
    def fetchComments(self, submission:praw.models.Submission,nbLimit:int|None=None):
        comments = submission.comments
        comments.replace_more(limit=None)
        return comments.list()
    
    def fetchCommentsLastXMinutes(self, submission:praw.models.Submission,nbLimit:int|None=None,timeDelta:int=1000):
        now = datetime.utcnow()
        time_threshold = now - timedelta(minutes=timeDelta)
        time_threshold_timestamp = int(time_threshold.timestamp())
        filteredComments = []
        comments = submission.comments
        comments.replace_more(limit=5)
        for comment in comments.list():
             if comment.created_utc >= time_threshold_timestamp:
                 filteredComments.append(comment)
        return filteredComments
            
    def extractAuthorInfos(self,author:praw.models.Redditor):
        authorObject = Author(author)
        if authorObject.id not in self.extractedAuthorsIds:
            self.extractedAuthorsIds.append(authorObject.id)
            self.extractedAuthors.append(authorObject)
            
    def extractCommentsInfos(self,comments:typing.Iterator[praw.models.Comment]):
        for comment in comments:
            print(comment.body)
            print('-------------------')
            self.extractedComments.append(Comments(comment))
            self.extractAuthorInfos(comment.author)
            
    def extractSubredditInfo(self,subreddit:praw.models.Subreddit):
        self.subreddit = Subreddits(subreddit)
        
                
        