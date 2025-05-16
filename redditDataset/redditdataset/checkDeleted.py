import json

from redditDataset.redditdataset.MongoHandler import MongoHandler
from redditDataset.redditdataset.Gatherer import Gatherer


def cli():
    with open("../config.json", "r") as jsonfile:
        config = json.load(jsonfile)

    mongo = MongoHandler(verbose=True)

    gatherer = Gatherer(config)

    comments = mongo.getAllNonCheckedComments()

    for comment in comments:
        newComment = gatherer.getCommentById(comment['id'])
        if newComment.body!= comment['body']:
            if not newComment.edited :
                mongo.addDeletedField(comment,'Deleted')
                mongo.addDeletedBodyField(comment,newComment.body)
                for key, value in vars(newComment).items():
                    print(f"{key}: {value}")
                print('-----------------------------------')
        else:
            mongo.addDeletedField(comment,'Not Deleted')