cache = {}


def get_cached_response(query):
    return cache.get(query)



def save_to_cache(query, response):
    cache[query] = response