#!/usr/bin/python3

from os import system
import os

#import MySQLdb
import pymysql

	# Open DB connect
DB_ip	= "172.31.1.19"				###### Have to address modify!!
#id_ip	= ip_addr_get.ip
conn	= pymysql.connect(DB_ip,"Controller","","netdb")
curs	= conn.cursor()

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

