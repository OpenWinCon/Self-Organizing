#!/usr/bin/python3

from os import system
import os

# AP scan & catch infromation
system("sudo iw dev wlan1 scan ap-force | egrep '^BSS|SSID|: channel |signal' >AP_info.out 2>&1")
AP_info_file = open("AP_info.out","r")
AP_info_line = AP_info_file.readlines()

#Num_AP = len(AP_info_line) // 4

j = 0
AP_trim_line = []
for i in range(0,len(AP_info_line)):
#	k = AP_info_line[i].find('API')
	k = AP_info_line[i].find('goth_')

	if k != -1:
		AP_info_line[j*4]	= AP_info_line[i - 2].replace(":","")[4:-11]	# MAC
		AP_info_line[j*4+1]	= AP_info_line[i - 1][9:-5]			# dB
		AP_info_line[j*4+2]	= AP_info_line[i][7:-1]				# SSID
		AP_info_line[j*4+3]	= AP_info_line[i + 1][27:-1]			# CH
		j = j + 1

AP_info_file.close()

AP_trim_file = open("AP_trim.out","w")
for i in range(0, j*4):
	AP_trim_file.write(AP_info_line[i])
	AP_trim_file.write("\n")
AP_trim_file.close()

#print (AP_info_line)
#print (AP_info_line[0])
#print (AP_info_line[1])
#print (AP_info_line[2])
#print (AP_info_line[3])

#AP_n = len(AP_info_line) // 3	# Number of APs
#print(AP_n)
