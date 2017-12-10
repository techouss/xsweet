#!/usr/bin/env python

from zope.interface import implements
from twisted.cred import portal

from core.xsweet_avatar import *

class SSHRealm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
	return interfaces[0], SSHAvatar(avatarId), lambda: None
