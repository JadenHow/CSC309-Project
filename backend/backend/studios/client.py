from algoliasearch_django import algolia_engine
import time
now_timestamp = int(time.time())

def get_client():
    return algolia_engine.client

# def get_index(index_name='backend_Studio'):
#     client = get_client()
#     index = client.init_index(index_name)
#     return index

def get_index(index_name):
    client = get_client()
    index = client.init_index(index_name)
    return index

def perform_search(query, index_name, **kwargs):
    index = get_index(index_name)
    results = index.search(query)
    return results

def perform_search_studio_class(query, id):
    index = get_index('backend_ClassInstances')
    results = index.search(query, {
        'filters': 'studio:"Studio object (' + str(id) + ')"' ' AND ' + 'class_date_timestamp >= ' + str(now_timestamp)
    })
    return results
