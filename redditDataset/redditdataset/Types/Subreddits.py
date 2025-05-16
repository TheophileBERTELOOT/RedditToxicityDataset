import praw

class Subreddits:
    def __init__(self,subreddit:praw.models.Subreddit):
        self.subreddit:praw.models.subreddit = subreddit
        self.fillInfos()
        
    def fillInfos(self):
        self.id:str = self.subreddit.id
        self.over18:bool = self.subreddit.over18
        self.name:str = self.subreddit.display_name
        self.createdTime:str = self.subreddit.created_utc
        self.subscribers:int=self.subreddit.subscribers
        self.moderators = []
        self.rules = []
        self.description = self.subreddit.description
        for moderator in self.subreddit.moderator():
            self.moderators.append(moderator.id)
        for rule in self.subreddit.rules:
            self.rules.append(rule.short_name)


    def getDict(self):
        return {'id':self.id,
                'over18':self.over18,
                'description':self.description,
                'name':self.name,
                'createdTime':self.createdTime,
                'subscribers':self.subscribers,
                'moderators':self.moderators,
                'rules':self.rules
                }