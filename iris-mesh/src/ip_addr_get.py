#!/usr/bin/python3

from os import system
import os

system("ifconfig eth0 |awk '/inet addr/{print substr($2,6)}' >ip.out 2>&1")
ip_file = open("./ip.out","r")
ip_line = ip_file.readlines()
ip = ip_line[0][-4:-1]
#id_ip = ip[-3:]
#print (id_ip)
