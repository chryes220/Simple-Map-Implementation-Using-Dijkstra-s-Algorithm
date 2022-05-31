import math
import networkx as nx
import matplotlib.pyplot as plt
from os import path

def read_file(filename, g):
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
    pos = nx.spring_layout(G, seed=7, k=5/math.sqrt(G.order()))  # positions for all nodes - seed for reproducibility
    # nodes
    nx.draw_networkx_nodes(G, pos, node_color="#259881cc")

    # edges
    nx.draw_networkx_edges(G, pos, arrows=True)

    # node labels
    nx.draw_networkx_labels(G, pos, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    filepath = path.dirname(path.dirname(__file__))
    filepath = path.join(filepath, "frontend/static/graph_init.jpg")
    plt.savefig(filepath)

def save_fin_img(G, p, visited):
    pos = nx.spring_layout(G, seed=7, k=5/math.sqrt(G.order()))  # positions for all nodes - seed for reproducibility
    
    color_map = []
    for node in G:
        if node in visited:
            color_map.append("#11bbc1")
        else:
            color_map.append("#259881cc")
    nx.draw_networkx_nodes(G, pos, node_color=color_map)

    for (u,v) in G.edges:
        G[u][v]['color'] = 'black'
    for i in range (len(p)-1):
        G[p[i]][p[i+1]]['color'] = 'red'
    edge_color_map = [G[u][v]['color'] for (u,v) in G.edges]
    nx.draw_networkx_edges(G, pos, edge_color = edge_color_map, arrows=True)

    # node labels
    nx.draw_networkx_labels(G, pos, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    filepath = path.dirname(path.dirname(__file__))
    filepath = path.join(filepath, "frontend/static/graph_fin.jpg")
    plt.savefig(filepath)

if __name__=="__main__":
    G = nx.DiGraph()
    read_file("tc1.txt", G)
    save_init_img(G)
