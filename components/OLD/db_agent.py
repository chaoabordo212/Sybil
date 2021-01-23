### db_agent.py
#	Agent app for communication with mongoDB backend
import pymongo
import urllib


from .components.config_db import *


def db_test_connection():
	collection_name = db_collection
    dbuser = urllib.parse.quote_plus(db_u)
    dbpass = urllib.parse.quote_plus(db_p)
    mng_client = pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s' % (dbuser, dbpass, dbhost, dbport, user_db))
    mng_db = mng_client[database_name]
    db_cm = mng_db[collection_name]