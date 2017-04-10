#!/usr/bin/python

import MySQLdb
import pymysql

from os import system
import os

import numpy as np
import numpy.linalg as lin

import copy

import ip_addr_get				# AP own ip

##### Foundation work
	# Open DB connect
DB_ip	= "192.168.1.224"				###### Have to address modify!!
#id_ip	= ip_addr_get.ip
#conn	= pymysql.connect(DB_ip,"Controller","","netdb")
conn	= pymysql.connect(DB_ip,"Controller","","netex")
curs	= conn.cursor()

	# get STAs id_mac
STA_info	= open("hostInfo.dat","r")
STA_list	= STA_info.readlines()
STA_N	= len(STA_list) // 6

STAs 	= []					# Defined STAs
for i in range(0, STA_N):
	STA_mac	= STA_list[6*i+3][6:-1]
	STA	= STA_mac.replace(":","")
	STAs.append(STA)
	print (STA)

	# get APs id_mac
sql	= "show tables"
curs.execute(sql)
rows	= curs.fetchall()
AP_N	= len(rows)
F	= 3

APs	= []
for i in range(0, len(rows)):
	APs.append(rows[i][0])	# real APs_id

"""
	# get All APs ID
scanning_AP	= []
scanning_APs	= []
i	= 0
for AP in APs:
#	sql1 = "select ID from netdb."
	sql1 = "select ID from netex."
	sql_AP = sql1 + AP
#		print (AP)
	curs.execute(sql_AP)
	rows = curs.fetchall()
	for j in range(0, len(rows)):
		scanning_AP.append(rows[j][0])	# real All_id
	scanning_APs.append(scanning_AP)
	i = i + 1
print (scanning_APs)
"""

##### Network topology matrix G(N*N)
G	= np.zeros((AP_N,AP_N))
# inter AP-AP
i	= 0
for AP1 in APs:
	j = 0
	for AP2 in APs:
#		sql1 = "select * from netdb."
		sql1 = "select * from netex."
		sql2 = " where ID=%s"
		sql_AP = sql1 + AP1 + sql2
		curs.execute(sql_AP, AP2)
		AP1_AP2 = curs.fetchall()
		if AP1_AP2 != ():
			G[i][j] = 1
		else:
			G[i][j] = 0
		j = j + 1		# j-th AP2
	i = i + 1			# i-th AP1

# inter AP-STA
i	= 0
for AP1 in APs:
	j = 0
	for AP2 in APs:
		for STA in STAs:			##### STAs <- hosts information
#			sql1 = "select ID from netdb."
			sql1 = "select ID from netex."
			sql2 = " where ID=%s"
			sql_AP1 = sql1 + AP1 + sql2
			sql_AP2 = sql1 + AP2 + sql2

			curs.execute(sql_AP1, STA)
			STA_AP1 = curs.fetchall()
			curs.execute(sql_AP2, STA)
			STA_AP2 = curs.fetchall()
			
			if len(STA_AP1) == len(STA_AP2):
				G[i][j] = 1	# Through STA, AP1 and AP2 have co-region
		j = j + 1
	i = i + 1


##### Channel assignment matrix A(F*N)	
A	= np.zeros((F,AP_N))
for AP in APs:
	i = 0
#	sql1 = "select ch from netdb."
	sql1 = "select ch from netex."
	sql2 = " where ID=%s"
	sql_AP = sql1 + AP + sql2
	curs.execute(sql_AP, AP)
	ch = curs.fetchall()[0][0]		# AP's ch
#	print (curs.fetchall())
	if ch == 1:
		A[0][i] = 1
		A[1][i] = 0
		A[2][i] = 0
	elif ch == 6:
		A[0][i] = 0
		A[1][i] = 1
		A[2][i] = 0
	elif ch == 11:
		A[0][i] = 0
		A[1][i] = 0
		A[2][i] = 1
	i = i + 1


##### Interference predicted matrix I(N*F)
I	= np.zeros((AP_N,F))
# inter AP-AP


# inter AP-STA


######################################################################################################
##### ILP			# simplicity
c_A	= np.zeros((F,AP_N))
n_A	= np.zeros((F,AP_N))
c_A_star	= AP_N
c_similar_A	= 0

for k in range(0,F ** AP_N):
	j = 0
	for AP in APs:
		c_A[0][j] = 1	# initiate [[1,1,1...][0,0,0...][0,0,0...]]
		j = j + 1
	j = 0
#	print (k)
	while k:
		i = k % 3
		k = k // 3

		c_A[0][j] = 0
		c_A[1][j] = 0
		c_A[2][j] = 0
		c_A[i][j] = 1
		j = j + 1

	W = np.dot(G, c_A.T)		# G x A.T
	Ele_mul_W = W * c_A.T		# W . A.T
	n_A_star = Ele_mul_W.sum()	# current A*
	
	if c_A_star >= n_A_star:		# 
		n_similar_A = copy.deepcopy((A * c_A).sum)	# Similarity with A and c_A
		if c_similar_A < n_similar_A:
			c_A_star = copy.deepcopy(n_A_star)
			n_A = copy.deepcopy(c_A)
print (n_A)
#	U = W * I
######################################################################################################

##### For insert next_config data
	# Open DB connection
#conn	= pymysql.connect(DB_ip,"Controller","","confdb")
conn	= pymysql.connect(DB_ip,"Controller","","confex")
curs	= conn.cursor()

i	= 0
for AP in APs:
		# create table
	sql1	= "create table if not exists `"
	table	= AP
	sql2	= "` (ch int(2), dB int(100), conf int);"
	sql	= sql1 + table + sql2
	curs.execute(sql)
	conn.commit()
	print (i)
		# delete previous data
	sql1	= "delete from "
	sql	= sql1 + AP
	curs.execute(sql)
	conn.commit()
		# insert config data
	sql1	= "insert into "
	sql2	= "(ch,dB,conf) "
	sql3	= "values (%s, %s, %s)"
	sql	= sql1 + AP + sql2 + sql3
	
	if n_A[0][i] == 1:
		conf_data	= (1,0,1)
	elif n_A[1][i] == 1:
		conf_data	= (6,0,1)
	elif n_A[2][i] == 1:
		conf_data	= (11,0,1)

	curs.execute(sql, conf_data)
	conn.commit()

	i	= i + 1


###### Clear netdb -> For cognizing removed/added APs
sql	= "show tables from netdb"
curs.execute(sql)
if curs.fetchall() != ():			# if netdb is empty, anything else
	sql	="""SET @tables = NULL;
		SELECT GROUP_CONCAT(table_schema, '.', table_name) INTO @tables
			FROM information_schema.tables
			WHERE table_schema = 'netdb';
		SET @tables = CONCAT('DROP TABLE ', @tables);
		PREPARE stmt FROM @tables;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;"""
	curs.execute(sql)
	conn.commit()



