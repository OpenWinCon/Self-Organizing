#!/usr/bin/python3

from os import system
import os

#import MySQLdb
import pymysql

	# Open DB connect
DB_ip	= "172.31.1.19"				###### Have to address modify!!
#id_ip	= ip_addr_get.ip
conn	= pymysql.connect(DB_ip,"Controller","","confdb")
curs	= conn.cursor()

sql	= "show tables"
curs.execute(sql)
rows	= curs.fetchall()
AP_N	= len(rows)

APs	= []
for i in range(0, len(rows)):
	APs.append(rows[i][0])

config	= 0
for AP in APs:
	sql1	= "select conf from " + AP + ""
	curs.execute(sql1)
	conf	= curs.fetchall()
	print (conf[0][0])
	config	= config + conf[0][0]

conn.close()
