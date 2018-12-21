import matplotlib.pyplot as plt2
import numpy as np


def draw_histo(x_list, y_list, x_lable, y_lable, title):
    plt2.xlabel(x_lable)
    plt2.ylabel(y_lable)
    plt2.title(title)
    plt2.xticks(x_list)
    list2 = range(0, y_list[-1] + 1000, 2000)
    y_lables = list(range(0 , 50000, 2000))
    plt2.yticks(y_lables)
    plt2.bar(x_list, y_list, color='b', width= 0.4)
    plt2.plot(x_list, y_list, color='r')
    plt2.show()


def draw_multibar_histo(x_list, y_list1, y_list2, x_lable, y_lable, title):
    fig, ax = plt2.subplots()

    p1 = ax.bar(x_list, y_list1, 0.4, color='r', yerr=x_list)

    p2 = ax.bar(x_list, y_list2, 0.4,
                color='y', yerr=x_list)

    ax.set_title('Scores by group and gender')
    # ax.set_xticks(y_list1)
    # ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))

    ax.legend((p1[0], p2[0]), ('Men', 'Women'))
    # ax.yaxis.set_units(inch)
    ax.autoscale_view()

    plt2.show()


def draw_degree_hist(graph):
    degree_list = sorted(graph.degree(weight='weight'), key=lambda x: x[1], reverse=True)
    max_degree = degree_list[0][1]
    min_degree = degree_list[-1][1]
    degree_sum =0
    degree_range = max_degree - min_degree
    print(max_degree, min_degree)
    freq_list = [0] * (degree_range)

    for d in degree_list:
        degree = d[1]
        if not degree == 0:
            freq_list[degree-1] = freq_list[degree-1] + 1

    x_list = list(range(1, max_degree+1))

    print(x_list)
    print(freq_list)
    for f in freq_list:
        degree_sum += f
    print('degree sum', degree_sum)
    print(sum(freq_list))

    draw_histo(x_list[0:200], freq_list[0:200], 'Degrees With Weights', 'Frequency', 'Degree Frequency Hist')


def draw_edge_hist(graph):
    print(graph.size(weight='weight'))
    edge_sum = 0
    edge_list = sorted(graph.edges(data=True), key=lambda x: x[2].get('weight'), reverse=True)
    weight_range = edge_list[0][2].get('weight') - 0
    # print(weight_range)
    freq_list = [0] * weight_range

    # print(edge_list)
    for e in edge_list:
        # print(e)
        weight = e[2].get('weight')
        if weight != 0:
            edge_sum += weight
            freq_list[weight - 1] = freq_list[weight - 1] + 1

    x_list = list(range(1, edge_list[0][2].get('weight') + 1))

    print(edge_sum)
    print(freq_list)
    print(x_list)

    draw_histo(x_list, freq_list, 'weights', 'frequency', 'Weight Frequency')


def draw_edge_cut_histo(cuts):
    x_list = range(2, (len(cuts))+2)
    y_list = cuts
    print(x_list)
    print(y_list)

    axes = plt2.gca()
    axes.set_ylim([0, 50000])
    draw_histo(x_list, y_list, 'partition count', 'edge cut', 'Partition count vs Edge cut (total weight = 50000)')


def draw_multi_edge_cut_histo(cuts1, cuts2):
    x_list = range(2, (len(cuts1))+2)
    y_list_1 = cuts1
    y_list_2 = cuts2
    print(x_list)
    print(y_list_1)
    print(y_list_2)

    axes = plt2.gca()
    axes.set_ylim([0, 50000])
    draw_multibar_histo(x_list, y_list_1, y_list_2, 'partition count', 'edge cut', 'Partition count vs Edge cut (total weight = 50000)')

# x_list = [2, 3, 4, 5, 6]
# y_list = [14141, 19612, 21939, 23423, 25406]
# draw_histo(x_list, y_list, 'partition count', 'edge cut', 'Partition count vs Edge cut (total weight = 50000)')

# draw_edge_cut_histo([15188, 20953, 24357, 26458, 27719, 28923, 29357, 30056, 30571, 30991, 31255, 31501, 31744, 31861, 32054, 32160])
# all_50000 = [15155, 21103, 24380, 26459, 27582, 28780, 29489, 29959, 30179, 30881, 30897, 31401]
# st_100000 = [13651, 18375, 22707, 26658, 28310, 28960, 30810, 30266, 32095, 31962, 32874, 32145, 33809, 32282, 32222, 35249]
# lt_40000 = [14084, 19643, 22978, 24879, 25793, 26220, 27174, 27139, 27736, 27662, 28418]
# lt_50000 = [17605.0, 24553.75, 28722.5, 31098.749999999996, 32241.25, 32775.0, 33967.5, 33923.75, 34670.0, 34577.5, 35522.5]
# draw_multi_edge_cut_histo(all_50000, st_100000)


# st5 = [8835, 11045, 13754, 16599, 19614, 20561, 21781, 23477, 23425, 24782, 22795, 25058]
# st5_50000 = [11043.75, 13806.25, 17192.5, 20748.75, 24517.5, 25701.249999999996, 27226.250000000004, 29346.25, 29281.249999999996, 30977.500000000004, 28493.75, 31322.499999999996]
# lt5 = [14537, 20164, 23623, 26226, 27670, 28645, 29556, 30029, 30460, 30820, 31180, 31192]
# lt5_50000 = [17728.048780487803, 24590.243902439022, 28808.53658536585, 31982.926829268294, 33743.902439024394, 34932.92682926829, 36043.90243902439, 36620.73170731707, 37146.34146341463, 37585.365853658535, 38024.39024390244, 38039.0243902439]

# peak_50000 = [14227, 20181, 23966, 26266, 27798, 28710, 29424, 30045, 30450, 30800, 31055, 31429]
# st_6000 = [12973, 17643, 21327, 24012, 26267, 27622, 28456, 29063, 29999, 30390, 30034, 31180]
# lt_36000 = [12569, 17325, 20520, 22364, 23760, 24522, 25240, 25730, 26091, 26453, 26515, 26949]
# lt_mean6_50000 = [17456.944444444445, 24062.5, 28499.999999999996, 31061.111111111113, 33000.0, 34058.333333333336, 35055.555555555555, 35736.11111111111, 36237.5, 36740.27777777778, 36826.38888888889, 37429.1666]


# peak_41000 = [14250, 19922, 23490, 25793, 27419, 28410, 29168, 29676, 30153, 30597, 30654, 31208]
# peak_50000 = [17378.048780487803, 24295.121951219513, 28646.341463414632, 31454.878048780487, 33437.80487804878, 34646.34146341463, 35570.73170731707, 36190.243902439026, 36771.95121951219, 37313.41463414634, 37382.92682926829, 38058.53658536585]
#
#
# rf = []
# for l in peak_41000:
#     a = (l/41000)* 50000
#     rf.append(a)
#
# print(rf)