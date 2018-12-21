import networkx as nx
from Utils import GraphUtils
from Utils import VisualizeUtil

partitioned_graphs =[]
partitioned_weights =[]
partition_limit = 2
edge_cuts = []
sub_graphs = []
isSecondRound = False
isThirdRound = False


# original_graph_weight = None


def add_edge_old(vertex, graph, graphA, graphB):
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        if n in graphA:
            # print(graph.get_edge_data(n, vertex))
            if len(graph.get_edge_data(n, vertex)) > 1:
                graphA.add_edge(n, vertex,
                                trips=graph.get_edge_data(n, vertex)[1].get('trips'))
            else:
                graphA.add_edge(n, vertex,
                                trips=graph.get_edge_data(n, vertex)[0].get('trips'))
            # print(graphA.get_edge_data(n, vertex))

def add_edge(vertex, graph, graphA, graphB):
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        if n in graphA:
            # print(graph.get_edge_data(n, vertex))
            if len(graph.get_edge_data(n, vertex)) > 1:
                graphA.add_edge(n, vertex,
                                trips=graph.get_edge_data(n, vertex).get('trips'))
            else:
                graphA.add_edge(n, vertex,
                                trips=graph.get_edge_data(n, vertex).get('trips'))
            # print(graphA.get_edge_data(n, vertex))


def get_initial_edge_cut_old(vertex, graph):
    cut = 0
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        print(graph.get_edge_data(vertex, n))
        cut = cut + graph.get_edge_data(vertex, n)[0].get('trips')
    return cut

def get_initial_edge_cut(vertex, graph):
    cut = 0
    neighbours = graph.neighbors(vertex)
    for n in neighbours:
        print(graph.get_edge_data(vertex, n))
        cut = cut + graph.get_edge_data(vertex, n).get('trips')
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


def calculate_gain_old(node, graph, graphA, graphB):
    gain = 0
    neighbours = graph.neighbors(node)
    for n in neighbours:
        # print(graph.get_edge_data(node, n))
        if graphA.has_node(n):
            if len(graph.get_edge_data(node, n)) > 1:
                gain = gain + graph.get_edge_data(node, n)[1].get('trips')
            else:
                gain = gain + graph.get_edge_data(node, n)[0].get('trips')
        else:
            if len(graph.get_edge_data(node, n)) > 1:
                gain = gain - graph.get_edge_data(node, n)[1].get('trips')
            else:
                gain = gain - graph.get_edge_data(node, n)[0].get('trips')

    return gain

def calculate_gain(node, graph, graphA, graphB):
    gain = 0
    neighbours = graph.neighbors(node)
    for n in neighbours:
        # print(graph.get_edge_data(node, n))
        if graphA.has_node(n):
            if len(graph.get_edge_data(node, n)) > 1:
                gain = gain + graph.get_edge_data(node, n).get('trips')
            else:
                gain = gain + graph.get_edge_data(node, n).get('trips')
        else:
            if len(graph.get_edge_data(node, n)) > 1:
                gain = gain - graph.get_edge_data(node, n).get('trips')
            else:
                gain = gain - graph.get_edge_data(node, n).get('trips')

    return gain

def check_islands(graph):
    gs = nx.connected_component_subgraphs(graph)
    c = 0
    main_graph = []
    main_graphs = []
    sorted_islands = sorted(gs, key=lambda k: k.number_of_nodes(), reverse=True)

    for a in sorted_islands:
        # main_graph = a
        print(a.number_of_nodes(), a.size(weight='trips'))
        main_graphs.append(a)
        c += 1
        # VisualizeUtil.draw_edge_hist(main_graph)
        if c ==2:
            main_graph = nx.compose_all(main_graphs)
            # break

    # print('peak trips', len(peak_trips))
    print('sub G', c)
    return main_graph


def get_single_island(graph):
    gs = nx.connected_component_subgraphs(graph)
    c = 0
    main_graph = []
    main_graphs = []
    sorted_islands = sorted(gs, key=lambda k: k.number_of_nodes(), reverse=True)

    for a in sorted_islands:
        # main_graph = a
        print(a.number_of_nodes(), a.size(weight='trips'))
        return a
    #     main_graphs.append(a)
    #     c += 1
    #     # VisualizeUtil.draw_edge_hist(main_graph)
    #     if c ==2:
    #         main_graph = nx.compose_all(main_graphs)
    #         # break
    #prepare_gainspartition1_prorityprepare_gainspartition1_prority
    # # print('peak trips', len(peak_trips))
    # print('sub G', c)
    # return main_graph


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
    # print(gains)
    return gains


