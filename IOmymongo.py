# coding:utf-8
__author__ = 'diaoshe'
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import datetime
from bson.objectid import ObjectId


def conToMogd():
    "Connect to Mongodb"
    try:
        c = MongoClient('localhost', 27017)
        # client = MongoClient('mongodb://localhost:27017/')
        print "[+]Connected mongodb successfully"
        return c
    except ConnectionFailure, e:
        sys.stderr.write("[!]Could not connect to MongoDB: %s" % e)
        sys.exit(1)



def writeToMongo(mgcont,item):
    db = mgcont.protestdb
    collection = db.protestcol
    post_id = collection.insert(item)
    print "ObjectId:" + post_id   #感觉可以不写
