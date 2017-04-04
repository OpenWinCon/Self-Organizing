#!/usr/bin/python

import MySQLdb
import pymysql

#import AP_addr_get
import ip_addr_get				# AP own ip
import mac_addr_get				# AP own MAC

from os import system
import os

##### start hostapd
##system("./auto_start_AP.py")							# Have to clear remark

##### get Address
##system("./AP_addr_get.py")			# around APs' MAC		# Have to clear remark
#system("./ip_addr_get.py")				# AP own ip
#system("./mac_addr_get.py")			# AP own MAC

##### comb AP's id
id_ip	= ip_addr_get.ip[-3:]			# extract "224" from "192.168.1.224"
id_mac	= mac_addr_get.mac.replace(":","")	# remove ":" from own mac_addr
id	= id_mac + id_ip

##### Open DB and create table
	# Open DB connection
DB_ip	= "192.168.1.224"			###### Have to address modify!!
conn	= pymysql.connect(DB_ip,"AP","","netdb")
curs	= conn.cursor()

##### Insert APs data to DB
AP_file	= open("AP_trim.out","r")
AP_list	= AP_file.readlines()
AP_N	= len(AP_list) // 4

# insert AP own's data				# delete this code at AP_agent
sql1	= "create table IF NOT EXISTS `"
table	= id_mac
ID	= "` (ID	varchar(20),"
state	= "state	int(1),"
ch	= "ch		int(2),"
dB	= "dB		int(100));"
sql	= sql1 + table + ID + state + ch + dB
curs.execute(sql)
conn.commit()

sql1	= "delete from "
sql2	= " where ID=%s"
sql	= sql1 + table + sql2
curs.execute(sql, id_mac)
conn.commit()

# insert APs data
for i in range(0, AP_N):

	scanned_APs_id = AP_list[4*i+0][:-1]		# address of scanned APs

	# create table
	sql1	= "create table IF NOT EXISTS `"
	table	= scanned_APs_id			######
	ID	= "` (ID	varchar(20),"
	state	= "state	int(1),"
	ch	= "ch	   int(2),"
	dB	= "dB	   int(100));"
	sql	= sql1 + table + ID + state + ch + dB
	curs.execute(sql)
	conn.commit()

for i in range(0, AP_N):

	scanned_APs_id = AP_list[4*i+0][:-1]				# address of scanned APs
	# Get APs data
	dB	= AP_list[4*i+1][:-1]
	SSID	= AP_list[4*i+2][:-1]
	ch	= AP_list[4*i+3][:-1]
	data	= (id_mac, 1, ch, dB)

##### delete DB
	sql1	= "delete from "
	sql2	= " where ID=%s"
	sql	= sql1 + scanned_APs_id + sql2
	curs.execute(sql, id_mac)
	conn.commit()

##### insert DB
	sql1	= "insert into "
	sql2	= "(ID,state,ch,dB) "
	sql3	= "values (%s, %s, %s, %s)"
	sql	= sql1 + scanned_APs_id + sql2 + sql3

	curs.execute(sql, data)
	conn.commit()
#end for

conn.close
