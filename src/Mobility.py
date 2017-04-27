
import matplotlib.pyplot as plt
import networkx as nx
import numpy.random as rd
import random
import sys
import socialNet as soc
import MeetingsGen as mg
import numpy as np
#import groupStructure as gs
#import Person as per

LEADER = 0
STRUCTURE = 1
PROB = 2
ENC = 3
END_ENC = 4
POSITION = 5

def nodeHomes(n_nodes,grid_x,grid_y,grid_size):
	node_homes = []
	for i in range(n_nodes):
		x = rd.randint(0,grid_x)
		y = rd.randint(0,grid_y)
		node_homes = node_homes + [[x + grid_size/2.0,y + grid_size/2.0]]
	return node_homes

def distance(p1,p2,alpha):
	euclideanDistance = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**(1.0/2.0)+15
	return euclideanDistance**(-alpha)

def meetingPlacesProb(groupStructure,nodesProb, nodeHomes, grid_x, grid_y, grid_size):
	probMatrix = [[0 for i in range(grid_x/grid_size)] for j in range(grid_y/grid_size)]
	consideredHomes = []
	totalSum = 0
	for i in groupStructure:
		consideredHomes = consideredHomes + [nodeHomes[i]]
	cumsum = 0
	for i in range(len(probMatrix)):
		for j in range(len(probMatrix[i])):
			cellPosition = [grid_size*i + grid_size/2.0, grid_size*j + grid_size/2.0]
			avgDist = 0
			for k in range(len(consideredHomes)):

				avgDist += (distance(consideredHomes[k],cellPosition,2.0)*nodesProb[k])/sum(nodesProb)
			probMatrix[i][j] = avgDist/len(consideredHomes)
			totalSum += probMatrix[i][j]


	for i in range(len(probMatrix)):
		for j in range(len(probMatrix[i])):
			probMatrix[i][j] = probMatrix[i][j]/totalSum

	totalSum = 0

	for i in range(len(probMatrix)):
		for j in range(len(probMatrix[i])):				
			totalSum += probMatrix[i][j]
			probMatrix[i][j] = totalSum
	return probMatrix

def walk(currentPosition,nextPosition,currentTime,displacementTime,gran):
	n = (((currentPosition[0] - nextPosition[0])**2 + (currentPosition[1] - nextPosition[1])**2)**(1.0/2.0))/gran
	dispx = 1.0*(nextPosition[0] - currentPosition[0])/n
	dispy = 1.0*(nextPosition[1] - currentPosition[1])/n
	timeStep = displacementTime/n
	positions = []
	x = currentPosition[0]
	y = currentPosition[1]
	time = currentTime
	for i in range(int(n)):
		x += dispx
		y += dispy
		time += timeStep
		positions = positions +[[int(x),int(y),int(time)]]
	return positions

def generateMobility(nodesSchedule,homes,spaceGran,displacementTime):
	nodesSchedule.sort(key=lambda x: x[2])
	nodesSchedule.sort(key=lambda x: x[0])
	last = nodesSchedule[0][0]
	time = 0
	f = open("trace.csv","w")
	currentPosition	= homes[nodesSchedule[0][0]]

	for i in range(len(nodesSchedule)):
		init = nodesSchedule[i][2]
		end = nodesSchedule[i][3]
		nextPosition = nodesSchedule[i][4]
		next = nodesSchedule[i][0]
		if next != last:
			currentPosition = homes[nodesSchedule[i][0]]

		if nextPosition != currentPosition:
			positions = walk(currentPosition,nextPosition,init-displacementTime,displacementTime,spaceGran)
			for j in range(len(positions)):
				f.write(str(positions[j][2])+" "+str(nodesSchedule[i][0])+" "+str(positions[j][0])+" "+str(positions[j][1])+"\n")
			f.write(str(init)+" "+str(nodesSchedule[i][0])+" "+str(int(nextPosition[0]))+" "+str(int(nextPosition[1]))+"\n")
			f.write(str(end)+" "+str(nodesSchedule[i][0])+" "+str(int(nextPosition[0]))+" "+str(int(nextPosition[1]))+"\n")
			currentPosition = nextPosition
	
		if i < len(nodesSchedule)-1 and nodesSchedule[i][0] == nodesSchedule[i+1][0]:
			if nodesSchedule[i+1][2] - end < displacementTime*2:
				continue
			else:
				nextPosition = homes[nodesSchedule[i][0]]
				if nextPosition != currentPosition:
					positions = walk(currentPosition,nextPosition,end,displacementTime,spaceGran)
					for j in range(len(positions)):
						f.write(str(positions[j][2])+" "+str(nodesSchedule[i][0])+" "+str(positions[j][0])+" "+str(positions[j][1])+"\n")
					f.write(str(end+displacementTime)+" "+str(nodesSchedule[i][0])+" "+str(int(nextPosition[0]))+" "+str(int(nextPosition[1]))+"\n")
					currentPosition	= nextPosition
		last = next
	f.close()

def sortMobility(homes,grid_x,grid_y,sim_dur):
	f = open("trace.csv")
	trace = []
	t_dur = (sim_dur+5)*24*3600
	cont = 0
	for line in f:
		cont+=1
		if cont%10000 == 0:
			print(cont)
		pair = line.split(" ")
		i = int(pair[0])
		j = int(pair[1])
		k = int(pair[2])
		l = int(pair[3])
		trace.append([i,j,k,l])
	print("sorting")
	trace.sort(key=lambda x: x[0])
	f.close()
	f = open("sorted_trace.csv","w")
	t_dur = trace[len(trace)-1][0]
	t_init = trace[0][0]
	f.write(str(t_init)+" "+str(t_dur)+" 0 "+str(grid_x)+" 0 "+str(grid_y)+"\n")
	for i in range(len(homes)):
		f.write(str(t_init)+" "+str(i)+" "+str(int(homes[i][0]))+" "+str(int(homes[i][1]))+"\n")
	for i in trace:
		f.write(str(i[0])+" "+str(i[1])+" "+str(i[2])+" "+str(i[3])+"\n")
	f.close()
	return