def k_way_partition(graph, limit, previouse_cut):
    print('Partitioning the graph...')
    partition_count = 0
    global partition_limit
    global edge_cuts
    edge_cuts = []
    cut_list=[]
    final_partitioned_graphs = []
    partition_limit = limit
    print('previouse', previouse_cut)
    original_graph_weight = graph.size(weight='trips')
    # original_graph_weight = graph.size(weight='trips') - (previouse_cut + 2000)
    if original_graph_weight > 10:
        final_partitioned_graphs, cut_list, is_limit_exceeded = recursive_bisection(graph, partition_count, original_graph_weight)
        print('partition1', final_partitioned_graphs[0].number_of_nodes(), final_partitioned_graphs[0].size(weight='trips'))
        print('partition2', final_partitioned_graphs[1].number_of_nodes(), final_partitioned_graphs[1].size(weight='trips'))
        # global isSecondRound
        # isSecondRound = True
        # remaining_graph = final_partitioned_graphs[1]
        # final_partitioned_graphs, cut_list, is_limit_exceeded = recursive_bisection(remaining_graph, partition_count, original_graph_weight)
        # global isThirdRound
        # isSecondRound = True
        # remaining_graph = final_partitioned_graphs[1]
        # final_partitioned_graphs, cut_list, is_limit_exceeded = recursive_bisection(remaining_graph, partition_count,original_graph_weight)
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
    edge_cut_variation = []
    nodes_added = []
    global isSecondRound

    total_graph_weight = graph.size(weight='trips')
    print('total weight', total_graph_weight)
    print('nodes', graph.number_of_nodes())
    graphA = nx.Graph()
    graphB = graph.copy()
    gains = []
    count =0
    partition_count += 1

    # random_vertex = GraphUtils.get_random_vertex(graph)
    random_vertex = GraphUtils.get_first_degree_vertex(graph)
    # random_vertex = GraphUtils.get_highest_degree_vertex(graph)
    graphA.add_node(random_vertex)
    # print(random_vertex)partition1
    # print(graphB.number_of_nodes())
    # print(graphA.number_of_nodes())
    graphB.remove_node(random_vertex)
    local_edge_cut = get_initial_edge_cut(random_vertex, graph)

    gains = prepare_gains_prority(gains, random_vertex, graph, graphA, graphB)
    # print(gains)

    # while (graphA.size(weight='trips') ) < ((original_graph_weight)*(1/(partition_limit+1))):
    # while (graphA.size(weight='trips') + local_edge_cut/2 ) < ((original_graph_weight)/2):
    # while (True):
    while graphA.number_of_nodes() < graph.number_of_nodes()*(1/(partition_limit+1)):
        # print(graphA.size(weight='trips'),((original_graph_weight)/3), graphB.size(weight='trips'), local_edge_cut)
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

        # ###################################### for edge cut variation graph ################################
        edge_cut_variation.append(local_edge_cut)
        nodes_added.append(graphA.number_of_nodes())
        ######################################################################################################

        graphB.remove_node(max_gain_vertex)
        add_edge(max_gain_vertex, graph, graphA, graphB)

        gains = prepare_gains_prority(gains, max_gain_vertex, graph, graphA, graphB)
        # if(local_edge_cut >11000 and not isSecondRound):
        #     print('break from elbow point')
        #     VisualizeUtil.draw_histo(nodes_added, edge_cut_variation, 'nodes added', 'edge cut',
        #                              'edge ut variaton vs nodes added')
        #     break
        # elif (local_edge_cut >20000 and not isThirdRound):
        #     print('break from elbow point')
        #     VisualizeUtil.draw_histo(nodes_added, edge_cut_variation, 'nodes added', 'edge cut',
        #                      'edge ut variaton vs nodes added')
        #     break
        # elif (graphB.number_of_nodes()<12):
        #     print('break from elbow point')
        #     VisualizeUtil.draw_histo(nodes_added, edge_cut_variation, 'nodes added', 'edge cut',
        #                      'edge ut variaton vs nodes added')
        #     break
        count += 1
        if count > (1000000):
            print('aaaaaaaaaa')

            break
        elif len(gains) == 0:
            vertex = GraphUtils.get_random_vertex(graphB)
            print('v', vertex)
            gains.append({"node": vertex, "gain": calculate_gain(vertex, graph, graphA, graphB)})

    edge_cuts.append(local_edge_cut)
    partitioned_weights.append({graphA.size(weight='trips'), graphB.size(weight="trips")})

    if partition_count < partition_limit:
        print('partition', partition_count, 'of', partition_limit+1)
        # print('edge_cuts', edge_cuts, 'partition_size', graphB.size(weight='weight'))
        partitioned_graphs.append(graphA.size(weight='trips'))
        sub_graphs.append(graphA)
        # if graphB.size(weight='weight')>100:
        # main_graph = check_iprepare_gainspartition1_prorityslands(graphB)
        main_graph = get_single_island(graphB)
        recursive_bisection(main_graph, partition_count, original_graph_weight)
        # else:
        #     partitioned_graphs.append(graphB.size(weight='weight'))
        # recursive_bisection(graphB, partition_count)
    elif partition_count == partition_limit:
        print('partition', partition_count+1, 'of', partition_limit + 1)
        print('edge_cuts', edge_cuts, 'partition_size', graphB.size(weight='trips'))
        print('edge_cuts',edge_cuts, 'edge_cut_sum', sum(edge_cuts), 'partition_size', graphA.size(weight='trips'))
        # graphB = check_islands(graphB)
        graphB = get_single_island(graphB)

        # graphA = check_islands(graphA)
        partitioned_graphs.append(graphB.size(weight='trips'))
        partitioned_graphs.append(graphA.size(weight='trips'))
        sub_graphs.append(graphA)
        sub_graphs.append(graphB)
        # partitioned_graphs.append(graphB)
    else:
        print(partitioned_graphs)
        return partitioned_graphs, False

    # print('edge_cut', local_edge_cut)
    # print(edge_cuts)
    return sub_graphs, sum(edge_cuts), False



# 5443757

# cuts = [ 288, 13180, 48279, 81436, 94063, 93474, 80405, 78398, 73318, 71244, 64341, 94604, 52285]
# cuts2 = [ 288, 13180, 70581, 70849, 105314, 92568, 67680, 67273, 77447, 82643, 65838, 49078, 52151, 52632, 83354, 64301, 62764, 85899, 69888]
refined_cuts = [295, 626, 2791, 1806, 2881, 5438, 6449, 5086, 5062, 5286, 7210, 9056, 9880, 11959, 12711, 13760, 13984]

# metis_cut = [1284, 3202, 13218]

perc = []
for c in refined_cuts:
    perc.append((c*5/3326609)*100)

print(perc)

