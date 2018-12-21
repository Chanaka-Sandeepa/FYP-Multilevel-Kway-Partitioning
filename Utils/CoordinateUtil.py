from geopy.distance import distance

distance_throshold = 5

def getStringCoordinateFromList(road_coor_list):
    road_str_coor_list = []
    for coor in road_coor_list:
        cor = (str(coor).replace("[", "").replace("]", "").replace(" ", ""))
        road_str_coor_list.append(cor)
    return road_str_coor_list

def getTupleWithStringCoordinate(coordinate):
    cor_list = coordinate.split(",")
    cor_tuple = (float(cor_list[1]), float(cor_list[0]))
    return cor_tuple

def getTupleListFromCoordinateList(cor_list):
    cor_tuple_list = []
    for c in cor_list:
        cor_list = c.split(",")
        cor_tuple = (float(cor_list[0]), float(cor_list[1]))
        cor_tuple_list.append(cor_tuple)

    # print(cor_tuple_list)
    # print(len(cor_tuple_list))
    return cor_tuple_list

def get_dist_between_locations(orig, dest):
    dist = distance(orig, dest).miles
    return dist

def isShortTrip(orig, dest):
    dist = get_dist_between_locations(orig, dest)
    if dist< distance_throshold:
        return True
    else:
        return False

