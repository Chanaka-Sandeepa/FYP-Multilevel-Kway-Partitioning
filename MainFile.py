from FileHandler import CSVReader
# from GraphHandler import RoadGraphController
from GraphHandler import TripGraphController
from PartitionController import RecursivePartitionController
# from PartitionController import NetworkXPartitions
# from Utils import GraphUtils
# from Utils import VisualizeUtil
# from GraphHandler import GraphMinimizer
from Utils import OSMNXutil
# from Utils import GraphEvaluator
from PartitionController import RecursivePartitionerTest
import networkx as nx
# from PartitionController import KWayPartition
# from PartitionController import MetisPartitioner
# from FileHandler import FileWriter
import time
# import  osmnx  as ox


# #
# base_node_list, base_coordinates = CSVReader.readBaseNodes('Resources/Roads/Colombo_Nodes.csv')
# road_cor_list = CSVReader.readRoadData('Resources/Roads/colomboTest.geojson')
# road_graph = RoadGraphController.create_roads_with_basenodes(road_cor_list, base_node_list, base_coordinates)
# # nx.write_graphml(road_graph, "TestGraphs/basenode_roadGraph.graphml")
# road_graph = nx.read_graphml("data/colombo_large.graphml")
# road_graph, osmnx_graph = OSMNXutil.get_colombo_graph_from_file()
# road_graph, osmnx_graph = OSMNXutil.get_manhatten_graph_from_file()
# # # ox.plot_graph(osmnx_graph)
# # tg = nx.read_graphml("data/manhatten1.graphml")
# # print('nodes', tg.number_of_nodes())
# # print('edges', tg.number_of_edges())
# #
# # # print(len(road_graph), len(osmnx_graph))
# # # # # # # #
# # # # short_trips, long_trips = CSVReader.readTripsForClassify('Resources/TripData/PickmeTrips.csv')
# # peak_trips, offpeak_trips = CSVReader.time_trip_classifier('Resources/TripData/PickmeTrips.csv')
# # trip_list = CSVReader.readTripData('Resources/TripData/PickmeTrips.csv')
# trip_list = CSVReader.readManhattenTripData('Resources/TripData/preprocessed_trips_discretised.csv')
# # # # # # # # # # # road_trip_graph = TripGraphController.combineShortTripsWithRoadGraph(road_graph, trip_list)
# # # short_trip_graph, road_long_trip_graph = TripGraphController.combineShortTripsWithOSMNXRoadGraph(road_graph, road_graph, osmnx_graph, trip_list)
# # # peakG = road_graph.copy()
# # # offpeakG = road_graph.copy()
# # # peak_trip_graph = TripGraphController.combinePeekTripsWithOSMNXRoadGraph(peakG, osmnx_graph, peak_trips)
# manhatten_trip_graph = TripGraphController.combineWithOSMNXRoadGraph(road_graph, osmnx_graph, trip_list)
# # offpeak_trip_graph = TripGraphController.combinePeekTripsWithOSMNXRoadGraph(offpeakG, osmnx_graph, offpeak_trips)
# # print(peak_trip_graph.size(weight='trips'), offpeak_trip_graph.size(weight='trips'))
# # # # road_trip_graph = TripGraphController.combineWithOSMNXRoadGraph(road_graph, osmnx_graph, trip_list)
# # # # # # # # # # # # pickME_TripG = TripGraphController.create_short_trip_graph(short_trips, base_node_list, base_coordinates)
# # # # # # # # # # # # nx.write_graphml(pickME_TripG, "TestGraphs/pickME_tripG_50000.graphml")
# # # # # # # # # # # # tg = nx.read_graphml("TestGraphs/pickMEminimized_trip_75000_new_to_40000_tripG2.graphml")
# # # # # # # # # # # # tg = nx.read_graphml("TestGraphs/pickME_tripG_50000.graphml")
# # # # nx.write_graphml(road_trip_graph, "TestGraphs/Osmnx_trip_75000_new.graphml")
# # nx.write_graphml(peak_trip_graph, "TestGraphs/peek_trips_new.graphml")
# # nx.write_graphml(offpeak_trip_graph, "TestGraphs/offpeek_trips_new.graphml")
# # # nx.write_graphml(road_short_graph, "TestGraphs/Osmnx_large_short_graph_75000.graphml")
# # # nx.write_graphml(road_long_graph, "TestGraphs/Osmnx_large_long_graph_75000.graphml")
# # # # ox.save_graphml(road_trip_graph, filename='Osmnx_trip_graph_50000.graphml')
# # # # tg = nx.read_graphml("TestGraphs/Osmnx_test_graph_20000.graphml")
# # # # print(tg.size(weight='trips'))
# # # tg = OSMNXutil.convert_to_simpleG(road_trip_graph)
# nx.write_graphml(manhatten_trip_graph, "TestGraphs/Manhatten_trips_50000.graphml")
# # #
# tg = nx.read_graphml("TestGraphs/Manhatten_trips_50000.graphml")
# # tg = OSMNXutil.convert_to_simpleG(tg)
#
# gs = nx.connected_component_subgraphs(tg)
# c = 0
# main_graph = []
# for a in gs:
#     main_graph = a
#     print(a.number_of_nodes(), a.size(weight='trips'))
#     c += 1
#     # VisualizeUtil.draw_edge_hist(main_graph)
#     # break
#
# # print('peak trips', len(peak_trips))
# print('sub G', c)
# # ########################################################################
# tg = nx.read_graphml("TestGraphs/Osmnx_trip_75000_new.graphml")
# print(tg.number_of_nodes(), tg.size(weight='trips'))
# minimized_graph = GraphMinimizer.random_match(tg)
# print(minimized_graph.number_of_nodes(), minimized_graph.size(weight='trips'))
# nx.write_graphml(minimized_graph, "TestGraphs/minimized_trip_75000_new_to_40000.graphml")

