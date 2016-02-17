import requests
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET

from subprocess import Popen, DEVNULL

import config

BASE_URL = 'http://thetvdb.com/api/'
API_KEY = config.TTDB_APIKEY



def from_imdbid(imdb_id):
    params = {'imdbid': imdb_id}
    r = requests.get(BASE_URL + 'GetSeriesByRemoteID.php', params=params)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    
    entry = TTDBEntry(root.find('.//id').text)
    entry._basic = root
    
    return entry


class TTDBEntry(object):
    
    def __init__(self, id):
        self.id = id
        self._actors = None
        self._banners = None
        self._info = None
    
    def cast(self):
        if not self._actors:
            self.init_extra_info()
        
        actors = self._actors.findall('.//Actor')
        orders = ( int(i.find('SortOrder').text) for i in actors )
        names = ( i.find('Name').text for i in actors )
        roles = ( i.find('Role').text for i in actors )
        return list(zip(orders, names, roles))
    
    
    def init_extra_info(self):
        url = BASE_URL + API_KEY + '/series/%s/all/en.zip' % self.id
        r = requests.get(url, stream=True)
        r.raise_for_status()
        zipdir = tempfile.mkdtemp()
        zipfile = zipdir + '/en.zip'
        with open(zipfile, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        
        # Python's built-in zipfile module can't handle zipv2.0
        # so we use unzip instead
        sp = Popen(['/usr/bin/env', 'unzip', zipfile, '-d', zipdir], stdout=DEVNULL)
        sp.wait()
        
        with open(zipdir + '/en.xml') as f:
            self._info = ET.fromstring(f.read())
        
        with open(zipdir + '/actors.xml') as f:
            self._actors = ET.fromstring(f.read())
        
        with open(zipdir + '/banners.xml') as f:
            self._banners = ET.fromstring(f.read())
        
        shutil.rmtree(zipdir)
