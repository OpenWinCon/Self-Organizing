#!/usr/bin/python3

#import MySQLdb
import pymysql

from os import system
import os

import mac_addr_get
#import ip_addr_get

hostapd_file	= open("/etc/hostapd/hostapd.conf","r")
hostapd_line	= hostapd_file.readlines()
hostapd_file.close()

DB_ip	= "172.31.1.19"				###### Have to address modify!!
id_mac  = mac_addr_get.mac.replace(":","")
id_mac	= "AP_" + id_mac
#id_ip	= ip_addr_get.ip[-3:]

conn	= pymysql.connect(DB_ip,"AP","","confdb")
curs	= conn.cursor()
sql1	= "select * from confdb."
sql	= sql1 + id_mac
curs.execute(sql)
conf_data	= curs.fetchall()

n_ch	= conf_data[0][0]		# config channel
n_ch	= str(n_ch)				# int -> str
c_ch	= hostapd_line[5][8:-1]		# current channel
config	= conf_data[0][2]		# configuration before and after
#print (conf_data)
print (n_ch,c_ch,config)

conf1	= "sudo sed -i 's/channel="
conf2	= "/channel="
conf3	= "/g' /etc/hostapd/hostapd.conf"

if config != 0:
	if c_ch != n_ch:
		ch_conf = conf1 + c_ch + conf2 + n_ch + conf3
		system(ch_conf)
		system("sudo killall hostapd")
		system("./auto_start_AP.py")
	else:
		print ("c_ch = n_ch")

	# conf <- 0
	sql1	= "update "
	sql2	= " set conf = 0 "
	sql3	= "where conf = 1"
	sql	= sql1 + id_mac + sql2 + sql3
	curs.execute(sql)
	conn.commit()
	print ("channel = " + c_ch)
conn.close()