# minimizedG = nx.read_graphml("TestGraphs/minimized_large_trips_graph_75000.graphml")
# edges = minimizedG.edges(data=True)
# sorted_local_gains = sorted(edges, key=lambda k: k[2].get('trips'), reverse=True)
# c = 0
# for  s in sorted_local_gains:
#     print(s)
#     c +=1
#     if c == 100:
#         break
    # break
# gs = nx.connected_component_subgraphs(minimizedG)
# c = 0
# main_graph = []
# for a in gs:
#     main_graph = a
#     print(a.number_of_nodes(), a.size(weight='trips'))
#     c += 1
#     # VisualizeUtil.draw_edge_hist(main_graph)
#     # break
#
# print('peak trips', c)

#
# ##############################################################################################################

tg = nx.read_graphml("TestGraphs/Manhatten_trips_50000.graphml")
print(tg.edges(data=True))
cuts =[]
partitions =[]
previouse_cut = 1000
expected_edge_cut = 1000
for i in range(2, 6):
    print('Partition level', i)
    tg = nx.read_graphml("TestGraphs/Manhatten_trips_50000.graphml")
    # tg = nx.read_graphml("TestGraphs/minimized_weekendG_40000.graphml")
    # nx.set_edge_attributes(tg, 0, 'trips')
    # print(tg.edges(data=True))
    # tg = OSMNXutil.convert_to_simpleG(tg)
    #
    # gs = nx.connected_component_subgraphs(tg)
    # c = 0
    # main_graph = []
    # for a in gs:
    #     main_graph = a
    #     print(a.number_of_nodes(), a.size(weight='trips'))
    #     c += 1
    #     # VisualizeUtil.draw_edge_hist(main_graph)
    #     break

    # print('sub G', c)
    # print('main G weight', main_graph.size(weight = 'weight'))

    # mg = nx.read_graphml("TestGraphs/minimized_graph.graphml")
    # print('size', tg.size(weight='weight'), 'nodes', tg.number_of_nodes())
    # # sampleG = GraphUtils.getSampleGraph()
    # # #
    local_cut = 0
    for j in range (0,1):
        start = time.time()
        sub_partitions = []
        cut_list, sub_partitions, is_limit_exceeded = RecursivePartitionController.k_way_partition(tg, i, previouse_cut)
        local_cut += cut_list
    # if is_limit_exceeded:
    #     break
    avg_cut = local_cut
    cuts.append(avg_cut)
    previouse_cut = avg_cut
    partitions.append(sub_partitions)
    print('-----------------------------------------final_cuts', cuts)
    pcount = 0
    for p in sub_partitions:
        pcount += 1
        nx.write_graphml(p, "ManhattenPartitions/" + str(i + 1) + "/manhatten" + str(pcount) + ".graphml")
    # print('sub partition_count', len(sub_partitions), sub_partitions)
    # nx.write_graphml(sub_partitions[0], "PartitionedGraphs/minimized_trip_75000_new_to_40000_1.graphml")
    # nx.write_graphml(sub_partitions[1], "PartitionedGraphs/minimized_trip_75000_new_to_40000_2.graphml")
    # nx.write_graphml(sub_partitions[2], "PartitionedGraphs/minimized_trip_75000_new_to_40000_3.graphml")
    # nx.write_graphml(sub_partitions[3], "PartitionedGraphs/minimized_trip_75000_new_to_40000_4.graphml")
    # nx.write_graphml(sub_partitions[4], "PartitionedGraphs/minimized_trip_75000_new_to_40000_5.graphml")
    # nx.write_graphml(sub_partitions[5], "PartitionedGraphs/minimized_trip_75000_new_to_40000_6.graphml")
    # nx.write_graphml(sub_partitions[6], "PartitionedGraphs/minimized_trip_75000_new_to_40000_7.graphml")
    # nx.write_graphml(sub_partitions[7], "PartitionedGraphs/minimized_trip_75000_new_to_40000_8.graphml")
    # nx.write_graphml(sub_partitions[8], "PartitionedGraphs/minimized_trip_75000_new_to_40000_9.graphml")
    # nx.write_graphml(sub_partitions[9], "PartitionedGraphs/minimized_trip_75000_new_to_40000_10.graphml")
    # nx.write_graphml(sub_partitions[10], "PartitionedGraphs/minimized_trip_75000_new_to_40000_11.graphml")
    # nx.write_graphml(sub_partitions[11], "PartitionedGraphs/minimized_trip_75000_new_to_40000_12.graphml")
    # nx.write_graphml(sub_partitions[12], "PartitionedGraphs/minimized_trip_75000_new_to_40000_13.graphml")
    # nx.write_graphml(sub_partitions[13], "PartitionedGraphs/minimized_trip_75000_new_to_40000_14.graphml")
    # nx.write_graphml(sub_partitions[14], "PartitionedGraphs/minimized_trip_75000_new_to_40000_15.graphml")
    # nx.write_graphml(sub_partitions[15], "PartitionedGraphs/minimized_trip_75000_new_to_40000_16.graphml")
    # nx.write_graphml(sub_partitions[16], "PartitionedGraphs/minimized_trip_75000_new_to_40000_17.graphml")
    # nx.write_graphml(sub_partitions[17], "PartitionedGraphs/minimized_trip_75000_new_to_40000_18.graphml")
    # nx.write_graphml(sub_partitions[18], "PartitionedGraphs/minimized_trip_75000_new_to_40000_19.graphml")
    # nx.write_graphml(sub_partitions[19], "PartitionedGraphs/minimized_trip_75000_new_to_40000_20.graphml")
    expected_edge_cut += 3000

    # if cut_list > 46000:
    #     break
    # break
