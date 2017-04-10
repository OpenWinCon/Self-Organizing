#!/usr/bin/python

import MySQLdb
import pymysql

from os import system
import os

import mac_addr_get.py
import ip_addr_get.py

hostapd_file	= open("/etc/hostapd/hostapd.conf","r")
hostapd_line	= hostapd_file.readlines()
hostapd_file.close()

DB_ip	= "192.168.1.224"				###### Have to address modify!!
#id_mac	= mac_addr_get.mac.replace(":","")
id_ip	= ip_addr_get.ip[-3:]

conn	= pymysql.connect(DB_ip,id_ip,"","confdb")
sql1	= "select ch from confdb."
sql	= sql1 + id_mac
curs.execute(sql)
conf_data	= curs.fetchall()

n_ch	= conf_data[0][0]		# config channel
c_ch	= hostapd_line[5][8:-1]		# current channel
config	= conf_data[0][2]		# configuration before and after

conf1	= "sed -i 's/channel="
conf2	= "/channel="
conf3	= "/g' /etc/hostapd/hostapd.conf"

if conf_data == 1:
	if c_ch != n_ch:
		ch_conf = conf1 + c_ch + conf2 + n_ch + conf3
		system(ch_conf)

	sql1	= "insert into "
	sql2	= "(conf) "
	sql3	= "values (%s)"
	sql	= sql1 + id_mac + sql2 + sql3
	curs.execute(sql, 0)
	conn.commit()

conn.close()
