from algoliasearch_django import algolia_engine
import time
import datetime
now_timestamp = int(time.time())

def get_client():
    return algolia_engine.client

def get_index(index_name='backend_ClassInstances'):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, **kwargs):
    if "start" in kwargs:
        start = kwargs.pop("start") or None
        if start is not None:
            start_unix = time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple())
    if "end" in kwargs:
        end = kwargs.pop("end") or None
        if end is not None:
            end_unix = time.mktime(datetime.datetime.strptime(end, "%Y-%m-%d").timetuple())
    if "starttime" in kwargs:
        starttime = kwargs.pop("starttime") or None
        if starttime is not None:
            starttime = starttime.split(':')
            starttime = starttime[0] + starttime[1] + starttime[2]
    if "endtime" in kwargs:
        endtime = kwargs.pop("endtime") or None
        if endtime is not None:
            endtime = endtime.split(':')
            endtime = endtime[0] + endtime[1] + endtime[2]
    
    index = get_index()
    if start and end and (not starttime) and (not endtime):
        results = index.search(query, {
            'filters': f'class_date_timestamp:{start_unix} TO {end_unix}'
            })
    elif start and (not end) and (not starttime):      
        results = index.search(query, {
            'filters': 'class_date_timestamp >= ' + str(start_unix)
            })
    elif starttime and endtime and (not start) and (not end):
        results = index.search(query, {
            'filters': f'start_time_timestamp:{starttime} TO {endtime}'
            })
    elif starttime and (not endtime) and (not start) and (not end):
        results = index.search(query, {
            'filters': 'start_time_timestamp >= ' + str(starttime)
            })
    elif start and starttime and (not endtime) and (not end):
        results = index.search(query, {
            'filters': 'class_date_timestamp >= ' + str(start_unix) + ' AND ' + 'start_time_timestamp >= ' + str(starttime)
            })
    elif (not start) and (not starttime) and (not endtime) and end:
        results = index.search(query, {
            'filters': f'class_date_timestamp:{now_timestamp} TO {end_unix}'
            })
    else: 
        results = index.search(query)

    return results
