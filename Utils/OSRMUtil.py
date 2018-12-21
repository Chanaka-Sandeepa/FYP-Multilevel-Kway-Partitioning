import urllib.request
import requests


def getNodeFromCoordinate(coordinates):
    url = 'http://localhost:5000/nearest/v1/driving/'+coordinates
    # print(url)
    # contents = urllib.request.urlopen(url).read()
    # print(contents.json())
    resp = requests.get(url=url)
    # return resp.json().get("waypoints")[0].get("nodes")[0]
    # print(resp.json())
    if resp.json().get("waypoints") is None:
        return 0
    else:
        # print(resp.json())
        return resp.json().get("waypoints")[0].get("nodes")[0]

def getDistanceFromCoordinate(origin, dest):
    if (origin is None) or (dest is None):
        return 0
    else:
        url = 'http://localhost:5000/route/v1/driving/'+origin+';'+dest
        # print(url)
        # contents = urllib.request.urlopen(url).read()
        # print(contents.json())
        resp = requests.get(url=url)
        if resp.json().get('routes') is None:
            return 0
        else:
            # print(resp.json())
            return resp.json().get('routes')[0].get('legs')[0].get('distance')