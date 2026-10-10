import time 

cache = {}

def get_cache(key:str|None):
    if key not in cache:
        return None
    data,timestamp = cache[key]

    if time.time()- timestamp >60:
        del cache[key]
        return None
    
    print("caching data")
    return data


def set_cache(key: str, data):
    cache[key] = (data, time.time())
    