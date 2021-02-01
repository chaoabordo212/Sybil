# ioagent.py
## Input/Output agent for communication between components

import pymongo
import traceback
from .dbagent import *
from .config_db import *

def query_lastnum(arg1_collection_sortfield_showfield_dict):
    var1_collection, var2_sortfield, var3_showfield = arg1_collection_sortfield_showfield_dict['collection'], arg1_collection_sortfield_showfield_dict['findmany'], arg1_collection_sortfield_showfield_dict['showfield']
    try:
        lastnum = db_findlast(var1_collection, var2_sortfield)[var3_showfield]
        return lastnum
    except Exception as err:
        ioagent_trace = traceback.print_exception(type(err), err, err.__traceback__)
        return ioagent_trace
        return "lastnum_error"

def query_list(arg1_collection_findmany_dict):
    var1_collection, var2_findmany_dict = arg1_collection_findmany_dict['collection'], arg1_collection_findmany_dict['findmany']
    try:
        query_found_list = db_findmany(var1_collection, var2_findmany_dict)
        return query_found_list
    except Exception as err:
        ioagent_trace = traceback.print_exception(type(err), err, err.__traceback__)
        return ioagent_trace
        return "list_error"

#def query_find():
#
#def query_add():
#
#def query_remove():

# def query_input(arg1_query)

# def insert_searchstring(arg1_queries_collection, arg2_search_string):
#   search_dict = { "search_string" : arg2_search_string, "qnum" : qnum }
#   try:
#       inserted_searchstring = db_insertone(arg1_queries_collection, arg2_search_string)

# def search.string.load(search_string):

# def import_searchstring(search_string):
#   queries_collection = "queries"
#   try:
#       imported_searchstring = db_insertone(, search_string)