import requests

from time import sleep
from datetime import datetime, timedelta

import data
from lmdb import app

BASE_URL = 'http://api.themoviedb.org/3/'

try:
    API_KEY = app.config['TMDB_API_KEY']
except KeyError as e:
    e.message = "Can't find API key for TMDb. Please define TMDB_API_KEY in the configuration file"
    raise

config = {}

def _update_config():
    global config
    if not config or datetime.now() - config['last_updated'] > timedelta(days=2):
        config = _get('configuration')
        config['last_updated'] = datetime.now()


def _get(endpoint, **kwargs):
    url = BASE_URL + endpoint
    params = dict(api_key=API_KEY, **kwargs)
    headers = {'Accept': 'application/json'}
    
    r = requests.get(url, params=params, headers=headers)
    
    # Rate limited to 30 requests per 10 seconds
    if r.status_code == 503:
        sleep(10) # Could be reduced
        return _get(endpoint, **kwargs)
    
    r.raise_for_status()
    return r.json()


def search(title, year=None):
    
    r = _get('search/multi', query=title)
    
    for result in r['results']:
        t = result['media_type']
        if t not in ['movie', 'tv']:
            continue
        
        key = 'first_air_date' if t == 'tv' else 'release_date'
        
        if not year or (result[key] and int(result[key][:4]) == year):
            if result['media_type'] == 'movie':
                return TMDbMovie(result['media_type'], result['id'])
            else:
                return TMDbTV(result['media_type'], result['id'])
    
    y = " from year %d" % year if year else ""
    raise data.TitleNotFound("No results for '%s'%s" % (title, y))



class TMDbEntry(object):
    
    def __init__(self, media_type, id):
        self.media_type = media_type
        self.id = id
        self.basic_info = _get('%s/%s' % (media_type, id))
        self.credits = None
        _update_config()
    
    
    def genres(self):
        return [ i['name'] for i in self.basic_info['genres'] ]
    
    def poster(self):
        size = 'w342'
        assert size in config['images']['poster_sizes']
        return config['images']['base_url'] + size + self.basic_info['poster_path']
    
    def backdrop(self):
        size = 'w780'
        assert size in config['images']['backdrop_sizes']
        return config['images']['base_url'] + size + self.basic_info['backdrop_path']
    
    def cast(self):
        if not self.credits:
            self.credits = _get('%s/%s/credits' % (self.media_type, self.id))
        
        cast = self.credits['cast']
        return [ (i['order'], i['name'], i['character']) for i in cast ]
    



class TMDbMovie(TMDbEntry):
    pass
    
    


class TMDbTV(TMDbEntry):
    pass
    
    
