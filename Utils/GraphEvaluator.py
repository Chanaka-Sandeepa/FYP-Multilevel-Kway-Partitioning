import networkx as nx
from networkx.algorithms.community import LFR_benchmark_graph
import nxmetis
from networkx.algorithms import community
from Utils import OSMNXutil
from Utils import CoordinateUtil

from geoindex import GeoGridIndex, GeoPoint


def generateLFR():
    n = 1000
    tau1 = 3
    tau2 = 1.5
    mu = 0.1
    G = LFR_benchmark_graph(n, tau1, tau2, mu, average_degree=5, min_community = 100, seed = 10)
    edges = G.edges(data=True)
    return G

def metis_partition(graph, partition_count):
    print('metis partitioning...')
    # G = nx.complete_graph(10)
    print('nodes', nx.number_of_nodes(graph))
    print('edges', nx.number_of_edges(graph))
    print(graph.size(weight='weight'))
    cut, partitions = nxmetis.partition(graph, partition_count, edge_weight= 'weight', recursive = True)
    print('metis cut', cut)
    print('coverage', community.coverage(graph, partitions))
    refinedPartitions = community.kernighan_lin_bisection(graph, partitions, 10, weight='weight')
    print('refined coverage', community.coverage(graph, refinedPartitions))


def test_trip_cut(marked_graph, road_graph, test_trips):
    index = GeoGridIndex()

    cut = 0
    c = 0
    node_list = marked_graph
    # print(node_list)
    road_nodes = road_graph.nodes(data=True)
    print(road_nodes)
    # print(marked_graph.number_of_nodes())
    print(road_graph.number_of_nodes())
    for node in road_nodes:
        # print(node[1].get('x'), node[1].get('y'))
        # print(node[0])
        index.add_point(GeoPoint(float(node[1].get('x')), float(node[1].get('y')), ref=node[0]))


    for index2, row in test_trips.iterrows():
        # print(row)
        start = row['pickup']
        dest = row['dropoff']
        # start_tuple = CoordinateUtil.getTupleWithStringCoordinate(start)
        # dest_tuple = CoordinateUtil.getTupleWithStringCoordinate(dest)
        # print(start_tuple)
        start_node = getNearestPointByIndex(start, index)
        dest_node = getNearestPointByIndex(dest, index)

        start_partition = 1000
        dest_partition = 1000
        has_start = False
        has_dest = False
        for n in node_list:
            print(n, start_node)
            if(has_start & has_dest):
                break
            if str(n[0]) == str(start_node):
                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                start_partition = n[1].get('partition')
                has_start = True

            if n[0] == dest_node:
                # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                dest_partition = n[1].get('partition')
                has_dest = True
        print(start_partition, dest_partition, 'count', c)
        if((start_partition != dest_partition) & (has_start & has_dest)):
            cut +=1
        if c > 1000:
            break
        c += 1
    print(cut)


def getNearestPointByIndex(node, index):
    # print(node)
    node_list = node.split(",")
    # print(node_list[0])
    center_point = GeoPoint((float(node_list[0])), float(node_list[1]))
    # print(float(node_list[0]), float(node_list[1]))
    for point, distance in index.get_nearest_points(center_point, 0.1, 'km'):
        # print("We nodeId {0} in {1} km".format(point.ref, distance))
        return point.ref


