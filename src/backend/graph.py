import math
import networkx as nx
import matplotlib.pyplot as plt
from os import path
from netgraph import Graph

def read_file(filename, g):
    # read txt file, translate content into nx.DiGraph
    p = filename
    lines = []
    with open(p, 'r') as f:
        lines = f.readlines()
    node_count = int(lines[0])
    for i in range (node_count):
        g.add_node(str(i+1))
    for i in range (1, len(lines)):
        edge = lines[i].split(' ')
        g.add_edge(edge[0],edge[1],weight=float(edge[2]))

def save_init_img(G):
    pos = nx.shell_layout(G)

    #pos = nx.spring_layout(G, seed=7, k=5/math.sqrt(G.order()))
    edge_labels = nx.get_edge_attributes(G, 'weight')
    Graph(G, node_layout=pos, edge_layout='curved', origin=(-1, -1), scale=(2, 2),
        node_color="#259881cc", node_size=15.,
        node_labels=True, node_label_fontdict=dict(size=13),
        edge_labels=edge_labels, edge_label_fontdict=dict(size=9),
        arrows=True, edge_width=2., edge_color="black"
    )
    
    filepath = path.dirname(path.dirname(__file__))
    filepath = path.join(filepath, "frontend/static/graph_init.jpg")
    plt.savefig(filepath)
    plt.clf()

def save_fin_img(G, p, visited):
    pos = nx.shell_layout(G)

    # nodes
    color_map = {}
    for node in G:
        if node in visited:
            color_map[node] = "#dfad2ed9"
        else:
            color_map[node] = "#259881cc"

    edge_labels = nx.get_edge_attributes(G, 'weight')

    # edges
    for (u,v) in G.edges:
        G[u][v]['color'] = 'black'
    for i in range (len(p)-1):
        G[p[i]][p[i+1]]['color'] = 'red'
    edge_color_map = {}
    for (u,v) in G.edges:
        edge_color_map[(u,v)] = G[u][v]['color']
    #edge_color_map = [G[u][v]['color'] for (u,v) in G.edges]

    Graph(G, node_layout=pos, edge_layout='curved', origin=(-1, -1), scale=(2, 2),
        node_color=color_map, node_size=15.,
        node_labels=True, node_label_fontdict=dict(size=13),
        edge_labels=edge_labels, edge_label_fontdict=dict(size=9),
        arrows=True, edge_width=2., edge_color=edge_color_map
    )

    filepath = path.dirname(path.dirname(__file__))
    filepath = path.join(filepath, "frontend/static/graph_fin.jpg")
    plt.savefig(filepath)
    plt.clf()

if __name__=="__main__":
    G = nx.DiGraph()
    read_file("tc1.txt", G)
    save_init_img(G)
