import pymongo
import copy

from redditDataset.redditdataset.Types.Authors import Author
from redditDataset.redditdataset.Types.Comments import Comments
from redditDataset.redditdataset.Types.Subreddits import Subreddits
from redditDataset.redditdataset.Enums.CollectionsNames import CollectionNames

class MongoHandler:
    def __init__(self,dbName='RedditToxicity',
                 collectionsNames=[CollectionNames.Authors.value,CollectionNames.Comments.value,CollectionNames.Subreddits.value]
                 ,verbose=False):
        self.mc = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.mc[dbName]
        self.session = self.mc.start_session()
        self.collectionsNames = collectionsNames
        self.initCollections()
        self.verbose = verbose
        
        
    def initCollections(self):
        self.myCols = {}
        for name in self.collectionsNames:
            self.myCols[name] = self.mydb[name]
        if CollectionNames.Authors.value in self.collectionsNames and  CollectionNames.Authors.value in self.mydb.list_collection_names():
            self.myCols[CollectionNames.Authors.value].create_index('id',unique=True)  
        if CollectionNames.Comments.value in self.collectionsNames and  CollectionNames.Comments.value in self.mydb.list_collection_names():
            self.myCols[CollectionNames.Comments.value].create_index('id',unique=True)
        if CollectionNames.Subreddits.value in self.collectionsNames and  CollectionNames.Subreddits.value in self.mydb.list_collection_names():
            self.myCols[CollectionNames.Subreddits.value].create_index('id',unique=True)
            

    '''
    def exportAuthorInfos(self,author:Author) -> bool:
        try :
            if CollectionNames.Authors.value in self.collectionsNames:
                doesAuthorAlreadyExist = len(list(self.myCols[CollectionNames.Authors.value].find({'id':author.id}))) > 0
                if not doesAuthorAlreadyExist :
                    self.myCols[CollectionNames.Authors.value].insert_one(author.getDict())
                    return True
                else:
                    #print('Author already exist in the database')
                    return False
            else:
                print('there is no Authors collection')
                return False
        except Exception as error :
            print(error)
            return False
'''
    def exportAuthorInfos(self,author:Author) -> bool:
        try :
            if CollectionNames.Authors.value in self.collectionsNames:
                self.myCols[CollectionNames.Authors.value].insert_one(author.getDict())
                return True
            else:
                print('there is no Authors collection')
                return False
        except Exception as error :
            print(error)
            return False

    def addDeletedField(self,comment,deleted):
        try :
            self.myCols[CollectionNames.Comments.value].update_one({"_id": comment["_id"]},
            {"$set": {"deleted": deleted}})
            return True
        except Exception as error :
            print(error)
            return False

    def addDeletedBodyField(self,comment,newBody):
        try :
            self.myCols[CollectionNames.Comments.value].update_one({"_id": comment["_id"]},
            {"$set": {"newBody": newBody}})
            return True
        except Exception as error :
            print(error)
            return False
    
    def exportAuthorsInfos(self,authors) ->bool:
        if self.verbose:
            print('begin exporting authors infos :')
            print(f'{len(authors)} authors to export')
        counter = 0
        for author in authors:
            res = self.exportAuthorInfos(author)
            if res :
                counter +=1
        if self.verbose:
            print(f'{counter} authors exported succesfully')
    ''' 
    def exportCommentInfos(self,comment:Comments) -> bool:
        try :
            if CollectionNames.Comments.value in self.collectionsNames:
                self.myCols[CollectionNames.Comments.value].insert_one(comment.getDict())
                return True
            else:
                print('there is no Comments collection')
                return False
        except Exception as error :
            print(error)
            return False
    '''
    def exportCommentInfos(self,comment:Comments) -> bool:
        try :
            self.myCols[CollectionNames.Comments.value].insert_one(comment.getDict())
            return True
        except Exception as error :
            print(error)
            return False
    
    def exportCommentsInfos(self,comments) ->bool:
        if self.verbose:
            print('begin exporting comments infos :')
            print(f'{len(comments)} comments to export')
        counter = 0
        for comment in comments:
            res = self.exportCommentInfos(comment)
            if res :
                counter +=1
        if self.verbose:
            print(f'{counter} comments exported succesfully')
            
    def exportSubredditInfos(self,subreddit:Subreddits) -> bool:
        if self.verbose:
            print('begin exporting subreddits infos :')
        try :
            doesSubredditAlreadyExist = len(list(self.myCols[CollectionNames.Subreddits.value].find({'id':subreddit.id}))) > 0
            if doesSubredditAlreadyExist:
                print('subreddit already exist in the database')
                return False
            else:
                if CollectionNames.Subreddits.value in self.collectionsNames :
                    self.myCols[CollectionNames.Subreddits.value].insert_one(subreddit.getDict())
                    return True
                else:
                    print('there is no Subreddits collection')
                    return False
        except Exception as error :
            print(error)
            return False
            
    def sampleComments(self):
        print('comments examples : ')
        res = self.myCols[CollectionNames.Comments.value].find().limit(10)
        for comment in res :
            print('__________________________________')
            print(comment)
            
    def sampleSubreddits(self):
        print('subreddits examples : ')
        res = self.myCols[CollectionNames.Subreddits.value].find().limit(10)
        for subreddit in res :
            print('__________________________________')
            print(subreddit)
            
    def sampleAuthors(self):
        print('authors examples : ')
        res = self.myCols[CollectionNames.Authors.value].find().limit(10)
        for author in res :
            print('__________________________________')
            print(author)
            
    def removeEverythingFromCollection(self,collectionName:CollectionNames):
        self.myCols[collectionName.value].delete_many({})
        
    def removeEverythingFromEveryCollection(self):
        for collection in CollectionNames :
            self.myCols[collection.value].delete_many({})

    def getAllNonCheckedComments(self):
        res = list(self.myCols[CollectionNames.Comments.value].find({'deleted':{'$exists':False}}))
        return res
    
    def getAllCheckedComments(self):
        res = list(self.myCols[CollectionNames.Comments.value].find({'newBody':{'$exists':True}}))
        return res
    
    def addLabels(self,id,label):
        try :
            self.myCols[CollectionNames.Comments.value].update_one({"_id": id},
            {"$set": {"label": label}})
            return True
        except Exception as error :
            print(error)
            return False
    
        
            
        
