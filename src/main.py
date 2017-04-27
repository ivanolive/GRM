#import networkx as nx
#import numpy.random as rd
#import random
import sys
import socialNet as soc
import MeetingsGen as mg
import groupStructure as gs
import Person as per
import Mobility as mb
import ContactGen as cg

###########Simulation Parameters################
sim_dur = 60
groups_dur = 30

n_nodes = 1000
grid_x = 1500
grid_y = 1500
cell_size = 50
space_gran = 10
path_time = 300
################################################

#########Statistical Parameters#################
group_size_alpha = 2
group_size_beta = 20

group_ict_alpha = 2

duration_alpha = 2
duration_beta = 30*24
################################################

sys.setrecursionlimit(1000000)

if len(sys.argv) == 1:
#########Synthetic Social Network Paramenters#################
	social_graph_cluster_size = 50#20
	cluster_size_sdev = 10
	p_in = 0.8
	p_out = 0.2
	socialGraph = soc.generateGaussian(n_nodes,social_graph_cluster_size, cluster_size_sdev,p_in,p_out);
##############################################################
else:
######### Social edge threshold for real social contact traces#############################
	w_th = 1*3600
	socialGraph = soc.readSocialGraph(sys.argv[1],n_nodes, w_th)
###########################################################################################

homes = mb.nodeHomes(n_nodes,grid_x,grid_y,cell_size)
print("Social Graph Generated")
groups = gs.defineGroups(n_nodes-1,group_ict_alpha,homes,group_size_alpha,group_size_beta,duration_alpha,duration_beta,socialGraph,sim_dur,groups_dur,grid_x,grid_y,cell_size,path_time)
print("Groups Defined")
nodesSchedule = per.allNodesSchedule(n_nodes,groups,path_time)
print("Nodes Schedule Defined")
nodesSchedule = cg.generateContacts(nodesSchedule)

mb.generateMobility(nodesSchedule,homes,space_gran,path_time)
mb.sortMobility(homes,grid_x,grid_y,sim_dur)


