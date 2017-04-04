#!/usr/bin/python

import MySQLdb
import pymysql

from os import system
import os

system("ifconfig -a | grep ^eth >mac.out 2>&1")
mac_file = open("./mac.out","r")
mac_line = mac_file.readlines()
mac = mac_line[0][-20:-3]
#print (mac)
