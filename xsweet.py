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
from twisted.conch.ssh import factory, keys
from twisted.cred import portal
import os
#from twisted.python import log
#import sys
from twisted.python import components

from core.xsweet_password_checker import *
from core.xsweet_realm import *
from core.xsweet_session import *
from core.xsweet_logging import *
#log.startLogging(sys.stderr)

##FIXME: do the ssh-keygen in docker and remove this method
def getRSAKeys():

    if not (os.path.exists('public.key') and os.path.exists('private.key')):
        # generate a RSA keypair
        print "Generating RSA keypair..."
        from Crypto.PublicKey import RSA
        KEY_LENGTH = 1024
        rsaKey = RSA.generate(KEY_LENGTH, common.entropy.get_bytes)
        publicKeyString = keys.makePublicKeyString(rsaKey)
        privateKeyString = keys.makePrivateKeyString(rsaKey)
        # save keys for next time
        file('public.key', 'w+b').write(publicKeyString)
        file('private.key', 'w+b').write(privateKeyString)
        print "done."
    else:
        publicKeyString = file('public.key').read()
        privateKeyString = file('private.key').read()
    return publicKeyString, privateKeyString

if __name__ == "__main__":
    start_logging()
    components.registerAdapter(XsweetSession, SSHAvatar, session.ISession)
    sshFactory = factory.SSHFactory()
    sshFactory.portal = portal.Portal(SSHRealm())
    sshFactory.portal.registerChecker(HoneypotPasswordChecker())
    pubKeyString, privKeyString = getRSAKeys()

    sshFactory.publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=pubKeyString)}
    sshFactory.privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=privKeyString)}

    from twisted.internet import reactor
    reactor.listenTCP(2222, sshFactory)
    reactor.run()

