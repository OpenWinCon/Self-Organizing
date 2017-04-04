#!/usr/bin/python

import MySQLdb
import pymysql

from os import system
import os

system("ifconfig br0 |awk '/inet addr/{print substr($2,6)}' >ip.out 2>&1")
ip_file = open("./ip.out","r")
ip_line = ip_file.readlines()
ip = ip_line[0][:-1]
#print (ip)
