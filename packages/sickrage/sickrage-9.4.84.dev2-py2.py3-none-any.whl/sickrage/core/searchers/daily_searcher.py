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

import datetime
import threading

import sickrage
from sickrage.core.common import Quality, WANTED, DOWNLOADED, SNATCHED, SNATCHED_PROPER
from sickrage.core.queues.search import DailySearchQueueItem
from sickrage.core.searchers import new_episode_finder


class DailySearcher(object):
    def __init__(self):
        self.name = "DAILYSEARCHER"
        self.lock = threading.Lock()
        self.amActive = False

    def run(self, force=False):
        """
        Runs the daily searcher, queuing selected episodes for search
        :param force: Force search
        """
        if self.amActive or sickrage.app.developer and not force:
            return

        self.amActive = True

        # set thread name
        threading.currentThread().setName(self.name)

        # find new released episodes and update their statuses
        new_episode_finder()

        for curShow in sickrage.app.showlist:
            if curShow.paused:
                sickrage.app.log.debug("Skipping search for {} because the show is paused".format(curShow.name))
                continue

            segments = self._get_segments(curShow, datetime.date.today())
            if segments:
                sickrage.app.search_queue.put(DailySearchQueueItem(curShow, segments))
            else:
                sickrage.app.log.debug("Nothing needs to be downloaded for {}, skipping".format(curShow.name))

        self.amActive = False

    @staticmethod
    def _get_segments(show, fromDate):
        """
        Get a list of episodes that we want to download
        :param show: Show these episodes are from
        :param fromDate: Search from a certain date
        :return: list of wanted episodes
        """

        wanted = []

        anyQualities, bestQualities = Quality.splitQuality(show.quality)
        allQualities = list(set(anyQualities + bestQualities))

        sickrage.app.log.debug("Seeing if we need anything from {}".format(show.name))

        # check through the list of statuses to see if we want any
        for dbData in sickrage.app.main_db.get_many('tv_episodes', show.indexerid):
            if dbData['season'] > 0 and dbData['airdate'] >= fromDate.toordinal():
                curStatus, curQuality = Quality.splitCompositeStatus(int(dbData["status"] or -1))

                # if we need a better one then say yes
                if curStatus not in (WANTED, DOWNLOADED, SNATCHED, SNATCHED_PROPER):
                    continue

                if curStatus != WANTED:
                    if bestQualities:
                        if curQuality in bestQualities:
                            continue
                        elif curQuality != Quality.UNKNOWN and curQuality > max(bestQualities):
                            continue
                    else:
                        if curQuality in anyQualities:
                            continue
                        elif curQuality != Quality.UNKNOWN and curQuality > max(anyQualities):
                            continue

                # skip upgrading quality of downloaded episodes if enabled
                if curStatus == DOWNLOADED and show.skip_downloaded:
                    continue

                epObj = show.get_episode(int(dbData["season"]), int(dbData["episode"]))
                epObj.wantedQuality = [i for i in allQualities if (i > curQuality and i != Quality.UNKNOWN)]
                wanted.append(epObj)

        return wanted
