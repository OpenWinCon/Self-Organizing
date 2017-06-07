#!/usr/bin/python3

from os import system
import os

import Ch_conf_check

while 1:
	if Ch_conf_check.config == 0:
		system("./Ch_conf.py")
		system("sleep 12")
	elif Ch_conf_check.config == 1:
		system("./del_netdb.py")
