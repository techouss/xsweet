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

import os
import threading 

from twisted.python import log

LOGFILE = 'attempts.txt'
LOGFILE_LOCK = threading.Lock()

def writetosession(ip,message):
        LOGFILE_LOCK.acquire()
        originaldirectory = str(os.getcwd())
        directory = originaldirectory +"/victims"
        newfile = directory+"/victim-"+ip+".txt"
        f = open(newfile,'a')
        f.write(message)
        f.close()
        LOGFILE_LOCK.release()    

def normalwrite(file,message):
        LOGFILE_LOCK.acquire()
        originaldirectory = str(os.getcwd())
        directory = originaldirectory +"/victims"
        newfile = directory +"/" +file
        f = open(newfile,'a')
        f.write(message)
        f.close()
        LOGFILE_LOCK.release()  

def start_logging():
        originaldirectory = str(os.getcwd())
        newfile = originaldirectory + "/xsweet.log"
        log.startLogging(open(newfile, 'a'))
