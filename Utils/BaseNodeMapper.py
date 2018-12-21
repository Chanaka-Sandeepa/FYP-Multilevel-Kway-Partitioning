from Utils import CoordinateUtil

distanceThreshold = 0.0025


def isInt(var):
    try:
        var = int(var)
    except ValueError:
        return False
    return True


def get_Mapped_BaseNode(colombo_basenodes, coordinate_tuple, tree, colombo_corlist):
    cor_entry = tree.query(coordinate_tuple)
    cor_index = cor_entry[1]
    print(cor_entry, colombo_basenodes[cor_index])

    if not isInt(cor_index):
        cor_index = cor_index[0]

    if cor_entry[0] < distanceThreshold:
        nearestNode = colombo_basenodes[cor_index]
        nearestCoordinate = None
        nearestCoordinate = colombo_corlist[cor_index]
        print({"nodeId": nearestNode, "coordinate": nearestCoordinate})
        return {"nodeId": nearestNode, "coordinate": nearestCoordinate}
    else:
        print("none entry", colombo_basenodes[cor_index])
        return None