print('round count', len(partitions))
end = time.time()
print('full time', end - start)
print(cuts)
# print(partitioned_graphs)
# # VisualizeUtil.draw_edge_cut_histo(cuts)
#
# st_100000 = [13651, 18375, 22707, 26658, 28310, 28960, 30810, 30266, 32095, 31962, 32874, 32145, 33809, 32282, 32222, 35249, 30422, 35524, 30504]
#
# #

# Evaluate graphs
# tg = nx.read_graphml("TestGraphs/Osmnx_trip_75000_new.graphml")
# # tg = nx.read_graphml("TestGraphs/minimized_trip_75000_new_to_40000.graphml")
# # OSMNXutil.metis_partition(tg)
# #
# # lfrG = GraphEvaluator.generateLFR()
# # weightedG = RecursivePartitionerTest.addWeightToGraph(lfrG)
# tg = OSMNXutil.convert_to_simpleG(tg)
#
# MetisPartitioner.metis_partition(tg, 8)

# g = nx.read_graphml("TestGraphs/Osmnx_large_trips_graph_75000.graphml")
# print('multi weight', g.size('trips'))
# # print('graph nodes', g.number_of_nodes())
# # print('graph edges', g.number_of_edges())
# simple_g = OSMNXutil.convert_to_simpleG(g)
# print('simple weight', simple_g.size('trips'))
# # MetisPartitioner.partition_rounds(simple_g, 5)
# print('nodes', simple_g.number_of_nodes())
# cut, partitions = MetisPartitioner.metis_partition(simple_g, 3)
# partition1 = partitions[0]
# partition2 = partitions[1]
# partition3 = partitions[2]
# # partition3 = partitions[3]
# graphA = MetisPartitioner.build_partition_graph(simple_g, partition1)
# graphB = MetisPartitioner.build_partition_graph(simple_g, partition2)
# graphB = MetisPartitioner.build_partition_graph(simple_g, partition3)
#
# marked_graph = GraphUtils.markPartitionNumber(simple_g, partitions)
# nx.write_graphml(marked_graph, "TestGraphs/Osmnx_large_trips_graph_75000_marked8.graphml")

