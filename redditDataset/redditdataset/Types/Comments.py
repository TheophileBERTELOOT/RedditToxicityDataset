import praw

class Comments:
    def __init__(self,comment:praw.models.Comment):
        self.comment:praw.models.Comment = comment
        self.fillInfos()
    
    def fillInfos(self):
        try:
            self.authorId:str = self.comment.author.id
        except:
            self.authorId:str = ''
        self.id:str = self.comment.id
        self.body:str = self.comment.body
        self.created_utc:str = self.comment.created_utc
        self.distinguished:bool=self.comment.distinguished
        self.link_id:str = self.comment.link_id
        self.parent_id:str = self.comment.parent_id
        self.score:int = self.comment.score
        self.subreddit_id:str = self.comment.subreddit_id


    def getDict(self):
        return {'id':self.id,
                'authorId':self.authorId,
                'body':self.body,
                'created_utc':self.created_utc,
                'distinguished':self.distinguished,
                'link_id':self.link_id,
                'subreddit_id':self.subreddit_id,
                'parent_id':self.parent_id,
                'score':self.score,
                }