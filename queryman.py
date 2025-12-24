# queryman.py
# Query management - list, find, add, remove, start 

import traceback
import logging
from typing import Dict, Any, List

import components.config_db as config_db
from components.dbagent import db_status, query_list
import components.ioagent as ioagent

def queryman_status():
    """Check and return database connection status.

    Returns a dict with status information on success, or a dict with
    an `error` and `trace` on failure.
    """
    logger = logging.getLogger(__name__)
    try:
        database_connection_status = db_status()
        for key, val in database_connection_status.items():
            logger.info("%s --- %s", key, val)
        return {"ok": True, "status": database_connection_status}
    except Exception as err:
        status_trace = "".join(traceback.format_exception(type(err), err, err.__traceback__))
        logger.exception("queryman_status failed: %s", err)
        return {"error": "status_error", "trace": status_trace}

def queryman_list_queries(arg1_collection_findmany_dict: Dict[str, Any]) -> Dict[str, Any]:
    """List queries from a collection using `query_list` helper.

    Returns a dict with `ok`, `count`, and `results` on success, or
    `error` and `trace` on failure.
    """
    logger = logging.getLogger(__name__)
    try:
        cursor = query_list(arg1_collection_findmany_dict)
        results = list(cursor)
        num_queries = len(results)
        logger.info("%d documents found", num_queries)
        logger.debug("var results is of type %s", type(results))

        output: List[Dict[str, Any]] = []
        for result in results:
            result_id = result.get('_id')
            result_url = result.get('URL')
            result_title = result.get('Title')
            result_timestamp = result.get('Timestamp')
            result_instance = {
                "_id": result_id,
                "URL": result_url,
                "Title": result_title,
                "Timestamp": result_timestamp,
            }
            logger.info(result_instance)
            output.append(result_instance)

        return {"ok": True, "count": num_queries, "results": output}
    except Exception as err:
        list_trace = "".join(traceback.format_exception(type(err), err, err.__traceback__))
        logger.exception("queryman_list_queries failed: %s", err)
        return {"error": "list_queries_error", "trace": list_trace}

# def queryman_list_google_queries(arg1_google_doc):
    

# def queryman_add_


# def query_management_list(arg1_list_dict):
#   var1_collection, var2_findmany_dict = arg1_list_dict['']