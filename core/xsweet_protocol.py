#!/usr/bin/env python

from twisted.internet import protocol
import datetime
import string
import re

from conf.fake_responses import *
from core.xsweet_process_cmd import *
from core.xsweet_logging import *
from conf.process_command import *


class XSWEETProtocol(protocol.Protocol):
    lastCmd = ""
    fake_workingdir = "/"
	
    def connectionMade(self): 
        pt = self.transport.session.conn.transport
        ip = pt.transport.getPeer().host
        message =  "got connection from "+ip+" at "+str(datetime.now())+"\n"
        writetosession(ip,message)
        global FAKE_CWD, FAKE_HOMEDIRS
        self.fake_username = self.transport.session.avatar.username  
        if self.fake_username in FAKE_HOMEDIRS:
            self.fake_workingdir = FAKE_HOMEDIRS[self.fake_username]
        else:
            FAKE_CWD = "/"
	self.transport.write("Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-97-generic x86_64)\r\n\n" 
 +" * Documentation:  https://help.ubuntu.com\r\n"
 +" * Management:     https://landscape.canonical.com\r\n"
 +" * Support:        https://ubuntu.com/advantage\r\n\n"
 +"72 packages can be updated.\r\n"
 +"34 updates are security updates.\r\n\n\n"
 +"Last login: Sun Oct 22 09:36:20 2017 from 59.45.175.11\r\n")
        self.showPrompt()

    def showPrompt(self):
	if self.transport.session.avatar.username=="root":
        	self.transport.write("root@ubuntu:/# ")
        else:
        	self.transport.write(self.transport.session.avatar.username+"@ubuntu:~$ ")

    def dataReceived(self, data):
        global FAKE_CWD, USE_DB
        if data == '\r':
            self.lastCmd = string.replace(self.lastCmd, '\r', '')
            self.lastCmd = string.replace(self.lastCmd, '\n', '')
            ip = self.transport.session.conn.transport.transport.getPeer().host
            # "Execute" the command(s)
            # handle multiple commands delimited by semi-colons
            if (len(self.lastCmd.split(';')) > 1):
                for command in self.lastCmd.split(';'):
                    retvalue = process_command(command,
                                          self.transport, 
                                          self.fake_username, 
                                          ip,  
                                          self.fake_workingdir)
                    (printlinebreak, self.fake_workingdir, self.fake_username) = retvalue
            else:
                retvalue = process_command(self.lastCmd,
                                      self.transport, 
                                      self.fake_username, 
                                      ip, 
                                      self.fake_workingdir)
                (printlinebreak, self.fake_workingdir, self.fake_username) = retvalue
                
            self.lastCmd = ""
	    ##prompting the proper form in ubuntu 
            if self.transport.session.avatar.username=="root" and self.fake_workingdir=='/root':
                FAKE_PROMPT = "root@ubuntu:~# "
            elif self.transport.session.avatar.username=="root" and self.fake_workingdir=='/':
                FAKE_PROMPT = "root@ubuntu:/# "
            elif self.fake_workingdir=='/home/'+self.transport.session.avatar.username:
            	FAKE_PROMPT = self.transport.session.avatar.username+"@ubuntu:~$ "
            elif '/home/'+self.transport.session.avatar.username in self.fake_workingdir:
            	regex = re.search(r"/home/.*/(.*)",self.fake_workingdir)
            	FAKE_PROMPT = self.transport.session.avatar.username+"@ubuntu:~/"+regex.group(1)+"$ "
            elif self.transport.session.avatar.username=="root":
                FAKE_PROMPT = "root@ubuntu:~"+self.fake_workingdir+"# "
            else:
            	FAKE_PROMPT = self.transport.session.avatar.username+"@ubuntu:"+self.fake_workingdir+"$ "

            if printlinebreak == 1:
                data = '\r\n'
            
            data += str(FAKE_PROMPT)
        elif data == '\x03': #^C
            try:
                self.transport.loseConnection()
            finally:
                return
        elif data == '\x7F':
            if len(self.lastCmd) > 0:
                self.lastCmd = self.lastCmd[0:len(self.lastCmd) - 1]
                self.transport.write("\x1B\x5B\x44 \x1B\x5B\x44 \x1B\x5B\x44");
            return
        elif data == "\x1B\x5B\x41":
            #ignore up arrow
            return
        elif data == "\x1B\x5B\x42":
            #ignore down arrow
            return
        elif data == "\x1B\x5B\x43":
            #ignore right arrow
            return
        elif data == "\x1B\x5B\x44":
            #ignore left arrow
            return
        else:
            self.lastCmd += data
	self.transport.write(data)
