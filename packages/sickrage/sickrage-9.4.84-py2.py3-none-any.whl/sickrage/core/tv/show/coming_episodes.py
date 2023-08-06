# This file is part of SickRage.
#
# URL: https://www.sickrage.ca
# Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
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

import sickrage
from sickrage.core.common import Quality, get_quality_string, WANTED, UNAIRED, timeFormat, dateFormat
from sickrage.core.helpers.srdatetime import srDateTime


class ComingEpisodes:
    """
    Missed:   yesterday...(less than 1 week)
    Today:    today
    Soon:     tomorrow till next week
    Later:    later than next week
    """
    categories = ['later', 'missed', 'soon', 'today']
    sorts = {
        'date': (lambda a, b: cmp(a['localtime'], b['localtime'])),
        'network': (lambda a, b: cmp((a['network'], a['localtime']), (b['network'], b['localtime']))),
        'show': (lambda a, b: cmp((a['show_name'], a['localtime']), (b['show_name'], b['localtime']))),
    }

    def __init__(self):
        pass

    @staticmethod
    def get_coming_episodes(categories, sort, group, paused=False):
        """
        :param categories: The categories of coming episodes. See ``ComingEpisodes.categories``
        :param sort: The sort to apply to the coming episodes. See ``ComingEpisodes.sorts``
        :param group: ``True`` to group the coming episodes by category, ``False`` otherwise
        :param paused: ``True`` to include paused shows, ``False`` otherwise
        :return: The list of coming episodes
        """

        def result(show, episode):
            return [{
                'airdate': episode['airdate'],
                'airs': show.airs,
                'description': episode['description'],
                'episode': episode['episode'],
                'imdb_id': show.imdbid,
                'indexer': episode['indexer'],
                'indexer_id': show.indexerid,
                'name': episode['name'],
                'network': show.network,
                'paused': show.paused,
                'quality': show.quality,
                'runtime': show.runtime,
                'season': episode['season'],
                'show_name': show.name,
                'showid': episode['showid'],
                'status': show.status
            }]

        paused = sickrage.app.config.coming_eps_display_paused or paused

        if not isinstance(categories, list):
            categories = categories.split('|')

        if sort not in ComingEpisodes.sorts.keys():
            sort = 'date'

        today = datetime.date.today().toordinal()
        next_week = (datetime.date.today() + datetime.timedelta(days=7)).toordinal()

        recently = (
                datetime.date.today() - datetime.timedelta(
            days=sickrage.app.config.coming_eps_missed_range)).toordinal()

        qualities_list = Quality.DOWNLOADED + \
                         Quality.SNATCHED + \
                         Quality.SNATCHED_BEST + \
                         Quality.SNATCHED_PROPER + \
                         Quality.ARCHIVED + \
                         Quality.IGNORED

        results = []
        for s in sickrage.app.showlist:
            for e in sickrage.app.main_db.get_many('tv_episodes', s.indexerid):
                if e['season'] != 0 and today <= e['airdate'] < next_week and e['status'] not in qualities_list:
                    results += result(s, e)

                if e['season'] != 0 and e['showid'] not in [int(r['showid']) for r in results] \
                        and e['airdate'] >= next_week and e['status'] \
                        not in Quality.DOWNLOADED + Quality.SNATCHED + Quality.SNATCHED_BEST + Quality.SNATCHED_PROPER:
                    results += result(s, e)

                if e['season'] != 0 and today > e['airdate'] >= recently \
                        and e['status'] in [WANTED, UNAIRED] and e['status'] not in qualities_list:
                    results += result(s, e)

        for index, item in enumerate(results):
            results[index]['localtime'] = srDateTime(
                sickrage.app.tz_updater.parse_date_time(item['airdate'], item['airs'], item['network']),
                convert=True).dt

        results.sort(ComingEpisodes.sorts[sort])

        if not group:
            return results

        grouped_results = {category: [] for category in categories}

        for result in results:
            if result['paused'] and not paused:
                continue

            result['airs'] = str(result['airs']).replace('am', ' AM').replace('pm', ' PM').replace('  ', ' ')
            result['airdate'] = result['localtime'].toordinal()

            if result['airdate'] < today:
                category = 'missed'
            elif result['airdate'] >= next_week:
                category = 'later'
            elif result['airdate'] == today:
                category = 'today'
            else:
                category = 'soon'

            if len(categories) > 0 and category not in categories:
                continue

            if not result['network']:
                result['network'] = ''

            result['quality'] = get_quality_string(result['quality'])
            result['airs'] = srDateTime(result['localtime']).srftime(t_preset=timeFormat).lstrip('0').replace(' 0', ' ')
            result['weekday'] = 1 + datetime.date.fromordinal(result['airdate']).weekday()
            result['tvdbid'] = result['indexer_id']
            result['airdate'] = srDateTime(result['localtime']).srfdate(d_preset=dateFormat)
            result['localtime'] = result['localtime'].toordinal()

            grouped_results[category].append(result)

        return grouped_results
