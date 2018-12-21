from FileHandler import CSVReader
import pandas as pd
import numpy
import networkx as nx
from Utils import OSRMUtil
from PartitionController import RecursivePartitionController

devide_count = 5


def read_manhatten_nodes(file):
    base_node_list, base_coordinates = CSVReader.readBaseNodes(file)
    # print(base_node_list)
    # print(base_coordinates)
    return base_node_list, base_coordinates

def readManhattenTripData(filePath):
    # trip_columns = ['trips.pickuplatitide', 'trips.pickuplongitude', 'trips.droplatitude', 'trips.droplongitude']
    print('Reading trip data ...')
    trip_data = pd.read_csv(filePath, header=None)
    print(len(trip_data))
    trip_data = trip_data[:100000]
    trip_data = trip_data.dropna(how='any')
    # print(trip_data)
    return trip_data

def devide_trips(trips, node_partitions):
    print('Deviding trips into regions')
    devided_trips = []
    selected_trips = []

    for partition in node_partitions:
        partition_trips = []
        for index, row in trips.iterrows():
            # print(row)
            pick_node = row[1]
            drop_node = row[4]
            if all(x in partition for x in [str(pick_node), str(drop_node)]):
                partition_trips.append(row)
                selected_trips.append(index)
                trips = trips.drop(index)
        devided_trips.append(partition_trips)

    remaining_trips = trips
    print('selected trips', str(len(devided_trips[0]) + len(devided_trips[1]) + len(devided_trips[2]) + len(devided_trips[3])+ len(devided_trips[4])))
    print('remaining trips', len(remaining_trips))
    remaining_trips.to_csv('remain_requests', header=None, index=False)

    i=1
    for d in devided_trips:
        df = pd.DataFrame(data=d)
        df = df.reset_index(drop=True)
        # print(df)
        df.to_csv('requests'+str(i), header=None, index=False)
        i+=1
        # break

    return devided_trips


def devide_nodes(nodes):
    partitioned_nodes = []
    node_limit = len(nodes)/devide_count
    region_node_list = []
    print(len(nodes))
    for n in nodes:
        region_node_list.append(n)
        if len(region_node_list)>node_limit:
            partitioned_nodes.append(region_node_list)
            region_node_list = []
    partitioned_nodes.append(region_node_list)

    print(len(partitioned_nodes[0]), len(partitioned_nodes[1]), len(partitioned_nodes[2]))
    return partitioned_nodes


def create_trip_graph(trips):
    print("Creating roads graph...")
    G = nx.Graph()
    count = 0

    for index, row in trips.iterrows():
        u = row[1]
        v = row[4]
        G.add_node(u)
        G.add_node(v)
        if (G.has_edge(u, v)):
            trips = G.get_edge_data(u, v).get('trips')
            if (trips == None):
                trips = 0
            G.remove_edge(u, v)
            G.add_edge(u, v, trips=trips + 1)
        else:
            G.add_edge(u, v, trips=1)

    # GraphUtils.draw_graph(G)
    print("road graph nodes :-", G.number_of_nodes())

    gs = nx.connected_component_subgraphs(G)
    c = 0
    for a in gs:
        c += 1
        print(a.number_of_nodes())
        nx.write_graphml(a, "Manhatten_trips_100000.graphml")
        break
    print('sub in roadG', c)

    # mainTest.set_road_corList(road_cor_list)
    return G

def partition_graph():
    g = nx.read_graphml("Manhatten_trips_100000.graphml")
    print('weight', g.size(weight= 'trips'))
    cut_list, sub_partitions, is_limit_exceeded = RecursivePartitionController.k_way_partition(g, devide_count-1, 1000)

    print(sub_partitions)
    return sub_partitions

def write_node_coordinates(partitions, cordinates):
    excel_data = []
    colors = ['red', 'blue', 'green', 'yellow']
    color_index = 0
    selected_nodes = []

    for p in partitions:
        nodes = list(p)
        for i in range(len(nodes)):
            if nodes[i] in selected_nodes:
                print(nodes[i], colors[color_index])
                break
            # print(colors[color_index])
            cor = cordinates[i]
            lat = cor.split(',')[0]
            lon = cor.split(',')[1]
            selected_nodes.append(nodes[i])
            excel_data.append([lat, lon, 'circle1', colors[color_index]])
        color_index += 1
        print(nodes[i], selected_nodes[0])

    df = pd.DataFrame(data=excel_data)
    df.to_csv('Partition_coordinates', header=None, index=False)

def get_coordinates_for_partitions(coordinates):
    p1 = nx.read_graphml("../ManhattenPartitions/4/manhatten1.graphml")
    p2 = nx.read_graphml("../ManhattenPartitions/4/manhatten2.graphml")
    p3 = nx.read_graphml("../ManhattenPartitions/4/manhatten3.graphml")
    p4 = nx.read_graphml("../ManhattenPartitions/4/manhatten4.graphml")
    partition_list = [p1,p2, p3, p4]
    write_node_coordinates(partition_list, coordinates)

node_list, coordinates = read_manhatten_nodes('../DemoData/nodeList.csv')
# partitioned_nodes = devide_nodes(node_list)
#
# trips = readManhattenTripData('../DemoData/requestData.csv')
# #
# # devided_trips = devide_trips(trips, partitioned_nodes)
# #
# # # matrix_devider('../DemoData/week.csv')
# # G = create_trip_graph(trips)
#
# partitoned_graphs = partition_graph()
# i = 1
# partitioned_nodes = []
# for p in partitoned_graphs:
#     nx.write_graphml(p, "Manhatten_partition"+str(i)+".graphml")
#     i +=1
#     partitioned_nodes.append(p.nodes())
#
#
# devided_trips = devide_trips(trips, partitioned_nodes)

get_coordinates_for_partitions(coordinates)
