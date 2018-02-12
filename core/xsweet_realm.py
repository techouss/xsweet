# Copyright (C) 2017 Ousama AbouGhoush <ousama.aboughoush@hotmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


#!/usr/bin/env python

from zope.interface import implements
from twisted.cred import portal

from core.xsweet_avatar import *

class SSHRealm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
	return interfaces[0], SSHAvatar(avatarId), lambda: None
