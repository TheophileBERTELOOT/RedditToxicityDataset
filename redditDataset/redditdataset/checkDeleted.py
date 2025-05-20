import json
import time 

from redditDataset.redditdataset.MongoHandler import MongoHandler
from redditDataset.redditdataset.Gatherer import Gatherer

def fixLabels():
    mongo = MongoHandler(verbose=True)
    comments = mongo.getAllCheckedComments()
    for comment in comments:
        if comment['newBody'] == '[effacé]' or comment['newBody'] == '[ Removed by Reddit ':
            mongo.addLabels(comment['_id'],1)
        else:
            mongo.addLabels(comment['_id'],0)

def cli():
    with open("../config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    mongo = MongoHandler(verbose=True)

    gatherer = Gatherer(config)

    comments = mongo.getAllNonCheckedComments()

    for comment in comments:
        try :
            newComment = gatherer.getCommentById(comment['id'])
            if newComment.body!= comment['body']:
                if not newComment.edited :
                    mongo.addDeletedField(comment,'Deleted')
                    mongo.addDeletedBodyField(comment,newComment.body)
                else:
                    mongo.addDeletedField(comment,'Not Deleted')
            else:
                mongo.addDeletedField(comment,'Not Deleted')
        except:
            print('Issue with api')
            time.sleep(10)