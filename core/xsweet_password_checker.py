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
        if username=="william" and password == "william":
            return True
	elif username == "root" and password == "root":
	    return True
        else:
            return False
