# ioagent.py
## Input/Output agent for communication between components

import pymongo
import traceback
from .dbagent import *
from .config_db import *


def query_lastqnum(arg1_queries_collection):
    try:
        lastqnum = db_findlast(arg1_queries_collection)['qnum']
        return lastqnum
    except Exception as err:
        traceback.print_exception(type(err), err, err.__traceback__)
        return "lastqnum_error"

# def insert_searchstring(arg1_queries_collection, arg2_search_string):
#   search_dict = { "search_string" : arg2_search_string, "qnum" : qnum }
#   try:
#       inserted_searchstring = db_insertone(arg1_queries_collection, arg2_search_string)

# def search.string.load(search_string):

# def import_searchstring(search_string):
#   queries_collection = "queries"
#   try:
#       imported_searchstring = db_insertone(, search_string)