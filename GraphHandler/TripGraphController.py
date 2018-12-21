from scipy import spatial
from Utils import GraphUtils
from Utils import CoordinateUtil
import networkx as nx
from Utils import OSMNXutil

distance_Threshold = 0.0025


def combineWithRoadGraph(road_graph, trip_data):
    print("combining into road graph...")
    road_nodes, road_tuples = GraphUtils.getRoadCoordinateTuples(road_graph)
    count = 0
    trip_count = 0

    tree = spatial.KDTree(road_tuples)
    print(road_tuples)
    for index, row in trip_data.iterrows():
        start = row['pickup']
        dest = row['dropoff']
        start_tuple = [CoordinateUtil.getTupleWithStringCoordinate(start)]
        dest_tuple = [CoordinateUtil.getTupleWithStringCoordinate(dest)]
        start_index = tree.query(start_tuple)[1][0]
        start_distance = tree.query(start_tuple)[0][0]
        nearestStartNode= road_nodes[start_index-1]
        dest_index = tree.query(dest_tuple)[1][0]
        dest_distance = tree.query(dest_tuple)[0][0]
        # print(start_index ,start_distance, dest_index, dest_distance)

        nearestDestNode= road_nodes[dest_index-1]

        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)
                and (start_distance < distance_Threshold and dest_distance < distance_Threshold)):
            # road_graph = GraphUtils.addEdge(road_graph, nearestStartNode, nearestDestNode, 1)
            path = GraphUtils.get_trip_path(road_graph, nearestStartNode, nearestDestNode)
            if path != None:
                # print(path)
                GraphUtils.add_path_to_graph(road_graph, path)
                # break
                print(trip_count)
                trip_count += 1
        # print(tree.query(start_tuple)[1][0])
        if trip_count > 50000:
            break
        count +=1
    print(road_graph.number_of_nodes())
    print(road_graph.size(weight='weight'))
    print('trip count', trip_count)

    return road_graph


def createNYC_tripGraph(trip_data, nodes, coordinates):
    G = nx.Graph()
    print("craeting NYC trip graph...")
    cor_tuples = CoordinateUtil.getTupleListFromCoordinateList(coordinates)
    count = 0
    trip_count = 0

    tree = spatial.KDTree(cor_tuples)
    # print(road_tuples)
    for index, row in trip_data.iterrows():
        start = row['pickup']
        dest = row['dropoff']
        start_tuple = [CoordinateUtil.getTupleWithStringCoordinate(start)]
        dest_tuple = [CoordinateUtil.getTupleWithStringCoordinate(dest)]
        start_index = tree.query(start_tuple)[1][0]
        start_distance = tree.query(start_tuple)[0][0]
        # print(start_index)
        nearestStartNode= nodes[start_index]
        dest_index = tree.query(dest_tuple)[1][0]
        dest_distance = tree.query(dest_tuple)[0][0]
        # print(start_index ,start_distance, dest_index, dest_distance)
        nearestDestNode= nodes[dest_index]

        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)
                and (start_distance < distance_Threshold and dest_distance < distance_Threshold)):
            G = GraphUtils.addEdge(G, nearestStartNode, nearestDestNode, 1)
            trip_count += 1
        # print(tree.query(start_tuple)[1][0])
        if trip_count > 50000:
            break
        count +=1
    print(G.number_of_nodes())
    print(G.size(weight='weight'))
    print('trip count', trip_count)

    return G


def create_short_trip_graph(trip_data, nodes, coordinates):
    G = nx.Graph()
    print("craeting NYC trip graph...")
    cor_tuples = CoordinateUtil.getTupleListFromCoordinateList(coordinates)
    count = 0
    trip_count = 0

    tree = spatial.KDTree(cor_tuples)
    # print(road_tuples)
    for t in trip_data:
        start = t.get('pickup')
        dest = t.get('dropoff')
        start_tuple = [CoordinateUtil.getTupleWithStringCoordinate(start)]
        dest_tuple = [CoordinateUtil.getTupleWithStringCoordinate(dest)]
        start_index = tree.query(start_tuple)[1][0]
        start_distance = tree.query(start_tuple)[0][0]
        # print(start_index)
        nearestStartNode = nodes[start_index]
        dest_index = tree.query(dest_tuple)[1][0]
        dest_distance = tree.query(dest_tuple)[0][0]
        # print(start_index ,start_distance, dest_index, dest_distance)
        nearestDestNode = nodes[dest_index]

        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)
                and (start_distance < distance_Threshold and dest_distance < distance_Threshold)):
            G = GraphUtils.addEdge(G, nearestStartNode, nearestDestNode, 1)
            trip_count += 1
        # print(tree.query(start_tuple)[1][0])
        if trip_count > 50000:
            break
        count += 1
    print(G.number_of_nodes())
    print(G.size(weight='weight'))
    print('trip count', trip_count)

    return


