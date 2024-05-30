import praw
import pprint

class Author:
    def __init__(self,author:praw.models.Redditor):
        self.author:praw.models.Redditor = author
        self.fillInfos()
        
    def fillInfos(self):
        try:
            self.karma:int = self.author.comment_karma
        except:
            self.karma:int = -1
        try:
            self.createdTime:int = self.author.created_utc
        except:
            self.createdTime:int = None
        try:
            self.id:str = self.author.id
        except:
            self.id:str = ''
        try:
            self.isEmployee:bool=self.author.is_employee
        except:
            self.isEmployee:bool=False
        try:
            self.isMod:bool = self.author.is_mod
        except:
            self.isMod:bool = False
        try:
            self.isSuspended:bool = self.author.is_suspended
        except:
            self.isSuspended:bool = False
        try:
            self.name:str = self.author.name
        except:
            self.name:str = ''
        
        
    def getDict(self):
        return {'id':self.id,
                'name':self.name,
                'karma':self.karma,
                'createdTime':self.createdTime,
                'isEmployee':self.isEmployee,
                'isMod':self.isMod,
                'isSuspended':self.isSuspended,
                }