#!/usr/bin/python

from os import system
import os

# AP scan & catch infromation
system("iw dev wlan0 scan ap-force | egrep '^BSS|SSID|: channel |signal' >AP_info.out 2>&1")
AP_info_file = open("AP_info.out","r")
AP_info_line = AP_info_file.readlines()

Num_AP = len(AP_info_line) // 4

for i in range(0,Num_AP):
	AP_info_line[i*4 + 0] = AP_info_line[i*4 + 0].replace(":","")[4:-11]	# MAC
	AP_info_line[i*4 + 1] = AP_info_line[i*4 + 1][9:-5]			# dB
	AP_info_line[i*4 + 2] = AP_info_line[i*4 + 2][7:-1]			# SSID
	AP_info_line[i*4 + 3] = AP_info_line[i*4 + 3][27:-1]			# CH

AP_info_file.close()

AP_trim_file = open("AP_trim.out","w")
for i in range(0, len(AP_info_line)):
	AP_trim_file.write(AP_info_line[i])
	AP_trim_file.write("\n")
AP_trim_file.close()
