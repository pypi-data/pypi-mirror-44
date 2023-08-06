# Author: echel0n <echel0n@sickrage.ca>
# URL: https://sickrage.ca
# Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#
# This file is part of SickRage.
#
# SickRage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SickRage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SickRage.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import time
from datetime import datetime, timedelta

import sickrage
from sickrage.core.helpers import full_sanitizeSceneName
from sickrage.core.helpers.encoding import strip_accents
from sickrage.core.scene_exceptions import retrieve_exceptions, get_scene_seasons, get_scene_exceptions


class NameCache(object):
    def __init__(self, *args, **kwargs):
        self.name = "NAMECACHE"
        self.min_time = 10
        self.last_update = {}
        self.cache = {}

    def should_update(self, show):
        # if we've updated recently then skip the update
        if datetime.today() - (self.last_update.get(show.name) or datetime.fromtimestamp(
                int(time.mktime(datetime.today().timetuple())))) < timedelta(minutes=self.min_time):
            return True

    def put(self, name, indexer_id=0):
        """
        Adds the show & tvdb id to the scene_names table in cache db

        :param name: The show name to cache
        :param indexer_id: the TVDB id that this show should be cached with (can be None/0 for unknown)
        """

        # standardize the name we're using to account for small differences in providers
        name = full_sanitizeSceneName(name)

        self.cache[name] = int(indexer_id)

        dbData = [x for x in sickrage.app.cache_db.get_many('scene_names', name) if x['indexer_id'] == indexer_id]
        if not len(dbData):
            # insert name into cache
            sickrage.app.cache_db.insert({
                '_t': 'scene_names',
                'indexer_id': indexer_id,
                'name': name
            })

    def get(self, name):
        """
        Looks up the given name in the scene_names table in cache db

        :param name: The show name to look up.
        :return: the TVDB id that resulted from the cache lookup or None if the show wasn't found in the cache
        """
        name = full_sanitizeSceneName(name)
        if name in self.cache:
            return int(self.cache[name])

    def clear(self, indexerid=None, name=None):
        """
        Deletes all entries from the cache matching the indexerid or name.
        """
        if any([indexerid, name]):
            for x in sickrage.app.cache_db.all('scene_names'):
                if x['indexer_id'] == indexerid or x['name'] == name:
                    sickrage.app.cache_db.delete(x)

            for key, value in self.cache.items():
                if value == indexerid or key == name:
                    del self.cache[key]

    def load(self):
        self.cache = dict([(x['name'], x['indexer_id']) for x in sickrage.app.cache_db.all('scene_names')])

    def save(self):
        """Commit cache to database file"""
        for name, indexer_id in self.cache.items():
            dbData = [x for x in sickrage.app.cache_db.get_many('scene_names', name) if x['indexer_id'] == indexer_id]
            if len(dbData):
                continue

            # insert name into cache
            sickrage.app.cache_db.insert({
                '_t': 'scene_names',
                'indexer_id': indexer_id,
                'name': name
            })

    def build(self, show):
        """Build internal name cache

        :param show: Specify show to build name cache for, if None, just do all shows
        """

        retrieve_exceptions()

        if self.should_update(show):
            self.last_update[show.name] = datetime.fromtimestamp(int(time.mktime(datetime.today().timetuple())))

            self.clear(show.indexerid)

            show_names = []
            for curSeason in [-1] + get_scene_seasons(show.indexerid):
                for name in list(set(get_scene_exceptions(show.indexerid, season=curSeason) + [show.name])):
                    show_names.append(name)
                    show_names.append(strip_accents(name))
                    show_names.append(strip_accents(name).replace("'", " "))

            for show_name in set(show_names):
                self.clear(show_name)
                self.put(show_name, show.indexerid)

    def build_all(self):
        for show in sickrage.app.showlist:
            self.build(show)
