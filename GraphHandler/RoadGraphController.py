import networkx as nx
from Utils import OSRMUtil
from Utils import GraphUtils
from scipy import spatial
from Utils import CoordinateUtil
from Utils import BaseNodeMapper


def create_road_graph(roads):
    print("Creating roads graph...")
    G = nx.Graph()
    count = 0

    for road in roads:
        for i in range(len(road)-1):
            cor_node = OSRMUtil.getNodeFromCoordinate(road[i])
            cor_next_node = OSRMUtil.getNodeFromCoordinate(road[i+1])

            if(cor_next_node != 0 and cor_node != 0 and cor_next_node != cor_node):
                G.add_node(cor_node, coordinate=road[i])
                G.add_node(cor_next_node, coordinate=road[i+1])
                G.add_edge(cor_node,cor_next_node, weight =0)

    # GraphUtils.draw_graph(G)
    print("road graph nodes :-", G.number_of_nodes())


    gs = nx.connected_component_subgraphs(G)
    c =0
    for a in gs:
        c += 1
    print('sub in roadG', c)

    # mainTest.set_road_corList(road_cor_list)
    return G


def create_roads_with_basenodes(roads, base_nodes, base_coordinate_list):
    print('Creating road network with base nodes...')
    G = nx.Graph()
    base_cor_tuples = GraphUtils.getBaseCoordinateTuples(base_coordinate_list)
    tree = spatial.KDTree(base_cor_tuples)

    road_count = 0
    for road in roads:
        # print(road)
        road_count += 1

        for i in range(len(road) - 1):
            cor_tuple = CoordinateUtil.getTupleWithStringCoordinate(road[i])
            cor_next_tuple = CoordinateUtil.getTupleWithStringCoordinate(road[i+1])
            print(cor_tuple, cor_next_tuple)
            nearestStartNode = BaseNodeMapper.get_Mapped_BaseNode(base_nodes, cor_tuple, tree, base_coordinate_list)
            nearestDestNode = BaseNodeMapper.get_Mapped_BaseNode(base_nodes, cor_next_tuple, tree, base_coordinate_list)
            if ((nearestStartNode != None and nearestDestNode != None) and (
                    nearestStartNode.get("nodeId") != nearestDestNode.get("nodeId"))):
                G.add_node(nearestStartNode.get("nodeId"), coordinate=nearestStartNode.get("coordinate"))
                G.add_node(nearestDestNode.get("nodeId"), coordinate=nearestDestNode.get("coordinate"))
                G.add_edge(nearestStartNode.get("nodeId"), nearestDestNode.get("nodeId"), weight=0)

    print("base node road graph nodes :-", G.number_of_nodes())
    return G