def combineShortTripsWithRoadGraph(road_graph, trip_data):
    print("combining into road graph...")
    road_nodes, road_tuples = GraphUtils.getRoadCoordinateTuples(road_graph)
    count = 0
    trip_count = 0

    tree = spatial.KDTree(road_tuples)
    print(road_tuples)
    # for index, row in trip_data.iterrows():
    for t in trip_data:
        print(t)
        start = t.get('pickup')
        dest = t.get('dropoff')
        start_tuple = [CoordinateUtil.getTupleWithStringCoordinate(start)]
        dest_tuple = [CoordinateUtil.getTupleWithStringCoordinate(dest)]
        start_index = tree.query(start_tuple)[1][0]
        start_distance = tree.query(start_tuple)[0][0]

        nearestStartNode= road_nodes[start_index-1]
        dest_index = tree.query(dest_tuple)[1][0]
        dest_distance = tree.query(dest_tuple)[0][0]
        print(start_index ,start_distance, dest_index, dest_distance)

        nearestDestNode= road_nodes[dest_index-1]

        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)
                and (start_distance < distance_Threshold and dest_distance < distance_Threshold)):
            road_graph = GraphUtils.addEdge(road_graph, nearestStartNode, nearestDestNode, 1)
            trip_count += 1
        # print(tree.query(start_tuple)[1][0])
        if trip_count > 75000:
            break
        count +=1
    print(road_graph.number_of_nodes())
    print(road_graph.size(weight='weight'))
    print('trip count', trip_count)

    return road_graph



def combineWithOSMNXRoadGraph(road_graph, osmnx_graph, trip_data):
    print("combining into road graph...")
    # road_nodes, road_tuples = GraphUtils.getRoadCoordinateTuples(road_graph)
    count = 0
    trip_count = 0
    # road_short_graph = road_graph.copy()
    # road_long_graph = road_graph.copy()

    # tree = spatial.KDTree(road_tuples)
    # print(road_tuples)
    print(road_graph.edges(data=True))
    # nx.set_edge_attributes(road_graph, 'trips', 0)
    print(road_graph.edges(data=True))
    for index, row in trip_data.iterrows():
        start = row['pickup']
        dest = row['dropoff']
        start_tuple = CoordinateUtil.getTupleWithStringCoordinate(start)
        dest_tuple = CoordinateUtil.getTupleWithStringCoordinate(dest)

        nearestStartNode = OSMNXutil.get_nearest_node(osmnx_graph, start_tuple)
        nearestDestNode = OSMNXutil.get_nearest_node(osmnx_graph, dest_tuple)
        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)):
            # road_graph = GraphUtils.addEdge(road_graph, nearestStartNode, nearestDestNode, 1)
            path = OSMNXutil.get_path(osmnx_graph, nearestStartNode, nearestDestNode)
            # print(path)
            if path != None:
                # print(path)
                road_graph = GraphUtils.add_path_to_graph(road_graph, path)
                # if CoordinateUtil.isShortTrip(start_tuple, dest_tuple):
                #     road_short_graph = GraphUtils.add_path_to_graph(road_graph, path)
                # else:
                #     road_long_graph = GraphUtils.add_path_to_graph(road_long_graph, path)
                # break
                print(trip_count)
                trip_count += 1
        # print(tree.query(start_tuple)[1][0])
        if trip_count > 75000:
            break
        count +=1
    print(road_graph.number_of_nodes())
    print('road_graph', road_graph.size(weight='trips'))
    # print('short graph', road_short_graph.size(weight='trips'))
    # print('long trips', road_long_graph.size(weight='trips'))
    print('trip count', trip_count)

    return road_graph


