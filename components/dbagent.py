# dbagent.py
## MongoDB agent for connecting, quering and managing database.

import pymongo
import urllib
from .config_db import *

def db_core():
    username = urllib.parse.quote_plus(mongodb_user)
    passwd = urllib.parse.quote_plus(mongodb_pass)
    connect_exp = "pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s' % (username, passwd, mongodb_host, mongodb_port, mongodb_admindb), serverSelectionTimeoutMS = 2000)"
    try:
        client_connect = eval(connect_exp)
        return client_connect
    except Exception as error:
        return False, error

def db_status():
    try:
        client_status = dict(db_core().server_info())
        connection_status = { "connected" : True }
        client_status.update(connection_status)
        return client_status
    except Exception as error:
        connection_status = { "connected" : False }
        client_status = { "error_msg":error }
        client_status.update(connection_status)
        return client_status

def db_core_collection(mongodb_dbname, arg1_collection):
    try:
        client_collection = db_core()[mongodb_dbname][arg1_collection]
        return client_collection
    except Exception as error:
        return False, error

def db_createindex(arg1_collection, arg2_indexname, arg3_field, arg4_order):
    try:
        index_status = {"created":True}
        index_created = { "index_name" : db_core_collection(mongodb_dbname, arg1_collection).create_index([ (arg3_field, arg4_order) ], name=arg2_indexname) }
        index_status.update(index_created)
        return index_status
    except Exception as error:
        index_status = {"created" : False}
        index_created = { "error_msg" : error }
        index_status.update(index_created)
        return index_status

def db_insertone(arg1_collection, arg2_insertone_dict):
    try:
        inserted_one = db_core_collection(mongodb_dbname, arg1_collection).insert_one(arg2_insertone_dict)
        return inserted_one.inserted_id
    except Exception as error:
        print(error)
        return "insertone_error"

def db_insertmany(arg1_collection, arg2_insertmany_dict):
    try:
        inserted_many = db_core_collection(mongodb_dbname, arg1_collection).insert_many(arg2_insertmany_dict)
        return inserted_many.inserted_id
    except Exception as error:
        print(error)
        return "insertmany_error"

def db_deleteone(arg1_collection, arg2_deleteone_dict):
    try:
        deleted_one = db_core_collection(mongodb_dbname, arg1_collection).delete_one(arg2_deleteone_dict)
        return deleted_one
    except Exception as error:
        print(error)
        return "deleteone_error"

def db_deletemany(arg1_collection, arg2_deletemany_dict):
    try:
        deleted_many = db_core_collection(mongodb_dbname, arg1_collection).delete_many(arg2_deletemany_dict)
        return deleted_many
    except Exception as error:
        print(error)
        return "deletemany_error"

def db_findone(arg1_collection, arg2_findone_dict):
    try:
        found_one = db_core_collection(mongodb_dbname, arg1_collection).find_one(arg2_findone_dict)
        return found_one
    except Exception as error:
        print(error)
        return "findone_error"

def db_findmany(arg1_collection, arg2_findmany_dict):
    found_many_list = []
    try:
        found_many = db_core_collection(mongodb_dbname, arg1_collection).find(arg2_findmany_dict)
        for x in found_many:
            found_many_list.append(x)
        return found_many_list
    except Exception as error:
        print(error)
        return "findmany_error"

def db_findlast(arg1_collection):
    try:
        found_last = db_core_collection(mongodb_dbname, arg1_collection).find().sort('qnum', -1).limit(1)
        for x in found_last:
            return x

    except Exception as error:
        print(error)
        return "findlast_error"

def db_updateone(arg1_collection, arg2_findone_dict, arg3_updateone_dict):
    try:
        updated_one = db_core_collection(mongodb_dbname, arg1_collection).update_one(arg2_findone_dict, arg3_updateone_dict)
        return updated_one
    except Exception as error:
        print(error)
        return "updateone_error"

def db_updatemany(arg1_collection, arg2_findmany_dict, arg3_updatemany_dict):
    try:
        updated_many = db_core_collection(mongodb_dbname, arg1_collection).update_many(arg2_findmany_dict, arg3_updatemany_dict)
        return updated_many
    except Exception as error:
        print(error)
        return "updatemany_error"