# FileWriter.write_partitions(partitions)
# partitionedGraphs, edgeCut, isLimit = RecursivePartitionerTest.k_way_partition(lfrG, 3, 100)

# edge_cuts = [-657225, -2891467, -2506293, -5601881, -6618236, 6478536, 8651635, 11248227]
# a =[]
# for  e in edge_cuts:
#     a.append((abs(e)/9885858)*100)
# print(a)

# [12.223198026918858, 9.918127490805553, 24.73436296576382, 44.40932693955345, 66.9465007488475, 96.79752632497856, 113.78098896423559]

# Evaluate graph
# partitioned_graph1 = nx.read_graphml("PartitionedGraphs/2/minimized_trip_75000_new_to_40000_1.graphml")
# partitioned_graph2 = nx.read_graphml("PartitionedGraphs/2/minimized_trip_75000_new_to_40000_2.graphml")
# partition_list = [partitioned_graph1, partitioned_graph2]
#
# # tg = nx.read_graphml("data/colombo_large.graphml")
#
# marked_nodes = GraphUtils.markUsingPartitionList(partition_list)
# test_trip_list = CSVReader.read_test_trips('Resources/TripData/PickmeTrips.csv')
# # # print(test_trip_list)
# # marked_graph = nx.read_graphml("MarkedGraphs/Osmnx_large_trips_graph_75000_marked3.graphml")
# road_graph = nx.read_graphml("data/colombo_large.graphml")
# # print(road_graph.number_of_edges())
# # road_g, osmnx_graph = OSMNXutil.get_colombo_graph_from_file()
# GraphEvaluator.test_trip_cut(marked_nodes, road_graph, test_trip_list)


# tgorig = nx.read_graphml("TestGraphs/Osmnx_trip_75000_new.graphml")
# tg = nx.read_graphml("TestGraphs/minimized_trip_75000_new_to_40000.graphml")
# edges = tg.edges(data=True)
# print(len(edges), tg.size(weight='trips'), tgorig.size(weight='trips'))
# count = 0
# for e in edges:
#     # print(e)
#     count += 1
#
#     # if e[2].get('trips')>0:
#         # print(e)
# print(tg.size(weight='trips'))
# print(count)


metis_cut = [1284, 3202, 13218]