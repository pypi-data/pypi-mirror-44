# Author: Frank Fenton
# URL: https://sickrage.ca
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

import os
import threading
import traceback
from datetime import date

import sickrage
from sickrage.core.common import Quality
from sickrage.core.common import SKIPPED, WANTED, UNKNOWN
from sickrage.core.helpers import findCertainShow, sanitizeFileName, makeDir, chmod_as_parent
from sickrage.core.queues.search import BacklogQueueItem
from sickrage.core.traktapi import srTraktAPI
from sickrage.indexers import IndexerApi


def setEpisodeToWanted(show, s, e):
    """
    Sets an episode to wanted, only if it is currently skipped
    """
    epObj = show.get_episode(int(s), int(e))
    if epObj:
        with epObj.lock:
            if epObj.status != SKIPPED or epObj.airdate == date.fromordinal(1):
                return

            sickrage.app.log.info("Setting episode %s S%02dE%02d to wanted" % (show.name, s, e))
            # figure out what segment the episode is in and remember it so we can backlog it

            epObj.status = WANTED
            epObj.save_to_db()

        sickrage.app.search_queue.put(BacklogQueueItem(show, [epObj]))

        sickrage.app.log.info(
            "Starting backlog search for %s S%02dE%02d because some episodes were set to wanted" % (
                show.name, s, e))


