# Xsweet

## Introduction

Xsweet is a medium interaction SSH honeypot which is based on kojoney2, but way different. Xsweet is written in python using python twisted conch. Xsweet uses its own twisted Conch SSH protocol with the goal to log brute force attacks including username and password successful and failed attempts, collect session command logs, intelligence of the methods and motives of the attacker targeting your servers and the location of the IP that we are receiving the attack from.

Xsweet simulates a real SSH environment and a real shell environment. Xsweet will listen on port 2222 but to make it accessible by the attackers, we will use iptables to route attacker's SSH connection to 22. When an attacker tries to connect to our servers, our honeypotwill be ready for them. It will authenticate users by comparing fake usernames and passwords that are mostly used by SSH brute forcing lists so that the attackers get trapped easily in our honeypot with a simulated shell. After the attackers gets access to the fake system, he can issuecommands that will be logged completely. Xsweet fake system responds to these commands with fake strings that looks completely legitimate to the attacker that he won’t notice he is in a fakesystem.

What we mean by medium interaction SSH honeypot is that when an attacker uses curl or wget command to download viruses on our system, Xsweet will actually download the files to a safely locked directory outside our honeypotthat will later be examined by system administrators and analysists to determine what was the motive of this specific hacker; but these viruses won’t appear in the fake system and the hacker won’t be able to actually see or interact with these files or viruses. The honeypot will give the attacker error that the files can’t be downloaded due to a specific reason.


## Motives and Purpose

After I rented some cloud servers online to test my projects on them,  I  saw a honeypot  that logs only the username and password that the attacker is using to brute force systems.  So, I  thought that it would be nice if I deployed it on my server and checked if someone is trying to hack me. After 1 minute of deploying it on the rented server, I started getting massive hits trying to guess the username and password combination of my server to get access. I contacted the support of my server and they told me that such cloud servers are brute forced 24/7 by attackers because they are exposed to external network. Therefore, from here I decided to create my own honeypot that not only logs username and password combination but also gives attackers access to a fake file system to study the behavior of real dangerous attackers after they compromise a system to use it for investigation and defense in case of a legitimate SSH servers.


## Features

- Used Logstash, Elasticsearch and Kibana to search and visualize the logged data in a neat way.
- Fake filesystem with the ability to add/remove files. A full fake filesystem resembling an Ubuntu 16.04 installation is included.
- Possibility of adding fake file contents so the attacker can cat files such as /etc/passwd. Only minimal file contents are included.
- Attempts and Session logs stored with UTC timing Compatible format for easy viewing globally

## Installation

- You need first to install all the dependencies and utilities mentioned below in the Requirements section.
- Clone the repository `git clone https://github.com/techouss/xsweet.git` and navigate to the direcotry `cd xsweet`
- Strat xsweet `python xsweet.py &`
- To run it on port 22 because it is by default on port 2222
`sudo iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2222`

## Requirements

```
sudo apt-get install python-minimal
sudo apt-get install python-pip
sudo apt-get install build-essential
sudo apt-get install default-jre
sudo pip install --upgrade pip
sudo pip install setuptools 
sudo pip install pyasn1 pyasn1-modules
sudo pip install virtualenv
sudo pip install pycrypto
sudo pip install virtualenv
sudo pip install twisted
sudo pip install cryptography
sudo pip install tzlocal
```

**You dont need these requirements if you choose to install with Docker**


## Docker

Xsweet uses Docker to be deployed, Configured, and installed on any machine whether its  Linux , Mac, Windows... with one simple command . I created an Ubuntu image with docker, containing the honeypot and all its visualization applications needed  (Elasticsearch,  Logstash and  Kibana) and the configuration files needed to run the whole  system on your machine without any errors while installing , due to different OS systems or some python  utilities or dependencies not being installed on your machine. Just Run This command and you are good to go without downloading anything:

`sudo docker run -p 22:2222 ousamaag/docker-xsweet`

**Note: Make sure you  don’t have any SSH servers running on your system or the app won’t work because it also runs on port 22.**



## Files of interest

**All the attacker’s interaction with the honeypot whether he got access or not is logged in three files:**

- `attempts.txt`: stores the (username:password) combination attempts with the timing.
- `victim-ActualIPofTheAttacker.txt`(Example: victim-10.10.10.10.txt): is the file where the executed commands of the attacker are logged after gaining access to the honeypot.
- `xsweet.log`: the file where the IP of the attacker and the key exchage is logged.

**If you downloaded Xsweet with Docker, you'll get it automatically configured with Kibana, Logstash and Elastic Search.**

When we collect all these log files, Logstash takes them as input and parses and extracts key words such as username, password, IP,and timing from these logs. Logstash then sends these keywords to elastic search. Elasticsearch stores them and sends them to Kibana to be viewed in charts and graphs according to these keywords.

![files on interest](https://image.ibb.co/jco937/xsweet_image.png "ELK")

## Overall System

An attacker tries to compromise our system with SSH bruteforcing, whether he connects or not everything is logged, if he gains access,the commands used inside the session are logged. After everything is logged, these log files are fetched to Logstash. Logstash takes care of them as mentioned in the previous model routing.

![Overall Xsweet system](https://image.ibb.co/mho937/xsweet_image2.png "ELK")

## End Result Dashboard in Kibana 

![Dashboard](https://image.ibb.co/gBTDJ7/dashboard1.png "ELK")

![Dashboard](https://image.ibb.co/f8CvWS/dashboard2.png "ELK")

## Video Demo

[![xsweet demo youtube video](https://image.ibb.co/jWgVWS/video_demo.png)](https://www.youtube.com/watch?v=SGwpJwFwJ-A)



