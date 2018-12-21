import networkx as nx
from networkx.algorithms import community

def getBiPartitions(graph):
    partitions = community.kernighan_lin_bisection(graph, partition=None, max_iter=10, weight='weight')
    p = ({3, 4,5, 6, 7}, {1, 2})
    print(partitions)
    print(community.performance(graph, partitions))