class TraktSearcher(object):
    def __init__(self):
        self.name = "TRAKTSEARCHER"

        self.todoBacklog = []
        self.todoWanted = []
        self.ShowWatchlist = {}
        self.EpisodeWatchlist = {}
        self.Collectionlist = {}
        self.amActive = False

    def run(self, force=False):
        if self.amActive or (not sickrage.app.config.use_trakt or sickrage.app.developer) and not force:
            return

        self.amActive = True

        # set thread name
        threading.currentThread().setName(self.name)

        self.todoWanted = []  # its about to all get re-added
        if len(sickrage.app.config.root_dirs.split('|')) < 2:
            sickrage.app.log.warning("No default root directory")
            return

        # add shows from tv watchlist
        if sickrage.app.config.trakt_sync_watchlist:
            try:
                self.syncWatchlist()
            except Exception:
                sickrage.app.log.debug(traceback.format_exc())

        # add shows from tv collection
        if sickrage.app.config.trakt_sync:
            try:
                self.syncCollection()
            except Exception:
                sickrage.app.log.debug(traceback.format_exc())

        self.amActive = False

    def syncWatchlist(self):
        sickrage.app.log.debug("Syncing SiCKRAGE with Trakt Watchlist")

        self.removeShowFromSickRage()

        if self._getShowWatchlist():
            self.addShowToTraktWatchList()
            self.updateShows()

        if self._getEpisodeWatchlist():
            self.addEpisodesToTraktWatchList()
            if sickrage.app.config.trakt_remove_show_from_sickrage:
                self.removeEpisodesFromTraktWatchList()
            self.updateEpisodes()

    def syncCollection(self):
        sickrage.app.log.debug("Syncing SiCKRAGE with Trakt Collection")
        if self._getShowCollection():
            self.addEpisodesToTraktCollection()
            if sickrage.app.config.trakt_sync_remove:
                self.removeEpisodesFromTraktCollection()

    def findShowMatch(self, indexer, indexerid):
        traktShow = None

        try:
            library = srTraktAPI()["sync/collection"].shows() or {}
            if not library:
                sickrage.app.log.debug("No shows found in your library, aborting library update")
                return

            traktShow = [x for __, x in library.items() if
                         int(indexerid) == int(x.ids[IndexerApi(indexer).trakt_id])]
        except Exception as e:
            sickrage.app.log.warning(
                "Could not connect to Trakt service. Aborting library check. Error: %s" % repr(e))

        return traktShow

    def removeShowFromTraktLibrary(self, show_obj):
        if self.findShowMatch(show_obj.indexer, show_obj.indexerid):
            # URL parameters
            data = {
                'shows': [
                    {
                        'title': show_obj.name,
                        'year': show_obj.startyear,
                        'ids': {IndexerApi(show_obj.indexer).trakt_id: show_obj.indexerid}
                    }
                ]
            }

            sickrage.app.log.debug("Removing %s from tv library" % show_obj.name)

            try:
                srTraktAPI()["sync/collection"].remove(data)
            except Exception as e:
                sickrage.app.log.warning(
                    "Could not connect to Trakt service. Aborting removing show %s from Trakt library. Error: %s" % (
                        show_obj.name, repr(e)))

    def addShowToTraktLibrary(self, show_obj):
        """
        Sends a request to trakt indicating that the given show and all its episodes is part of our library.

        show_obj: The TVShow object to add to trakt
        """
        data = {}

        if not self.findShowMatch(show_obj.indexer, show_obj.indexerid):
            # URL parameters
            data = {
                'shows': [
                    {
                        'title': show_obj.name,
                        'year': show_obj.startyear,
                        'ids': {IndexerApi(show_obj.indexer).trakt_id: show_obj.indexerid}
                    }
                ]
            }

        if len(data):
            sickrage.app.log.debug("Adding %s to tv library" % show_obj.name)

            try:
                srTraktAPI()["sync/collection"].add(data)
            except Exception as e:
                sickrage.app.log.warning(
                    "Could not connect to Trakt service. Aborting adding show %s to Trakt library. Error: %s" % (
                        show_obj.name, repr(e)))
                return

    def addEpisodesToTraktCollection(self):
        trakt_data = []

        sickrage.app.log.debug("COLLECTION::SYNC::START - Look for Episodes to Add to Trakt Collection")

        for s in sickrage.app.showlist:
            for e in sickrage.app.main_db.get_many('tv_episodes', s.indexerid):
                trakt_id = IndexerApi(s.indexer).trakt_id
                if not self._checkInList(trakt_id, str(e["showid"]), e["season"], e["episode"], 'Collection'):
                    sickrage.app.log.debug(
                        "Adding Episode %s S%02dE%02d to collection" % (s.name, e["season"], e["episode"]))
                    trakt_data.append((e["showid"], s.indexer, s.name, s.startyear, e["season"], e["episode"]))

        if len(trakt_data):
            try:
                srTraktAPI()["sync/collection"].add(self.trakt_bulk_data_generate(trakt_data))
                self._getShowCollection()
            except Exception as e:
                sickrage.app.log.warning("Could not connect to Trakt service. Error: %s" % e)

        sickrage.app.log.debug("COLLECTION::ADD::FINISH - Look for Episodes to Add to Trakt Collection")

    def removeEpisodesFromTraktCollection(self):
        trakt_data = []

        sickrage.app.log.debug(
            "COLLECTION::REMOVE::START - Look for Episodes to Remove From Trakt Collection")

        for s in sickrage.app.showlist:
            for e in sickrage.app.main_db.get_many('tv_episodes', s.indexerid):
                if e["location"]: continue
                trakt_id = IndexerApi(s.indexer).trakt_id
                if self._checkInList(trakt_id, str(e["showid"]), e["season"], e["episode"], 'Collection'):
                    sickrage.app.log.debug(
                        "Removing Episode %s S%02dE%02d from collection" % (s.name, e["season"], e["episode"]))
                    trakt_data.append((e["showid"], s.indexer, s.name, s.startyear, e["season"], e["episode"]))

        if len(trakt_data):
            try:
                srTraktAPI()["sync/collection"].remove(self.trakt_bulk_data_generate(trakt_data))
                self._getShowCollection()
            except Exception as e:
                sickrage.app.log.warning("Could not connect to Trakt service. Error: %s" % e)

        sickrage.app.log.debug(
            "COLLECTION::REMOVE::FINISH - Look for Episodes to Remove From Trakt Collection")

    def removeEpisodesFromTraktWatchList(self):
        trakt_data = []

        sickrage.app.log.debug(
            "WATCHLIST::REMOVE::START - Look for Episodes to Remove from Trakt Watchlist")

        for s in sickrage.app.showlist:
            for e in sickrage.app.main_db.get_many('tv_episodes', s.indexerid):
                trakt_id = IndexerApi(s.indexer).trakt_id
                if self._checkInList(trakt_id, str(e["showid"]), e["season"], e["episode"]):
                    sickrage.app.log.debug(
                        "Removing Episode %s S%02dE%02d from watchlist" % (s.name, e["season"], e["episode"]))
                    trakt_data.append((e["showid"], s.indexer, s.name, s.startyear, e["season"], e["episode"]))

        if len(trakt_data):
            try:
                data = self.trakt_bulk_data_generate(trakt_data)
                srTraktAPI()["sync/watchlist"].remove(data)
                self._getEpisodeWatchlist()
            except Exception as e:
                sickrage.app.log.warning("Could not connect to Trakt service. Error: %s" % e)

        sickrage.app.log.debug(
            "WATCHLIST::REMOVE::FINISH - Look for Episodes to Remove from Trakt Watchlist")

    def addEpisodesToTraktWatchList(self):
        trakt_data = []

        sickrage.app.log.debug("WATCHLIST::ADD::START - Look for Episodes to Add to Trakt Watchlist")

        for s in sickrage.app.showlist:
            for e in sickrage.app.main_db.get_many('tv_episodes', s.indexerid):
                if not e['status'] in Quality.SNATCHED + Quality.SNATCHED_PROPER + [UNKNOWN] + [WANTED]: continue
                trakt_id = IndexerApi(s.indexer).trakt_id
                if self._checkInList(trakt_id, str(e["showid"]), e["season"], e["episode"]):
                    sickrage.app.log.debug(
                        "Adding Episode %s S%02dE%02d to watchlist" % (s.name, e["season"], e["episode"]))
                    trakt_data.append((e["showid"], s.indexer, s.name, s.startyear, e["season"], e["episode"]))

        if len(trakt_data):
            try:
                data = self.trakt_bulk_data_generate(trakt_data)
                srTraktAPI()["sync/watchlist"].add(data)
                self._getEpisodeWatchlist()
            except Exception as e:
                sickrage.app.log.warning("Could not connect to Trakt service. Error %s" % e)

        sickrage.app.log.debug("WATCHLIST::ADD::FINISH - Look for Episodes to Add to Trakt Watchlist")

    def addShowToTraktWatchList(self):
        trakt_data = []

        sickrage.app.log.debug("SHOW_WATCHLIST::ADD::START - Look for Shows to Add to Trakt Watchlist")

        for show in sickrage.app.showlist:
            if not self._checkInList(IndexerApi(show.indexer).trakt_id, str(show.indexerid), 0, 0, 'Show'):
                sickrage.app.log.debug(
                    "Adding Show: Indexer %s %s - %s to Watchlist" % (
                        IndexerApi(show.indexer).trakt_id, str(show.indexerid), show.name))

                show_el = {'title': show.name,
                           'year': show.startyear,
                           'ids': {IndexerApi(show.indexer).trakt_id: show.indexerid}}

                trakt_data.append(show_el)

        if len(trakt_data):
            try:
                data = {'shows': trakt_data}
                srTraktAPI()["sync/watchlist"].add(data)
                self._getShowWatchlist()
            except Exception as e:
                sickrage.app.log.warning("Could not connect to Trakt service. Error: %s" % e)

        sickrage.app.log.debug("SHOW_WATCHLIST::ADD::FINISH - Look for Shows to Add to Trakt Watchlist")

    def removeShowFromSickRage(self):
        sickrage.app.log.debug("SHOW_SICKRAGE::REMOVE::START - Look for Shows to remove from SiCKRAGE")

        for show in sickrage.app.showlist:
            if show.status == "Ended":
                try:
                    progress = srTraktAPI()["shows"].get(show.imdbid)
                except Exception as e:
                    sickrage.app.log.warning(
                        "Could not connect to Trakt service. Aborting removing show %s from SiCKRAGE. Error: %s" % (
                            show.name, repr(e)))
                    return

                if progress.status in ['canceled', 'ended']:
                    sickrage.app.show_queue.removeShow(show, full=True)
                    sickrage.app.log.debug("Show: %s has been removed from SiCKRAGE" % show.name)

        sickrage.app.log.debug("SHOW_SICKRAGE::REMOVE::FINISH - Trakt Show Watchlist")

    def updateShows(self):
        sickrage.app.log.debug("SHOW_WATCHLIST::CHECK::START - Trakt Show Watchlist")

        if not len(self.ShowWatchlist):
            sickrage.app.log.debug("No shows found in your watchlist, aborting watchlist update")
            return

        for key, show in self.ShowWatchlist.items():
            # get traktID and indexerID values
            trakt_id, indexer_id = key

            try:
                # determine
                indexer = IndexerApi().indexersByTraktID[trakt_id]
            except KeyError:
                continue

            if trakt_id == IndexerApi(indexer).trakt_id:
                if int(sickrage.app.config.trakt_method_add) != 2:
                    self.addDefaultShow(indexer, indexer_id, show.title, SKIPPED)
                else:
                    self.addDefaultShow(indexer, indexer_id, show.title, WANTED)

                if int(sickrage.app.config.trakt_method_add) == 1:
                    newShow = findCertainShow(indexer_id)

                    if newShow is not None:
                        setEpisodeToWanted(newShow, 1, 1)
                    else:
                        self.todoWanted.append((indexer_id, 1, 1))

        sickrage.app.log.debug("SHOW_WATCHLIST::CHECK::FINISH - Trakt Show Watchlist")

    def updateEpisodes(self):
        """
        Sets episodes to wanted that are in trakt watchlist
        """
        sickrage.app.log.debug("SHOW_WATCHLIST::CHECK::START - Trakt Episode Watchlist")

        if not len(self.EpisodeWatchlist):
            sickrage.app.log.debug("No episode found in your watchlist, aborting episode update")
            return

        managed_show = []

        for key, show in self.EpisodeWatchlist.items():
            # get traktID and indexerID values
            trakt_id, indexer_id = key

            try:
                # determine
                indexer = IndexerApi().indexersByTraktID[trakt_id]
            except KeyError:
                continue

            newShow = findCertainShow(indexer_id)

            try:
                if newShow is None:
                    if indexer_id not in managed_show:
                        self.addDefaultShow(indexer, indexer_id, show.title, SKIPPED)
                        managed_show.append(indexer_id)

                        for season_number, season in show.seasons.items():
                            for episode_number, _ in season.episodes.items():
                                self.todoWanted.append((int(indexer_id), int(season_number), int(episode_number)))
                else:
                    if newShow.indexer == indexer:
                        for season_number, season in show.seasons.items():
                            for episode_number, _ in season.episodes.items():
                                setEpisodeToWanted(newShow, int(season_number), int(episode_number))
            except TypeError:
                sickrage.app.log.debug("Could not parse the output from trakt for %s " % show.title)

        sickrage.app.log.debug("SHOW_WATCHLIST::CHECK::FINISH - Trakt Episode Watchlist")

    @staticmethod
    def addDefaultShow(indexer, indexer_id, name, status):
        """
        Adds a new show with the default settings
        """
        if not findCertainShow(int(indexer_id)):
            sickrage.app.log.info("Adding show " + str(indexer_id))
            root_dirs = sickrage.app.config.root_dirs.split('|')

            try:
                location = root_dirs[int(root_dirs[0]) + 1]
            except Exception:
                location = None

            if location:
                showPath = os.path.join(location, sanitizeFileName(name))
                dir_exists = makeDir(showPath)

                if not dir_exists:
                    sickrage.app.log.warning("Unable to create the folder %s , can't add the show" % showPath)
                    return
                else:
                    chmod_as_parent(showPath)

                sickrage.app.show_queue.addShow(int(indexer), int(indexer_id), showPath,
                                                default_status=status,
                                                quality=int(sickrage.app.config.quality_default),
                                                flatten_folders=int(sickrage.app.config.flatten_folders_default),
                                                paused=sickrage.app.config.trakt_start_paused,
                                                default_status_after=status,
                                                skip_downloaded=sickrage.app.config.skip_downloaded_default)
            else:
                sickrage.app.log.warning(
                    "There was an error creating the show, no root directory setting found")
                return

    def manageNewShow(self, show):
        sickrage.app.log.debug(
            "Checking if trakt watch list wants to search for episodes from new show " + show.name)
        episodes = [i for i in self.todoWanted if i[0] == show.indexerid]

        for episode in episodes:
            self.todoWanted.remove(episode)
            setEpisodeToWanted(show, episode[1], episode[2])

    def _checkInList(self, trakt_id, showid, season, episode, List=None):
        """
         Check in the Watchlist or CollectionList for Show
         Is the Show, Season and Episode in the trakt_id list (tvdb / tvrage)
        """
        if "Collection" == List:
            try:
                if self.Collectionlist[trakt_id, showid].seasons[int(season)].episodes[int(episode)]: return True
            except Exception:
                return False
        elif "Show" == List:
            try:
                if self.ShowWatchlist[trakt_id, showid]: return True
            except Exception:
                return False
        else:
            try:
                if self.EpisodeWatchlist[trakt_id, showid].seasons[int(season)].episodes[int(episode)]: return True
            except Exception:
                return False

    def _getShowWatchlist(self):
        """
        Get Watchlist and parse once into addressable structure
        """
        try:
            sickrage.app.log.debug("Getting Show Watchlist")
            self.ShowWatchlist = srTraktAPI()["sync/watchlist"].shows() or {}
        except Exception as e:
            sickrage.app.log.warning(
                "Could not connect to trakt service, cannot download Show Watchlist: %s" % repr(e))
            return False
        return True

    def _getEpisodeWatchlist(self):
        """
         Get Watchlist and parse once into addressable structure
        """
        try:
            sickrage.app.log.debug("Getting Episode Watchlist")
            self.EpisodeWatchlist = srTraktAPI()["sync/watchlist"].episodes() or {}
        except Exception as e:
            sickrage.app.log.warning(
                "Could not connect to trakt service, cannot download Episode Watchlist: %s" % repr(e))
            return False

        return True

    def _getShowCollection(self):
        """
        Get Collection and parse once into addressable structure
        """
        try:
            sickrage.app.log.debug("Getting Show Collection")
            self.Collectionlist = srTraktAPI()["sync/collection"].shows() or {}
        except Exception as e:
            sickrage.app.log.warning(
                "Could not connect to trakt service, cannot download Show Collection: %s" % repr(e))
            return False

        return True

    @staticmethod
    def trakt_bulk_data_generate(data):
        """
        Build the JSON structure to send back to Trakt
        """
        show_list = []

        shows = {}
        seasons = {}

        for indexerid, indexer, show_name, startyear, season, episode in data:
            if indexerid not in shows:
                shows[indexerid] = {'title': show_name,
                                    'year': startyear,
                                    'ids': {IndexerApi(indexer).trakt_id: indexerid}}

            if indexerid not in seasons:
                seasons[indexerid] = {}
            if season not in seasons[indexerid]:
                seasons[indexerid] = {season: []}
            if episode not in seasons[indexerid][season]:
                seasons[indexerid][season] += [{'number': episode}]

        for indexerid, seasonlist in seasons.items():
            if 'seasons' not in shows[indexerid]: shows[indexerid]['seasons'] = []
            for season, episodelist in seasonlist.items():
                shows[indexerid]['seasons'] += [{'number': season, 'episodes': episodelist}]

            show_list.append(shows[indexerid])

        return {'shows': show_list}
