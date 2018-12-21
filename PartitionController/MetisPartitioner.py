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


def recursive_partition_by_levels(graph, levels):
    current_level = 1
    cut, partitions = metis_partition(graph, 2)
    partition1 = partitions[0]
    partition2 = partitions[1]
    graphA = build_partition_graph(graph, partition1)
    graphB = build_partition_graph(graph, partition2)

    while levels>current_level:
        cut, partitions = metis_partition(graphA, 2)
        partition1 = partitions[0]
        partition2 = partitions[1]
        graphA = build_partition_graph(graph, partition1)
        graphB = build_partition_graph(graph, partition2)

        cut, partitions = metis_partition(graphB, 2)
        partition1 = partitions[0]
        partition2 = partitions[1]
        graphA = build_partition_graph(graph, partition1)
        graphB = build_partition_graph(graph, partition2)
        current_level +=1

def metis_partition(graph, partition_count):
    print('metis partitioning...',)
    # G = nx.complete_graph(10)
    # print(nx.number_of_nodes(graph))
    # options = nxmetis.types.MetisOptions(contig=True, dbglvl=True, rtype=nxmetis.enums.MetisRType.default)
    partitionn_results = nxmetis.partition(graph, partition_count, edge_weight='trips', recursive=False)
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


def build_partition_graph(graph, partition):
    new_graph = graph.subgraph(partition)
    graphs = list(nx.connected_component_subgraphs(new_graph))
    selected_partitions = []
    # print(len(graphs))
    graphs.sort(key=lambda x: x.number_of_nodes(), reverse=True)
    for g in graphs:
        selected_partitions += g.nodes()
        if(g.number_of_nodes() < 1000):
            break
    # print(selected_partitions)
    selected_graph = graph.subgraph(selected_partitions)
    print(selected_graph.number_of_nodes())
    print(selected_graph.size(weight='trips'))
    return selected_graph

# edge_cuts = [-99356, -385837, -542899, -957088, -1791906]
# edge_cuts = [-99356, -385837, -542899, -957088, -1791906]


# edge_cuts = [-1208368, -385837, -542899, -957088, -1791906]