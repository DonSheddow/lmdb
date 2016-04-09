import re

import tmdb
import ttdb


class TitleNotFound(Exception):
    pass



title_regex = re.compile(r'^(.*) \((\d{4})\)$')


def search(title):
    year = None
    match = title_regex.search(title)
    if match:
        title, year = match.group(1), int(match.group(2))
    
    tmdb_data = tmdb.search(title, year)
    
    if tmdb_data.media_type == 'tv':
        data = TVData()
    else:
        data = MovieData()
    
    data._tmdb = tmdb_data
#    data._ttdb = ttdb.from_imdbid(tmdb_data.basic_info['imdb_id'])
    
    return data



class Data(object):
    
    COLUMNS = ['title', 'summary', 'tmdb_rating']
    TMDB_KEYMAP = {'summary': 'overview', 'tmdb_rating': 'vote_average'}
    
    def __init__(self):
        self.TMDB_KEYS = [ self.TMDB_KEYMAP.get(col, col) for col in self.COLUMNS ]
    
    def basic_info(self):
        return { col: self._tmdb.basic_info[k] for col, k in zip(self.COLUMNS, self.TMDB_KEYS) }
    
    def genres(self):
        return self._tmdb.genres()
    
    def poster_url(self):
        return self._tmdb.poster()
    
    def cast(self):
        return self._tmdb.cast()


class TVData(Data):
    TMDB_KEYMAP = Data.TMDB_KEYMAP.copy()
    TMDB_KEYMAP['title'] = 'original_name'


class MovieData(Data):
    pass
