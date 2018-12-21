
import  osmnx  as ox
import networkx as nx
import sys
import nxmetis
import metis

ox.config(log_file=True, log_console=True, use_cache=True)
# get the driving network for Colombo
# G = ox.graph_from_place('Colombo, Colombo District, Western Province, Sri Lanka', network_type='drive', buffer_dist=10000)
# # G = ox.graph_from_file('/home/chanaka/pyProjects/osrm-backend/map2.osm', network_type='drive')
#
# G_projected = ox.project_graph(G)
# ox.save_graphml(G_projected, filename='colombo_roads.graphml')
# fig, ax = ox.plot_graph(G_projected)
# r_graph = nx.read_graphml("data/colombo_roads.graphml")

# print(r_graph.nodes(data=True))

def get_colombo_graph():
    G = ox.graph_from_place('Colombo, Colombo District, Western Province, Sri Lanka', network_type='drive',
                            buffer_dist=15000, simplify=True)
    # G_projected = ox.project_graph(G)

    ox.save_graphml(G, filename='colombo_roads_test_15000.graphml')
    r_graph = nx.read_graphml("data/colombo_roads_test_15000.graphml")
    r_graph = (convert_to_simpleG(r_graph))

    return r_graph,G

def isShortTrip(graph, orig_node, dest_node):
    route = nx.shortest_path(graph, orig_node, dest_node, weight='length')
    print(route)


def get_nearest_node(G, coordinate):
    # print(coordinate)
    node = ox.get_nearest_node(G, coordinate)
    # print(node)
    return node

def get_path(G, start, dest):
    if(nx.has_path(G, start, dest)):
        route = nx.shortest_path(G, start, dest, weight='length')
        # fig, ax = ox.plot_graph_route(G, route, node_size=0)
        return route

def convert_to_simpleG(graph):
    g = graph.to_undirected(graph)

    G = nx.Graph()
    for u, v, data in g.edges(data=True):
        w = data['trips'] if 'trips' in data else 0
        if G.has_edge(u, v):
            G[u][v]['trips'] += w
        else:
            G.add_edge(u, v, trips=w)

    print(G.edges(data=True))
    return G

def metis_partition(graph):
    print('metis partitioning...')
    # G = nx.complete_graph(10)
    sg = convert_to_simpleG(graph)
    print(nx.number_of_nodes(sg))
    print(sg.size(weight='trips'))
    cut = nxmetis.partition(sg, 2, edge_weight= 'trips', recursive = True)[0]
    print(cut)


# metis_partition()

[17010, 530338, 565976]