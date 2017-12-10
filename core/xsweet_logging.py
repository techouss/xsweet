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
