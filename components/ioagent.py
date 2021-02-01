# ioagent.py
## Input/Output agent for communication between components

import pymongo
import traceback
from .dbagent import *
from .config_db import *


def query_lastqnum(dict1_collection_sortfield):
    arg1_collection, arg2_sortfield = dict1_collection_sortfield['collection'], dict1_collection_sortfield['sortfield']
    try:
        lastqnum = db_findlast(arg1_collection, arg2_sortfield)['Num']
        return lastqnum
    except Exception as err:
        ioagent_trace = traceback.print_exception(type(err), err, err.__traceback__)
        return ioagent_trace
        return "lastqnum_error"

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