# googleagent.py
## Google agent for importing google queries, searching them and piping the result wherever needed.
import urllib
import re
import unidecode
import time
import ssl
import certifi 
from googlesearch import search
from urllib.error import HTTPError


def google_search(search_query):
    i = 0
    search_result_list = []
    query_sanitized = unidecode.unidecode(re.sub(r'\.+', "_", re.sub('[\W_]', '.', search_query)))
    query_short = ' '.join(query_sanitized.split("_")[:12])
    if len(query_short) >= 122:
        query_short = ' '.join(query_sanitized.split("_")[:12]) + "..."
    try:
        for url in search(search_query + ' -filetype:pdf ',   # The query you want to run
#                   tld = 'com',  # The top level domain
#                   lang = 'en',  # The language
#                   start = 0,    # First result to retrieve
#                   stop = stop_after,    # Last result to retrieve
                    num = 10,     # Number of results per page
                    pause = 4.0,  # Lapse between HTTP requests
                    ):
            time.sleep(0.3)
            i += 1
            search_result = [ i, url ]
            print(search_result)
            search_result_list.append(search_result)
        return search_result_list
    except IndexError as e:
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print('Index error occured: ' + str(e.code))
    except HTTPError as err:
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print("Error occured for string: " + str(query_short))
        print(err)
        if err.code == 429:
            print('Too many requests; temporarily blocked by Google')
            print("Sleeping for 1200 secs")
            countdown(1200)
            print("Retrying...")
            google_search(search_query)
    except Exception as error:
        print('ERROR --- Searching interrupted by exception')
        print("Error code: " + str(error))