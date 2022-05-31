import math
from nbformat import read
import networkx as nx
import matplotlib.pyplot as plt
from os import path
from pathlib import Path

def read_file(filename, g):
    p = path.dirname(path.dirname(path.dirname(__file__)))
    p = path.join(p, "test/"+filename)
    lines = []
    with open(p, 'r') as f:
        lines = f.readlines()
    node_count = int(lines[0])
    for i in range (node_count):
        g.add_node(str(i+1))
    for i in range (1, len(lines)):
        edge = lines[i].split(' ')
        g.add_edge(edge[0],edge[1],weight=float(edge[2]))

def save_img(G):
    pos = nx.spring_layout(G, seed=7, k=5/math.sqrt(G.order()))  # positions for all nodes - seed for reproducibility

    # nodes
    nx.draw_networkx_nodes(G, pos)

    # edges
    nx.draw_networkx_edges(G, pos, arrows=True)

    # node labels
    nx.draw_networkx_labels(G, pos, font_family="sans-serif")
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    filepath = path.dirname(path.dirname(__file__))
    filepath = path.join(filepath, "frontend/static/graph.jpg")
    plt.savefig(filepath)

if __name__=="__main__":
    G = nx.DiGraph()
    read_file("tc1.txt", G)
    save_img(G)
