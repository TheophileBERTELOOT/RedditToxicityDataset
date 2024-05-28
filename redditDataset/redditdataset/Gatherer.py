import praw
import typing 

from Types.Authors import Author
from Types.Comments import Comments
from Types.Subreddits import Subreddits

from Enums.SubredditGathering import SubredditGathering
from Enums.SubmissionsGathering import SubmissionGathering

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
            
    
    def fetchComments(self, submission:praw.models.Submission):
        comments = submission.comments
        comments.replace_more(limit=None)
        return comments.list()
            
    def extractAuthorInfos(self,author:praw.models.Redditor):
        authorObject = Author(author)
        if authorObject.id not in self.extractedAuthorsIds:
            self.extractedAuthorsIds.append(authorObject.id)
            self.extractedAuthors.append(authorObject)
            
    def extractCommentsInfos(self,comments:typing.Iterator[praw.models.Comment]):
        for comment in comments:
            self.extractedComments.append(Comments(comment))
            
    def extractSubredditInfo(self,subreddit:praw.models.Subreddit):
        self.subreddit = Subreddits(subreddit)
                
        