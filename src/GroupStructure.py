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
import HeavyTail as pl
import Mobility as mb

def fixedSnowball(center,graph, maxNodes):
	members = [center]
	iterator = 0
	while len(members) < maxNodes and iterator < len(members):
		for i in graph.neighbors(members[iterator]):
			if not (i in members):
				members = members + [i]
		if len(members) > maxNodes:
			return members[0:maxNodes]
		iterator+=1
	return members

def snowball(center,graph, maxNodes, p):
	members = [center]
	iterator = 0
	while len(members) < maxNodes and iterator < len(members):
		randomizedNeighbors = list(rd.permutation(graph.neighbors(members[iterator])))
		size = int(len(members)*p) + 1
		randomizedNeighbors = randomizedNeighbors[:size]
		for i in randomizedNeighbors:
			if not (i in members):
				members = members + [i]
		if len(members) > maxNodes:
			return members[0:maxNodes]
		iterator+=1
	return members

	
def plotSnowball(G, snowball,num):

	pos=nx.graphviz_layout(G) # positions for all nodes

	plt.figure(figsize=(12,12))

	nx.draw_networkx_nodes(G,pos,nodelist=snowball,node_color="red")

	nx.draw_networkx_edges(G,pos,width=1)
			# labels
	nx.draw_networkx_labels(G,pos,font_size=12,font_family='sans-serif')

	plt.axis('off')
	plt.savefig("snowball"+str(num)+".png") # save as png
	plt.close()

def snowBallTest():			
	leaders = selectGroupLeaders(40,10)

	socialGraph = soc.generateGaussian(100,20, 10,0.5,0.002);

	sb = snowball(20,socialGraph, 5)
	plotSnowball(socialGraph,sb,1)

	sb = snowball(20,socialGraph, 10)
	plotSnowball(socialGraph,sb,2)

	sb = snowball(20,socialGraph, 20)
	plotSnowball(socialGraph,sb,3)

	sb = snowball(20,socialGraph, 40)
	plotSnowball(socialGraph,sb,4)

	sb = snowball(20,socialGraph, 80)
	plotSnowball(socialGraph,sb,5)

def defineGroupLeaders(n_nodes,n_groups): #selects group leaders with uniform distribution
	leaderSet = []
	for i in range(n_groups):
		leaderSet = leaderSet + [random.randint(0, n_nodes)]
	return leaderSet

def defineGroupSizes(n_groups,alpha, beta):
	sizes = []
	sample = pl.randht(n_groups,'cutoff',3,alpha,1.0/(beta));
	#sample = rd.exponential(beta,n_groups)
	for i in sample:
		sizes = sizes + [int(i)]

	return sizes

def defineGroups(n_nodes, groupICTalpha,homes, group_size_alpha, group_size_beta, dur_alpha, dur_beta, socialGraph,sim_dur,groups_dur, grid_x, grid_y, grid_size,pathTime):
	n_groups,groupsRegDistro = mg.readRegularityDistro()
	#groupsRegDistro = mg.generateRegularityDistro(n_groups, groupICTalpha)
	meetings = mg.generateGroupSet(n_groups,groupICTalpha,groupsRegDistro,groups_dur,sim_dur,pathTime)
	endMeeting = mg.generateMeetingDur(n_groups,meetings,dur_alpha,dur_beta,pathTime);
	#print(teste)
	leaders = defineGroupLeaders(n_nodes, n_groups)
	sizes = defineGroupSizes(n_groups, group_size_alpha, group_size_beta)
	#homes = mb.nodeHomes(n_nodes+1,grid_x,grid_y,grid_size)
	groupsList = []
	for i in range(n_groups):
		print(i)
		leader = leaders[i]
		size = sizes[i]
		structure = snowball(leader,socialGraph,size,0.5)
		probabilities = []
		for j in range(len(structure)):
			probabilities = probabilities + [willIGo(structure[j],structure,socialGraph)]
		if sum(probabilities) == 0:
			continue
		encounters = meetings[i]
		endEncounter = endMeeting[i]
		positions = []
		for j in range(len(meetings[i])):
			probMatrix = mb.meetingPlacesProb(structure,probabilities, homes, grid_x, grid_y, grid_size)
			coin = (rd.randint(0,100000000)*1.0)/100000000
			last = [0,0]
			for i2 in range(len(probMatrix)):
				for j2 in range(len(probMatrix[i2])):				
					if probMatrix[i2][j2] > coin:
						break
					last = [i2*grid_size + grid_size/2.0,j2*grid_size + grid_size/2.0]
			position = last
			
			positions = positions + [position]

		groupsList = groupsList + [[leader,structure,probabilities,encounters,endEncounter,positions]]
		
	return groupsList

def willIGo(node_id, group_struct, graph):
	if len(group_struct) <= 1:
		return 0;
	neighbors = graph.neighbors(node_id)
	intersection = 1.0*len(list(set(neighbors).intersection(group_struct)))
	return intersection/(len(group_struct)-1)

def printGroups(groups):
	for i in groups:
		print("Leader: " +str(i[0])+"\n")
		print("Structure: " +str(i[1])+"\n")
		print("Probabilities: " +str(i[2])+"\n")		
		print("Encounters: " +str(i[3])+"\n")
		print("End of Encounters: " +str(i[4])+"\n")
		print("Duration:")
		test = []
		for j in range(len(i[4])):
			test = test+[(i[4][j]-i[3][j])]
		print(test)
		print ("Positions: " +str(i[5])+"\n")
		print ;

def printDurations(groups):
	for i in groups:
		for j in range(len(i[2])):
			print(int(i[3][j]-i[2][j]))



