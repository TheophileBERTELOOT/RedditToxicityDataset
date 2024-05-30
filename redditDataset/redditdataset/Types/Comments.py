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
        self.message:str = self.comment.body
        self.createdTime:str = self.comment.created_utc
        self.distinguished:bool=self.comment.distinguished
        self.submissionId:str = self.comment.link_id
        self.parentId:str = self.comment.parent_id
        self.score:int = self.comment.score
        self.subredditId:str = self.comment.subreddit_id


    def getDict(self):
        return {'id':self.id,
                'authorId':self.authorId,
                'message':self.message,
                'createdTime':self.createdTime,
                'distinguished':self.distinguished,
                'submissionId':self.submissionId,
                'subredditId':self.subredditId,
                'parentId':self.parentId,
                'score':self.score,
                }