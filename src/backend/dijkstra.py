# Dijkstra algorithm
import networkx as nx
import graph

def dijkstra(start, end, graph):
    nodes = list(graph.nodes)
    visited = []
    expand = []
    it_count = 0
    dist = {}
    prev = {}

    for n in nodes:
        dist[n] = 999999
        prev[n] = None
    dist[start] = 0

    for n in list(graph[start]):
        dist[n] = graph[start][n]["weight"]
        prev[n] = start
        expand = sorted(dist, key=dist.get)
        for e in expand:
            if (e in visited or e not in list(graph[start])):
                expand.remove(e)
    visited += start

    while end not in visited:
        c_node = expand.pop(0)
        for n in list(graph[c_node]):
            new_dist = dist[c_node] + graph[c_node][n]["weight"]
            if (new_dist < dist[n] and n not in visited):
                up = {n:new_dist}
                dist.update(up)
                prev[n] = c_node
                expand = sorted(dist, key=dist.get)
                for e in expand:
                    if (e in visited or e not in list(graph[c_node])):
                        expand.remove(e)
        visited += c_node
    print(prev)
    print(dist)

if __name__=="__main__":
    g = nx.DiGraph()
    graph.read_file('tc1.txt', g)
    graph.save_img(g)
    dijkstra('1','6',g)
