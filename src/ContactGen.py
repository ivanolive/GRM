try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import numpy.random as rd
import random
import sys
import socialNet as soc
import MeetingsGen as mg
import groupStructure as gs
import Person as per
import Mobility as mb

LEADER = 0
STRUCTURE = 1
PROB = 2
ENC = 3
END_ENC = 4

def ajustNodesSchedule(nodesSchedule):
	ajusted = []
	for i in range(len(nodesSchedule)):
		print("adjust: "+str(i)+" "+str(len(nodesSchedule[i])))
		for j in range(len(nodesSchedule[i])):
			ajusted = ajusted + [[i,nodesSchedule[i][j][0], int(nodesSchedule[i][j][1][0]),int(nodesSchedule[i][j][1][1]),nodesSchedule[i][j][2]]]
			
	return ajusted

def conflict(entry_a, entry_b):
	flag = False
	to1 = entry_a[2]
	tf1 = entry_a[3]
	to2 = entry_b[2]
	tf2 = entry_b[3]
	case1 = to1 >= to2 and to1 <= tf2
	case2 = tf1 >= to2 and tf1 <= tf2
	case3 = to2 >= to1 and to2 <= tf1
	case4 = tf2 >= to1 and tf2 <= tf1
	if(case1 or case2 or case3 or case4):
		flag = True
	return flag

def computeDurations(entry_a, entry_b):
	to1 = entry_a[2]
	tf1 = entry_a[3]
	to2 = entry_b[2]
	tf2 = entry_b[3]
	init = max(to1,to2)
	end = min(tf1,tf2)
	dur = end - init
	return (init,end,dur)

def generateContacts(nodesSchedule):
	nodesSchedule = ajustNodesSchedule(nodesSchedule)
	copy = nodesSchedule
	print(len(nodesSchedule))
	nodesSchedule.sort(key=lambda x: x[2])
	print("first sorting done")
	nodesSchedule.sort(key=lambda x: x[1])
	print("second sorting done")
	f = open("contacts_test.csv","w")
	
	contacts = []
	
	group_ant = nodesSchedule[0][1]
	group = []

	for i in range(len(nodesSchedule)):
		if i % 1000 == 0:
			print i
		if nodesSchedule[i][1] == group_ant:
			group = group + [nodesSchedule[i]]
		else:
			for j in range(len(group)):
				for k in range(j,len(group)):
					if (j!=k and conflict(group[j],group[k])):
						init,end,dur = computeDurations(group[j],group[k])
						contacts = contacts + [[group[j][0],group[k][0],init,dur]]
						#f.write(str(group[j][0])+" "+str(group[k][0])+" "+str(init)+" "+str(end)+" "+str(dur)+"\n")
						#f.flush() 
			group = [nodesSchedule[i]]

		group_ant = nodesSchedule[i][1]
	contacts.sort(key=lambda x: x[2])
	for i in range(len(contacts)):
		if contacts[i][3] > 0:
			f.write(str(contacts[i][0])+" "+str(contacts[i][1])+" "+str(contacts[i][2])+" "+str(contacts[i][3])+"\n")
	f.close()
	return copy