def combineShortTripsWithOSMNXRoadGraph(road_graph, road_long_graph, osmnx_graph, trip_data):
    print("combining into road graph...")
    # road_nodes, road_tuples = GraphUtils.getRoadCoordinateTuples(road_graph)
    count = 0
    trip_count = 0
    short_trips = 0
    long_trips = 0
    road_long_graph = road_graph.copy()
    road_short_graph = road_graph.copy()

    # tree = spatial.KDTree(road_tuples)
    # print(road_tuples)
    nx.set_edge_attributes(road_graph, 'trips', 0)
    for index, row in trip_data.iterrows():
        start = row['pickup']
        dest = row['dropoff']
        start_tuple = CoordinateUtil.getTupleWithStringCoordinate(start)
        dest_tuple = CoordinateUtil.getTupleWithStringCoordinate(dest)

        nearestStartNode = OSMNXutil.get_nearest_node(osmnx_graph, start_tuple)
        nearestDestNode = OSMNXutil.get_nearest_node(osmnx_graph, dest_tuple)
        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)):
            # road_graph = GraphUtils.addEdge(road_graph, nearestStartNode, nearestDestNode, 1)
            path = OSMNXutil.get_path(osmnx_graph, nearestStartNode, nearestDestNode)
            # print(path)
            if path != None:
                print(path)
                if CoordinateUtil.isShortTrip(start_tuple, dest_tuple):
                    short_trips+=1
                    road_short_graph = GraphUtils.add_path_to_graph(road_short_graph, path)
                else:
                    long_trips +=1
                    road_long_graph = GraphUtils.add_path_to_graph(road_long_graph, path)
                # break
                print(trip_count, short_trips, long_trips)
                trip_count += 1
            # print(tree.query(start_tuple)[1][0])
        if trip_count > 75000:
            break
        count +=1
    print(road_graph.number_of_nodes())
    print('short trips', road_short_graph.size(weight='trips'))
    print('long trips', road_long_graph.size(weight='trips'))
    print('trip count', trip_count)

    return road_graph, road_long_graph


def combinePeekTripsWithOSMNXRoadGraph(road_graph, osmnx_graph, trip_data):
    print("combining into road graph...")
    # road_nodes, road_tuples = GraphUtils.getRoadCoordinateTuples(road_graph)
    count = 0
    trip_count = 0
    # road_short_graph = road_graph.copy()
    # road_long_graph = road_graph.copy()

    # tree = spatial.KDTree(road_tuples)
    # print(road_tuples)
    print(road_graph.edges(data=True))
    # nx.set_edge_attributes(road_graph, 'trips', 0)
    print(road_graph.edges(data=True))
    for t in trip_data:
        start = t.get('pickup')
        dest = t.get('dropoff')
        start_tuple = CoordinateUtil.getTupleWithStringCoordinate(start)
        dest_tuple = CoordinateUtil.getTupleWithStringCoordinate(dest)

        nearestStartNode = OSMNXutil.get_nearest_node(osmnx_graph, start_tuple)
        nearestDestNode = OSMNXutil.get_nearest_node(osmnx_graph, dest_tuple)
        if ((nearestStartNode != None and nearestDestNode != None) and (nearestStartNode != nearestDestNode)):
            # road_graph = GraphUtils.addEdge(road_graph, nearestStartNode, nearestDestNode, 1)
            path = OSMNXutil.get_path(osmnx_graph, nearestStartNode, nearestDestNode)
            # print(path)
            if path != None:
                # print(path)
                road_graph = GraphUtils.add_path_to_graph(road_graph, path)
                # if CoordinateUtil.isShortTrip(start_tuple, dest_tuple):
                #     road_short_graph = GraphUtils.add_path_to_graph(road_graph, path)
                # else:
                #     road_long_graph = GraphUtils.add_path_to_graph(road_long_graph, path)
                # break
                print(trip_count)
                trip_count += 1
        # print(tree.query(start_tuple)[1][0])
        if trip_count > 75000:
            break
        count +=1
    print(road_graph.number_of_nodes())
    print('road_graph', road_graph.size(weight='trips'))
    # print('short graph', road_short_graph.size(weight='trips'))
    # print('long trips', road_long_graph.size(weight='trips'))
    print('trip count', trip_count)

    return road_graph