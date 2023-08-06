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

import socket
from httplib import HTTPException, HTTPSConnection
from ssl import SSLError
from urllib import urlencode

import sickrage
from sickrage.notifiers import Notifiers


class PushalotNotifier(Notifiers):
    def __init__(self):
        super(PushalotNotifier, self).__init__()
        self.name = 'pushalot'

    def test_notify(self, pushalot_authorizationtoken):
        return self._sendPushalot(pushalot_authorizationtoken, event="Test",
                                  message="Testing Pushalot settings from SiCKRAGE", force=True)

    def notify_snatch(self, ep_name):
        if sickrage.app.config.pushalot_notify_onsnatch:
            self._sendPushalot(pushalot_authorizationtoken=sickrage.app.config.pushalot_authorizationtoken,
                               event=self.notifyStrings[self.NOTIFY_SNATCH],
                               message=ep_name)

    def notify_download(self, ep_name):
        if sickrage.app.config.pushalot_notify_ondownload:
            self._sendPushalot(pushalot_authorizationtoken=sickrage.app.config.pushalot_authorizationtoken,
                               event=self.notifyStrings[self.NOTIFY_DOWNLOAD],
                               message=ep_name)

    def notify_subtitle_download(self, ep_name, lang):
        if sickrage.app.config.pushalot_notify_onsubtitledownload:
            self._sendPushalot(pushalot_authorizationtoken=sickrage.app.config.pushalot_authorizationtoken,
                               event=self.notifyStrings[self.NOTIFY_SUBTITLE_DOWNLOAD],
                               message=ep_name + ": " + lang)

    def notify_version_update(self, new_version="??"):
        if sickrage.app.config.use_pushalot:
            update_text = self.notifyStrings[self.NOTIFY_GIT_UPDATE_TEXT]
            title = self.notifyStrings[self.NOTIFY_GIT_UPDATE]
            self._sendPushalot(pushalot_authorizationtoken=sickrage.app.config.pushalot_authorizationtoken,
                               event=title,
                               message=update_text + new_version)

    def _sendPushalot(self, pushalot_authorizationtoken=None, event=None, message=None, force=False):

        if not sickrage.app.config.use_pushalot and not force:
            return False

        sickrage.app.log.debug("Pushalot event: " + event)
        sickrage.app.log.debug("Pushalot message: " + message)
        sickrage.app.log.debug("Pushalot api: " + pushalot_authorizationtoken)

        http_handler = HTTPSConnection("pushalot.com")

        data = {'AuthorizationToken': pushalot_authorizationtoken,
                'Title': event.encode('utf-8'),
                'Body': message.encode('utf-8')}

        try:
            http_handler.request("POST",
                                 "/api/sendmessage",
                                 headers={'Content-type': "application/x-www-form-urlencoded"},
                                 body=urlencode(data))
        except (SSLError, HTTPException, socket.error):
            sickrage.app.log.error("Pushalot notification failed.")
            return False
        response = http_handler.getresponse()
        request_status = response.status

        if request_status == 200:
            sickrage.app.log.debug("Pushalot notifications sent.")
            return True
        elif request_status == 410:
            sickrage.app.log.error("Pushalot auth failed: %s" % response.reason)
            return False
        else:
            sickrage.app.log.error("Pushalot notification failed.")
            return False
