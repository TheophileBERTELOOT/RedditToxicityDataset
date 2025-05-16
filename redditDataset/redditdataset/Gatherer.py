import praw
import typing 
from datetime import datetime, timedelta,timezone

from redditDataset.redditdataset.Types.Authors import Author
from redditDataset.redditdataset.Types.Comments import Comments
from redditDataset.redditdataset.Types.Subreddits import Subreddits

from redditDataset.redditdataset.Enums.SubredditGathering import SubredditGathering
from redditDataset.redditdataset.Enums.SubmissionsGathering import SubmissionGathering
import time

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
        self.filteredComments = []
        self.subreddit = None
        
        
    def resetBuffers(self):
        self.extractedAuthors = []
        self.extractedAuthorsIds = []
        self.extractedComments = []
        self.filteredComments = []
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
    
    def fetchCommentsLastXMinutes(self, submission:praw.models.Submission,nbLimit:int|None=None,timeDelta:int=10):
        now = datetime.now(timezone.utc)
        time_threshold = now - timedelta(minutes=timeDelta )
        time_threshold_timestamp = int(time_threshold.timestamp())
        self.filteredComments = []
        print(submission.title)
        try :
            submission.comment_sort = 'new'
            comments = submission.comments
            comments.replace_more(limit=1)
            for comment in comments.list():

                time.sleep(0.1)
                if comment.created_utc >= time_threshold_timestamp:
                    self.filteredComments.append(comment)
            print('number of comments extracted :')
            print(len(self.filteredComments))
        except Exception as error :
            print(error)

        return self.filteredComments
            
    def extractAuthorInfos(self,author:praw.models.Redditor):
        authorObject = Author(author)
        if authorObject.id not in self.extractedAuthorsIds:
            self.extractedAuthorsIds.append(authorObject.id)
            self.extractedAuthors.append(authorObject)
            
    def extractCommentsInfos(self,comments:typing.Iterator[praw.models.Comment]):
        for comment in comments:
            try:
                
                print(comment.body)
                print('-------------------')
                self.extractedComments.append(Comments(comment))
                self.extractAuthorInfos(comment.author)
            except Exception as error :
                print(error)
                
            
    def extractSubredditInfo(self,subreddit:praw.models.Subreddit):
        self.subreddit = Subreddits(subreddit)

    def getCommentById(self,id:str):
        return self.reddit.comment(id=id)
        
                
        