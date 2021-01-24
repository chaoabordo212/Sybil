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

def db_insertdoc(arg1_collection, arg2_newdoc_dict):
    try:
        inserted_doc = db_core_collection(mongodb_dbname, arg1_collection).insert_one(arg2_newdoc_dict)
        return inserted_doc
    except Exception as error:
        print(error)
        return "createdoc_error"

def db_deletedoc(arg1_collection, arg2_deldoc_dict):
    try:
        deleted_doc = db_core_collection(mongodb_dbname, arg1_collection).delete_one(arg2_deldoc_dict)
        return deleted_doc
    except Exception as error:
        print(error)
        return "deletedoc_error"

def db_findone(arg1_collection, arg2_findone_dict):
    try:
        found_one = db_core_collection(mongodb_dbname, arg1_collection).find_one(arg2_findone_dict)
        return found_one
    except Exception as error:
        print(error)
        return "findone_error"

def db_findall(arg1_collection, arg2_findall_dict):
    try:
        found_all = db_core_collection(mongodb_dbname, arg1_collection).find(arg2_findall_dict)
        for x in found_all:
            found_all_list.append(x)
        return found_all_list
    except Exception as error:
        print(error)
        return "findall_error"

def db_updateone(arg1_collection, arg2_findone_dict, arg3_updateone_dict):
    try:
        updated_one = db_core_collection(mongodb_dbname, arg1_collection).update_one(arg2_findone_dict, arg3_updateone_dict)
        return updated_one
    except Exception as error:
        print(error)
        return "updateone_error"

def db_updateall(arg1_collection, arg2_findall_dict, arg3_updateall_dict):
    try:
        updated_all = db_core_collection(mongodb_dbname, arg1_collection).update_many(arg2_findall_dict, arg3_updateall_dict)
        return updated_all
    except Exception as error:
        print(error)
        return "updateall_error"












###########################################################
# def db_find(arg1_collection, query_key, query_value ):

#     query_dict = { query_key : {"$regex" : query_value}}
#     print(query_dict)  ###DEBUG
#     db_find_result = db_core_collection(mongodb_dbname, arg1_collection).find(query_dict)
#     #print(db_find_result)  ###DEBUG
#     #print(list(db_find_result))
#     result_list = []
#     for result in db_find_result:
#         result_list.append(result)
#     return result_list

# def db_findall(arg1_collection, query_string):
#     try:
#         query_dict = query_sting[0]
#         print(query_dict)
#     except Exception as error:
#         print(error)
#         pass
#     try:
#         sort_list = query_sting[1]
#         print(sort_list)
#     except Exception as error:
#         print(error)
#         #pass
#     try:
#         display_dict = query_sting[2]
#         print(display_dict)
#     except Exception as error:
#         print(error)
#        #pass
    
#     # query_key
#     # query_value
#     query_results_list = []
#     query_results_instance = {}
#     #query_dict = dict(query_string)
#     try:
#         if not sort_list and display_dict:
#             query_results_pointer = db_core_collection(mongodb_dbname, arg1_collection).find(( query_dict ),( display_dict ))
#         elif sort_list and not display_dict:
#             query_results_pointer = db_core_collection(mongodb_dbname, arg1_collection).find(( query_dict )).sort( sort_list )
#         elif not display_dict and not sort_list:
#             query_results_pointer = db_core_collection(mongodb_dbname, arg1_collection).find(( query_dict ))
#         else:
#             query_results_pointer = db_core_collection(mongodb_dbname, arg1_collection).find(( query_dict ),( display_dict )).sort( sort_list )

#         for item in query_results_pointer:
#             try:
#                 query_results_instance = item
#                 query_results_instance = dict(query_results_instance)
#                 query_results_list.append(query_results_instance)
#             except Exception as error:
#                 # print(red(f'Function mongodb_query_search at {cyan(item)} {red(" failed.")}'))
#                 # print(yellow("Error details: ") + red(err))
#                 # traceback.print_exception(type(err), err, err.__traceback__)
#                 print(error)
#                 pass
#     except Exception as error:
#         # traceback.print_exception(type(err), err, err.__traceback__)
#         print(error)
#         pass
#     return query_results_list

# def db_list_collections:
#     db_core_database = db_core()[mongodb_dbname]

# def db_list_documents:

# def db_findall(_id):
#     dbuser = urllib.parse.quote_plus(db_u)
#     dbpass = urllib.parse.quote_plus(db_p)
#     collection_name = "beautifulsoup"
#     mng_client = pymongo.MongoClient('mongodb://%s:%s@%s:%s/%s' % (dbuser, dbpass, dbhost, dbport, user_db))
#     mng_db = mng_client[database_name]
#     db_cm = mng_db[collection_name]
#     json_time = json_timestamp()
#     try:
#         if db_cm.count_documents({ "_id": _id }, limit = 1) != 0:
#             return True
#         else:
#             return False
#     except Exception as err:
#         print(red(f'MongoDB query of link_id {cyan(link_id)} {red(" failed.")}'))
#         print(yellow("Error details: ") + red(err))
#         traceback.print_exception(type(err), err, err.__traceback__)
#         pass

###TODO:
# def db_findall():
# def db_delete():
# def db_update():
# def db_create():
# def db_popquery():

