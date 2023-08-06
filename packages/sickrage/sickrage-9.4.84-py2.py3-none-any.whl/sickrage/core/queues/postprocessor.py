# Author: echel0n <echel0n@sickrage.ca>
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
from time import sleep

import sickrage
from sickrage.core.common import cpu_presets
from sickrage.core.process_tv import logHelper, processDir
from sickrage.core.queues import srQueue, srQueueItem, srQueuePriorities


class PostProcessorQueueActions(object):
    AUTO = 1
    MANUAL = 2

    actions = {
        AUTO: 'Auto',
        MANUAL: 'Manual',
    }


postprocessor_queue_lock = threading.Lock()


class PostProcessorQueue(srQueue):
    def __init__(self):
        srQueue.__init__(self, "POSTPROCESSORQUEUE")

    def find_in_queue(self, dirName, proc_type):
        """
        Finds any item in the queue with the given dirName and proc_type pair
        :param dirName: directory to be processed by the task
        :param proc_type: processing type, auto/manual
        :return: instance of PostProcessorItem or None
        """
        for __, __, cur_item in self.queue + [(None, None, self.current_item)]:
            if isinstance(cur_item,
                          PostProcessorItem) and cur_item.dirName == dirName and cur_item.proc_type == proc_type:
                return cur_item
        return None

    @property
    def is_in_progress(self):
        for __, __, cur_item in self.queue + [(None, None, self.current_item)]:
            if isinstance(cur_item, PostProcessorItem):
                return True
        return False

    @property
    def queue_length(self):
        """
        Returns a dict showing how many auto and manual tasks are in the queue
        :return: dict
        """
        length = {'auto': 0, 'manual': 0}

        for __, __, cur_item in self.queue + [(None, None, self.current_item)]:
            if isinstance(cur_item, PostProcessorItem):
                if cur_item.proc_type == 'auto':
                    length['auto'] += 1
                else:
                    length['manual'] += 1

        return length

    def put(self, dirName, nzbName=None, process_method=None, force=False, is_priority=None, delete_on=False,
            failed=False, proc_type="auto", force_next=False, **kwargs):
        """
        Adds an item to post-processing queue
        :param dirName: directory to process
        :param nzbName: release/nzb name if available
        :param process_method: processing method, copy/move/symlink/link
        :param force: force overwriting of existing files regardless of quality
        :param is_priority: whether to replace the file even if it exists at higher quality
        :param delete_on: delete files and folders after they are processed (always happens with move and auto combination)
        :param failed: mark downloads as failed if they fail to process
        :param proc_type: processing type: auto/manual
        :param force_next: wait until the current item in the queue is finished then process this item next
        :return: string indicating success or failure
        """

        if not dirName:
            return logHelper(
                "{} post-processing attempted but directory is not set: {}".format(proc_type.title(), dirName),
                sickrage.app.log.WARNING)

        if not os.path.isabs(dirName):
            return logHelper("{} post-processing attempted but directory is relative (and probably not what you "
                             "really want to process): {}".format(proc_type.title(), dirName),
                             sickrage.app.log.WARNING)

        if not delete_on:
            delete_on = (False, (not sickrage.app.config.no_delete, True)[process_method == "move"])[
                proc_type == "auto"]

        item = self.find_in_queue(dirName, proc_type)

        if item:
            if self.current_item == item:
                return logHelper("Directory {} is already being processed right now, please wait until it completes "
                                 "before trying again".format(dirName))

            item.__dict__.update(dict(dirName=dirName, nzbName=nzbName, process_method=process_method, force=force,
                                      is_priority=is_priority, delete_on=delete_on, failed=failed, proc_type=proc_type))

            message = logHelper(
                "An item with directory {} is already being processed in the queue, item updated".format(dirName))
            return message + "<br\><span class='hidden'>Processing succeeded</span>"
        else:
            super(PostProcessorQueue, self).put(
                PostProcessorItem(dirName, nzbName, process_method, force, is_priority, delete_on, failed, proc_type)
            )
            if force_next:
                return self._result_queue.get()
            else:
                message = logHelper(
                    "{} post-processing job for {} has been added to the queue".format(proc_type.title(), dirName)
                )
                return message + "<br\><span class='hidden'>Processing succeeded</span>"


class PostProcessorItem(srQueueItem):
    def __init__(self, dirName, nzbName=None, process_method=None, force=False, is_priority=None, delete_on=False,
                 failed=False, proc_type="auto"):
        action_id = (PostProcessorQueueActions.MANUAL, PostProcessorQueueActions.AUTO)[proc_type == "auto"]
        super(PostProcessorItem, self).__init__(PostProcessorQueueActions.actions[action_id], action_id)

        self.dirName = dirName
        self.nzbName = nzbName
        self.process_method = process_method
        self.force = force
        self.is_priority = is_priority
        self.delete_on = delete_on
        self.failed = failed
        self.proc_type = proc_type

        self.priority = (srQueuePriorities.HIGH, srQueuePriorities.NORMAL)[proc_type == 'auto']

    def run(self):
        """
        Runs the task
        :return: None
        """

        try:
            sickrage.app.log.info("Started {} post-processing job for: {}".format(self.proc_type, self.dirName))

            self.result = unicode(processDir(
                dirName=self.dirName,
                nzbName=self.nzbName,
                process_method=self.process_method,
                force=self.force,
                is_priority=self.is_priority,
                delete_on=self.delete_on,
                failed=self.failed,
                proc_type=self.proc_type
            ))

            sickrage.app.log.info("Finished {} post-processing job for: {}".format(self.proc_type, self.dirName))

            # give the CPU a break
            sleep(cpu_presets[sickrage.app.config.cpu_preset])
        except Exception:
            sickrage.app.log.debug(traceback.format_exc())
            self.result = '{}'.format(traceback.format_exc())
            self.result += 'Processing Failed'

        self.result_queue.put(self.result)
