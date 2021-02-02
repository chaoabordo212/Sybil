# queryman.py
# Query management - list, find, add, remove, start 

import pymongo
import urllib
import traceback
from components.config_db import *
from components.dbagent import *
from components.ioagent import *

def queryman_status():

    try:
        database_connection_status = db_status()
        for key in database_connection_status:
            print(f' {key} --- {database_connection_status[key]} ')
        #return database_connection_status
    except Exception as err:
        status_trace = traceback.print_exception(type(err), err, err.__traceback__)
        return [ "status_error", status_trace ] 

def queryman_list_queries(arg1_collection_findmany_dict):

    result_list, posnum = [], 0
    try:
        result_list = query_list(arg1_collection_findmany_dict)
        num_queries = len(list(result_list))
        print(f' {num_queries} documents found ')
        print("DEBUG", "var result_list is of type ",type(result_list))
        for result in result_list:
            posnum =+ 1
            print( result_list[posnum]['Timestamp'], result_list[posnum]['URL'], result_list[posnum]['Title'] )
            print('')
    except Exception as err:
        list_trace = traceback.print_exception(type(err), err, err.__traceback__)
        return ("list_queries_error", list_trace)

# def query_management_list(arg1_list_dict):
#   var1_collection, var2_findmany_dict = arg1_list_dict['']