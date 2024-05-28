import praw
import pprint

class Author:
    def __init__(self,author:praw.models.Redditor):
        self.author:praw.models.Redditor = author
        self.fillInfos()
        
    def fillInfos(self):
        self.karma:int = self.author.comment_karma
        self.createdTime:int = self.author.created_utc
        self.id:str = self.author.id
        self.isEmployee:bool=self.author.is_employee
        self.isMod:bool = self.author.is_mod
        try:
            self.isSuspended:bool = self.author.is_suspended
        except:
            self.isSuspended:bool = False
        self.name:str = self.author.name
        
    def getDict(self):
        return {'id':self.id,
                'name':self.name,
                'karma':self.karma,
                'createdTime':self.createdTime,
                'isEmployee':self.isEmployee,
                'isMod':self.isMod,
                'isSuspended':self.isSuspended,
                }