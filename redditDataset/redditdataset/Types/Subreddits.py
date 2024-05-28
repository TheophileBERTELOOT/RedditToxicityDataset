import praw

class Subreddits:
    def __init__(self,subreddit:praw.models.Subreddit):
        self.subreddit:praw.models.subreddit = subreddit
        self.fillInfos()
        
    def fillInfos(self):
        self.id:str = self.subreddit.id
        self.over18:bool = self.subreddit.over18
        self.name:str = self.subreddit.name
        self.createdTime:str = self.subreddit.created_utc
        self.subscribers:int=self.subreddit.subscribers


    def getDict(self):
        return {'id':self.id,
                'over18':self.over18,
                'name':self.name,
                'createdTime':self.createdTime,
                'subscribers':self.subscribers,
                }