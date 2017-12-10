#!/usr/bin/env python

from twisted.conch.ssh import session

from core.xsweet_protocol import *

class XsweetSession:

    def __init__(self, avatar):
	"test"

    def openShell(self, protocol):
        serverProtocol = XSWEETProtocol() 
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, terminal, windowSize, attrs):
        return None

    def execCommand(self, protocol, cmd):
        raise NotImplementedError

    def closed(self):
        pass
