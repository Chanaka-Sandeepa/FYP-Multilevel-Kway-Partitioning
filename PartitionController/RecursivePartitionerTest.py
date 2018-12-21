import networkx as nx
from Utils import GraphUtils
from random import randint


partitioned_graphs =[]
partitioned_weights =[]
partition_limit = 2
edge_cuts = []


# original_graph_weight = None
def addWeightToGraph(graph):
    c = 0
    for u, v, a in graph.edges(data=True):
        # print (u, v, a)
        graph[u][v].update(weight=randint(0, 15))
        c += 1
    # print(c)
    # nx.set_edge_attributes(graph, 1, 'weight')

    return graph


def add_edge(vertex, graph, graphA, graphB):
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        if n in graphA:
            graphA.add_edge(n, vertex,
                            weight=graph.get_edge_data(n, vertex).get('weight'))


def get_initial_edge_cut(vertex, graph):
    cut = 0
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        print(graph.get_edge_data(vertex,n))
        cut = cut + graph.get_edge_data(vertex, n)['weight']
    return cut


def is_in_gains(node, gains,graph, graphA, graphB):
    for gain in gains:
        for g in gain:
            if g.get("node") == node:
                current_gain = calculate_gain(node, graph, graphA, graphB)
                if current_gain > g.get("gain"):
                    gain.remove(g)
                    return False
                return True
    return False


def calculate_gain(node, graph, graphA, graphB):
    gain = 0
    neighbours = graph.neighbors(node)
    for n in neighbours:
        if graphA.has_node(n):
            gain = gain + graph.get_edge_data(node, n).get('weight')
        else:
            gain = gain - graph.get_edge_data(node, n).get('weight')

    return gain


def prepare_gains_prority(gains, vertex, graph, graphA, graphB):
    local_gains =[]
    neighbours = graph.neighbors(vertex)

    for i in range(len(gains)):
        gain = gains[i]
        for j in range(len(gain)):
            gains[i][j] = {"node": gain[j].get('node'), "gain": calculate_gain(gain[j].get('node'), graph, graphA, graphB)}
        gains[i] = sorted(gains[i], key=lambda k: k['gain'], reverse=True)

    for n in neighbours:
        if n not in graphA:
            if not is_in_gains(n, gains, graph, graphA, graphB):
                local_gains.append({"node":n, "gain":calculate_gain(n, graph, graphA, graphB)})

    sorted_local_gains = sorted(local_gains, key=lambda k: k['gain'], reverse=True)
    gains.append(sorted_local_gains)

    return gains


def k_way_partition(graph, limit, previouse_cut):
    print('Partitioning the graph...')
    edges = graph.edges(data=True)
    print(edges)
    print(len(edges))
    partition_count = 0
    global partition_limit
    global edge_cuts
    edge_cuts = []
    cut_list=[]
    final_partitioned_graphs = []
    partition_limit = limit
    print('previouse', previouse_cut)
    original_graph_weight = graph.size(weight='weight')
    # original_graph_weight = graph.size(weight='weight') - (previouse_cut + 2000)
    if original_graph_weight > 10:
        final_partitioned_graphs, cut_list, is_limit_exceeded = recursive_bisection(graph, partition_count, original_graph_weight)
    return cut_list, final_partitioned_graphs, is_limit_exceeded


def get_next_node(gains):
    min_node = {'gain': -1000000000, 'node': 100000000000}
    # print(gains)
    for g in gains:
        if len(g) >0:
            # print('enterd')
            local_min_node = g[0]
            # print(min_node.get('gain'), local_min_node.get('gain'))
            if min_node.get('gain') < local_min_node.get('gain'):
                # print('enter iii')
                min_node = local_min_node

    # remove selected node
    for gain in gains:
        for g in gain:
            if g == min_node:
                # print(len(gain))
                gain.remove(min_node)
                if(len(gain) == 0):
                    # print('removed')
                    gains.remove(gain)
                break
    # print(min_node)

    return min_node


