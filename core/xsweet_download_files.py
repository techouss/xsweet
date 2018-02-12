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


import urllib, os, random

from core.xsweet_logging import *

def get_good_filename(filename):

#ceated this method because our program may not differenciate between the of the / in the URL and the / in the directories"
    
    buf = ""
    
    for c in filename:
        if c.isalnum():
            buf += c
        else:
            buf += "_"
    
    return buf 

def download_file(url, ip):
    message =  "[*] Attempting download of " + url+"\n"
    writetosession(ip,message)
    try:
        if url.find("://") == -1:
            url = "http://" + url
        data = urllib.urlopen(url)
        data = data.read()
        originaldirectory = str(os.getcwd())
        directory = originaldirectory +"/downloads/"
        filename = get_good_filename(url) +"_" + ip
        f = open (directory + filename, "wb")
        f.write(data)
        f.close()
        message = "[*] Downloaded successfully file: "+ filename+"\n"
        writetosession(ip,message)
    except:
        message = "[*] Error downloading file "+url+" request by attacker."
        writetosession(ip,message)


def wget(params, ip):
    data = ""
    if len(params) == 0:
        data  = "wget: You need to specify the URL\r\n"
        data +="\r\n"
        data +="Usage: wget [OPTIONS] [URL]\r\n"
        data +="\r\n"
        data +="Use wget --help to read the complete option list.\r\n"
    for param in params:
        if not param.startswith("-"):
            download_file(param, ip)
            
            data = "Downloading URL " + str(' '.join(params))
            data += "\r\nwget: Unknown error"
    return data

def curl(params, ip):
    data = ""
    if len(params) == 0:
        data  = "curl: try 'curl --help' or 'curl --manual' for more information\r\n"
    for param in params:
        if not param.startswith("-"):
            download_file(param, ip)

            data = "Downloading URL " + str(' '.join(params))
            return data + "\r\ncurl: Unknown error"
    return data
