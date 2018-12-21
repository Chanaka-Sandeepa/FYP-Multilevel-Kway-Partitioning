import nxmetis
import networkx as nx
# import nxmetis.types.MetisOptions
from networkx.algorithms import community

def partition_rounds(graph, rounds):
    edge_cuts=[]
    for i in range (1, rounds):
        print('partition round - ',pow(2, i))
        cut, partitions = metis_partition(graph, pow(2, i))
        # print('coverage', community.coverage(graph, partitions))
        # refined_partitions = refine_partitions(graph, partitions)
        # print('refined coverage', community.coverage(graph, refined_partitions))
        edge_cuts.append(cut)

    print(edge_cuts)

def metis_partition(graph, partition_count):
    print('metis partitioning...',)
    # G = nx.complete_graph(10)
    # print(nx.number_of_nodes(graph))
    options = nxmetis.types.MetisOptions(ptype= nxmetis.enums.MetisPType.kway)
    partitionn_results = nxmetis.partition(graph, partition_count, edge_weight='trips')
    cut = partitionn_results[0]
    partitions = partitionn_results[1]
    print(cut, len(partitions))
    return cut, partitions


def refine_partitions(graph, partitions):
    refined_partitions = []
    for i in range(len(partitions) - 1):
        # print[a[i], a[i + 1]]
        partition1 = partitions[i]
        partition2 = partitions[i+1]
        kl_refinedPartitions = community.kernighan_lin_bisection(graph, [partition1, partition2], 5, weight='weight')
        refined_partitions.append(kl_refinedPartitions[0])
    refined_partitions.append(kl_refinedPartitions[1])
    return refined_partitions


# edge_cuts = [-99356, -385837, -542899, -957088, -1791906]
# edge_cuts = [-99356, -385837, -542899, -957088, -1791906]