def recursive_bisection(graph, partition_count, original_graph_weight):

    # total_graph_weight = graph.size(weight='weight')
    graphA = nx.Graph()
    graphB = graph.copy()
    gains = []
    count =0
    partition_count += 1

    # random_vertex = GraphUtils.get_random_vertex(graph)
    random_vertex = GraphUtils.get_first_degree_vertex(graph)
    # random_vertex = GraphUtils.get_highest_degree_vertex(graph)
    graphA.add_node(random_vertex)
    # print(random_vertex)
    # print(graphB.number_of_nodes())
    # print(graphA.number_of_nodes())
    graphB.remove_node(random_vertex)
    local_edge_cut = get_initial_edge_cut(random_vertex, graph)

    gains = prepare_gains_prority(gains, random_vertex, graph, graphA, graphB)
    # print(gains)

    while (graphA.size(weight='weight') + (local_edge_cut*(1/(partition_limit+1))) ) < ((original_graph_weight)*(1/(partition_limit+1))):
    # while (graphA.size(weight='weight') + local_edge_cut/2 ) < ((original_graph_weight)/2):
    # while graphB.number_of_nodes() > graph.number_of_nodes()*(1/(partition_limit+1)):
        print(graphA.size(weight='weight'),((original_graph_weight)/2), graphB.size(weight='weight'), local_edge_cut)
        # print(gains)
        if graphB.number_of_nodes() < 10:
            print('dddddddddddddddddddddddddddddddddddddddddddddddd')
            return partitioned_graphs, sum(edge_cuts), True
        max_gain_entry = get_next_node(gains)
        max_gain_vertex = max_gain_entry.get('node')
        if max_gain_entry == {'gain': -1000000000, 'node': 100000000000}:
            print('ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
            return partitioned_graphs, sum(edge_cuts), True
        # print(max_gain_entry)
        local_edge_cut = local_edge_cut - max_gain_entry.get('gain')
        graphA.add_node(max_gain_vertex)
        # print(graphA.number_of_nodes(), graphB.number_of_nodes())

        graphB.remove_node(max_gain_vertex)
        add_edge(max_gain_vertex, graph, graphA, graphB)

        gains = prepare_gains_prority(gains, max_gain_vertex, graph, graphA, graphB)

        count += 1
        if count > (graph.number_of_nodes() * 2):
            print('aaaaaaaaaa')
            # break
        elif len(gains) == 0:
            vertex = GraphUtils.get_random_vertex(graphB)
            print('v', vertex)
            gains.append({"node": vertex, "gain": calculate_gain(vertex, graph, graphA, graphB)})

    edge_cuts.append(local_edge_cut)
    partitioned_weights.append({graphA.size(weight='weight'), graphB.size(weight="weight")})

    if partition_count < partition_limit:
        print('partition', partition_count, 'of', partition_limit+1)
        # print('edge_cuts', edge_cuts, 'partition_size', graphB.size(weight='weight'))
        partitioned_graphs.append(graphA.size(weight='weight'))
        # if graphB.size(weight='weight')>100:
        recursive_bisection(graphB, partition_count, original_graph_weight)
        # else:
        #     partitioned_graphs.append(graphB.size(weight='weight'))
        # recursive_bisection(graphB, partition_count)
    elif partition_count == partition_limit:
        print('partition', partition_count+1, 'of', partition_limit + 1)
        print('edge_cuts', edge_cuts, 'partition_size', graphB.size(weight='weight'))
        print('edge_cuts',edge_cuts, 'edge_cut_sum', sum(edge_cuts), 'partition_size', graphA.size(weight='weight'))
        partitioned_graphs.append(graphB.size(weight='weight'))
        partitioned_graphs.append(graphA.size(weight='weight'))
        # partitioned_graphs.append(graphB)
    else:
        # print(partitioned_graphs)
        return partitioned_graphs, False

    # print('edge_cut', local_edge_cut)
    # print(edge_cuts)
    return partitioned_graphs, sum(edge_cuts), False



# [16802]