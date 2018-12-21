import networkx as nx


def get_first_degree_vertex(graph):
    node_list = sorted(graph.degree(weight='trips'), key=lambda x: x[1])
    # print(node_list)
    for node in node_list:
        if node[1] > -1:
            print('dsadasdasd', node)
            return node[0]
    print('aaaaaaaaaaaaaa')


def get_initial_edge_cut(vertex, graph):
    cut = 0
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        # print(graph.get_edge_data(vertex, n))
        cut = cut + graph.get_edge_data(vertex, n)[0].get('trips')
    return cut


def calculate_gain(node, graph, graphA, graphB):
    gain = 0
    neighbours = graph.neighbors(node)
    for n in neighbours:
        print(graph.get_edge_data(node, n))
        if graphA.has_node(n):
            gain = gain + graph.get_edge_data(node, n)[0].get('trips')
        else:
            gain = gain - graph.get_edge_data(node, n)[0].get('trips')

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

def kwaypartition(graph, partition_coount):
    graphA = nx.Graph()
    graphB = graph.copy()

    start_vertex = get_first_degree_vertex(graph)
    graphA.add_node(start_vertex)
    graphB.remove_node(start_vertex)

    local_edge_cut = get_initial_edge_cut(start_vertex, graph)




