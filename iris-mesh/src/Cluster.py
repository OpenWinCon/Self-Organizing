#!/usr/bin/python3

from os import system
import os

import numpy as np
import numpy.linalg as lin
import copy
import random

import math
"""
	##### locate randomly AP #####
rand_AP_loc = np.zeros((100,2))
for i in range(0,100):
	for j in range(0,2):
		rand_AP_loc[i][j] = random.randrange(0,100)
#print(rand_AP_loc)
"""
"""
rand_AP_loc = np.zeros((100,2))
k = 0
for i in range(0,10):
	for j in range(0,10):
		rand_AP_loc[k][0] = i*10 + 5
		rand_AP_loc[k][1] = j*10 + 5
		k = k + 1
#print(rand_AP_loc)
"""
"""
	##### AP-AP distance #####
G = np.zeros((100,100))
D = np.zeros((100,100))
k = 0
for i in range(0,100):
	for j in range(0,100):
		d_sq = ((rand_AP_loc[i][0] - rand_AP_loc[j][0]) ** 2) + ((rand_AP_loc[i][1] - rand_AP_loc[j][1]) ** 2)
		D[i][j] = math.sqrt(d_sq)
		if d_sq < 196:					##### How long APs' distance
			if i != j:
				G[i][j] = 1
				k = k + 1
			else:
				G[i][j] = 0
		else:
			G[i][j] = 0
"""


	##### Make Cluster #####
H = np.zeros((100,100))
num_cluster = 0
cluster_s = [set() for i in range(0,100)]
cluster_l = [list() for i in range(0,100)]
cluster_head = max_num_nei_AP
all_cluster_element_s = set()
all_AP_s = set()
for i in range(0,100):
	all_AP_s = all_AP_s | set([i])
#print (all_AP_s)
i = 0
nei_AP = 0
max_nei_AP = 0


	##### Jaccard Similarity #####
nei_AP_s = [set() for i in range(0,100)]
nei_AP_l = [list() for i in range(0,100)]
for i in range(0,100):
	nei_AP_s[i] = nei_AP_s[i] | set([i])
	for j in range(0,100):
		if G[i][j] == 1:
			nei_AP_s[i] = nei_AP_s[i] | set([j])
#print (nei_AP_s)

Jac_sim = np.zeros((100,100))
for i in range(0,100):
	for j in range(0,100):
		if G[i][j] == 1:
			Jac_sim[i][j] = (len(nei_AP_s[i] & nei_AP_s[j])) / (len(nei_AP_s[i] | nei_AP_s[j]))
		if i == j:
			Jac_sim[i][j] = 1

cluster_s = [set() for i in range(0,100)]
cluster_l = [list() for i in range(0,100)]
n = 0
k = 0
lamb = 0.6															##### How much similarity threshold
for i in range(0,100):
	cluster_s[i] = set([i])
	if i != 0:
		for k in range (0,i):
			if (cluster_s[i].issubset(cluster_s[k])):
#				print(cluster_s[i])
#				print(cluster_s[k])
				break
			else:
				k = i
#	print("i = ", i)
#	print("k = ", k)
	for j in range(0,100):
			if Jac_sim[i][j] > lamb:
				cluster_s[k] = cluster_s[k] | set([i]) | set([j])

	cluster_l[k] = list(cluster_s[k])
	cluster_l[k] = sorted(cluster_l[k])
print("cluster_l")
print(cluster_l)

a = 0
pre_b = 0
b = 99999
si = np.zeros((100,3))
for i in range(0,100):
	for j in range(0,100):
		if len(cluster_l[j]) != 0:
			if set([i]) == (set([i]) & cluster_s[j]):
				for k in range(0,len(cluster_s[j])):
					a = a + D[i][cluster_l[j][k]]
				a = a / (len(cluster_s[j]))
				print ("a = ", a, i)
			else:
				for k in range(0,len(cluster_s[j])):
					pre_b = pre_b + D[i][cluster_l[j][k]]
				pre_b = pre_b / (len(cluster_s[j]))
				if pre_b < b:
					b = pre_b
	print ("b = ", b, i)
	s = (b - a) / max(a,b)
	si[i][0] = a
	si[i][1] = b
	si[i][2] = s
	print ("s = ", s, i)
	print ("\n")
print (si)


N1 = 0
N2 = 0
for i in range(0,100):
	if (len(cluster_l[i]) > 5):
		N1 = N1 + 1
	if (len(cluster_l[i]) > 0):
		N2 = N2 + 1
print ("# of main clusters = ", N1)
print ("# of clusters = ", N2)








#"""
f = open("Cluster.out",'w')
for i in range(0,100):
	for j in range(0,len(cluster_l[i])):
#		f.write(str(cluster_l[i][j]))
#		f.write(" ")
		for k in range(0,2):
			f.write(str(rand_AP_loc[cluster_l[i][j]][k]))
			f.write(" ")
			if k == 1:
				f.write("\n")
	f.write("\n")
f.close()

f = open("Jac_sim.out",'w')
for i in range(0,100):
	for j in range(0,100):
		f.write(str(Jac_sim[i][j]))
		f.write(" ")
		if j%100 == 99:
			f.write("\n")
f.close()

f = open("G.out",'w')
for i in range(0,100):
	for j in range(0,100):
		f.write(str(G[i][j]))
		f.write(" ")
		if j%100 == 99:
			f.write("\n")
f.close()

f = open("D.out",'w')
for i in range(0,100):
	for j in range(0,100):
		f.write(str(D[i][j]))
		f.write(" ")
		if j%100 == 99:
			f.write("\n")
f.close()

f = open("loc.out",'w')
for i in range(0,100):
	f.write(str(i))
	f.write(" ")
	for j in range(0,2):
		f.write(str(rand_AP_loc[i][j]))
		f.write(" ")
		if j == 1:
			f.write("\n")
f.close()
#"""
