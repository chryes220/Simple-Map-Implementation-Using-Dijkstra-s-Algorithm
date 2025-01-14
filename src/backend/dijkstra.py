# Dijkstra algorithm
import networkx as nx
import graph
import time

def dijkstra(source, dest, graph):
    begin = time.perf_counter()
    nodes = list(graph.nodes)
    visited = []
    expand = []
    it_count = 0
    dist = {}
    prev = {}

    for n in nodes:
        dist[n] = 999999
        prev[n] = None
    dist[source] = 0

    for n in list(graph[source]):
        dist[n] = graph[source][n]["weight"]
        prev[n] = source

    expand = sorted(dist, key=dist.get)
    expand = [node for node in expand if (node not in visited and node in list(graph[source]))]
    
    visited += source
    it_count += 1

    while (dest not in visited) and (len(expand) > 0):
        c_node = expand.pop(0)
        for n in list(graph[c_node]):
            new_dist = dist[c_node] + graph[c_node][n]["weight"]
            if (new_dist < dist[n] and n not in visited):
                up = {n:new_dist}
                dist.update(up)
                prev[n] = c_node
        
        visited += c_node
        expand = sorted(dist, key=dist.get)
        expand = [node for node in expand if (node not in visited and dist[node] != 999999)]     
        it_count += 1
        
    end = time.perf_counter()

    if (dest not in visited):
        return ([], visited, end-begin, None, it_count)
    else:
        path = [dest]
        while source not in path:
            path.append(prev[path[len(path)-1]])
        path.reverse()
        
        distance = dist[dest]
        return (path, visited, end-begin, distance, it_count)

if __name__=="__main__":
    g = nx.DiGraph()
    graph.read_file('tc2.txt', g)
    graph.save_init_img(g)
    graph.save_fin_img(g, dijkstra('1','5',g)[0], dijkstra('1','5',g)[1])
