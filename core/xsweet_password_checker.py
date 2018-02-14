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

from datetime import datetime
import tzlocal

from twisted.cred import checkers, credentials
from twisted.internet import defer
from zope.interface import implements
from twisted.conch import error

from core.xsweet_logging import *

class HoneypotPasswordChecker:
    implements(checkers.ICredentialsChecker)

    credentialInterfaces = {credentials.IUsernamePassword}

    def requestAvatarId(self, credentials):
	now = datetime.now(tzlocal.get_localzone())
        attempts =str(now)+ " " +credentials.username+":"+credentials.password+"\n"
        normalwrite(LOGFILE,attempts)
        if self.checkUserPass(credentials.username, credentials.password):
            return defer.succeed(credentials.username)
        else:
            return defer.fail(error.UnauthorizedLogin())
        return defer.fail(error.UnhandledCredentials())


    def checkUserPass(self, username, password):
        filepath = 'list.txt'  
        with open(filepath) as fp:  
            line = fp.readline().strip("\n")
            while line:
                user, passw = line.split(":")
                if user==username and passw == password:
                    return True
                line = fp.readline().strip("\n")
        return False
