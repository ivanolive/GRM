try:
    import matplotlib.pyplot as plt
except:
    raise

import networkx as nx
import random
import sys

colors = ["#ff0000","#ff8000","#ffbf00","#ffff00","#bfff00","#80ff00","#40ff00","#00ff00", "#00ff40", "#00ff80", "#00ffbf", "#00ffff", "#00bfff", "#0080ff", "#0040ff", "#0000ff", "#4000ff", "#8000ff", "#bf00ff", "#ff00ff", "#ff00bf", "#ff0080", "#ff0040","#ff0000","#ff8000","#ffbf00","#ffff00","#bfff00","#80ff00","#40ff00","#00ff00", "#00ff40", "#00ff80", "#00ffbf", "#00ffff", "#00bfff", "#0080ff", "#0040ff", "#0000ff", "#4000ff", "#8000ff", "#bf00ff", "#ff00ff", "#ff00bf", "#ff0080", "#ff0040","#ff0000","#ff8000","#ffbf00","#ffff00","#bfff00","#80ff00","#40ff00","#00ff00", "#00ff40", "#00ff80", "#00ffbf", "#00ffff", "#00bfff", "#0080ff", "#0040ff", "#0000ff", "#4000ff", "#8000ff", "#bf00ff", "#ff00ff", "#ff00bf", "#ff0080","#ff0040"]

def generateBASyntheticGraph(n_nodes,n_edges): #generates a synthetic graph using the barabasi-albert model
	return nx.barabasi_albert_graph(n_nodes,n_edges);

def generateGaussian(n_nodes,avg_cluster_size, var_cluster_size, p_in, p_out): #generates a synthetic graph using the barabasi-albert model
	return nx.gaussian_random_partition_graph(n_nodes, avg_cluster_size, var_cluster_size, p_in, p_out);

def readSocialGraph(dataset,n_nodes,socialThreshold): # reads a social graph from file. Format: <Node1_ID> <Node2_ID> <0> <weight(integer)>
	G=nx.Graph()

	for i in range(1,n_nodes):
		for j in range(0,n_nodes):
			if(i!=j):
				G.add_edge(i,j,weight=0);

	f = open(dataset)

	dia_ant = 0

	for line in f:
		pair = line.split(" ")
		i = int(pair[0])
		j = int(pair[1])
		time = int(pair[2])
		duration = int(pair[3])

		if(i!=j):
			G[i][j]['weight'] = G[i][j]['weight'] + duration
		else:
			print("A node cannot encounter itself \n disregarding entry...")
	for i in range(0,n_nodes):
		for j in range(i,n_nodes):
			if(i!=j):
				if(G[i][j]['weight'] < socialThreshold):
					G.remove_edge(i,j)


	print("Social Graph Generated")

	return G;

def plotWeightedCommunities(G, W_lim, k_clique, n_nodes):
	for i in range(0,n_nodes):
		for j in range(i,n_nodes):
			if(i!=j):
				print(i,j)
				if(G[i][j]['weight'] < W_lim):
					G.remove_edge(i,j)

	cls = nx.find_cliques(G)
	communities = list(nx.k_clique_communities(G,k_clique ,cliques = cls))

	print(len(communities))

	pos= nx.graphviz_layout(G) # positions for all nodes


	plt.figure(figsize=(12,12))

	#colors = ["green","yellow","red","blue","pink","orange","gray","brown","black","white","purple","green","yellow","red","blue","pink","orange","gray","brown","black","white","purple"]

	for i in range(len(communities)):
		nx.draw_networkx_nodes(G,pos,nodelist=list(communities[i]),node_color=colors[i])

	nx.draw_networkx_edges(G,pos,width=0.5)
			# labels
	#nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')

	plt.axis('off')
	plt.savefig("comm_w_"+str(W_lim)+"k"+str(k_clique)+".png") # save as png
	plt.close()
	
def plotUnweightedCommunities(G, k_clique, n_nodes,iw):

	cls = nx.find_cliques(G)
	communities = list(nx.k_clique_communities(G,k_clique ,cliques = cls))

	print(len(communities))

	pos=nx.graphviz_layout(G) # positions for all nodes


	plt.figure(figsize=(12,12))

	#colors = ["green","yellow","red","blue","pink","orange","gray","brown","black","white","purple","green","yellow","red","blue","pink","orange","gray","brown","black","white","purple"]

#	colors = ["#ff0000","#ff8000","#ffbf00","#ffff00","#bfff00","#80ff00","#40ff00","#00ff00", "#00ff40", "#00ff80", "#00ffbf", "#00ffff", "#00bfff", "#0080ff", "#0040ff", "#0000ff", "#4000ff", "#8000ff", "#bf00ff", "#ff00ff", "#ff00bf", "#ff0080", "#ff0040","#ff0000","#ff8000","#ffbf00","#ffff00","#bfff00","#80ff00","#40ff00","#00ff00", "#00ff40", "#00ff80", "#00ffbf", "#00ffff", "#00bfff", "#0080ff", "#0040ff", "#0000ff", "#4000ff", "#8000ff", "#bf00ff", "#ff00ff", "#ff00bf", "#ff0080", "#ff0040"]

	for i in range(len(communities)):
		nx.draw_networkx_nodes(G,pos,nodelist=list(communities[i]),node_color=colors[i%len(colors)])

	nx.draw_networkx_edges(G,pos,width=0.5)
			# labels
	#nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')

	plt.axis('off')
	plt.savefig("./communities/unweighted_"+"comm_"+"w"+str(iw)+"k"+str(k_clique)+".png") # save as png
	plt.close()


