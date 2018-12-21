import pandas as pd
import json
from Utils import CoordinateUtil
from Utils import OSRMUtil

mean_dist = 6000


def readRoadData(filePath):
    print("Reading road json files...")
    count = 0
    with open(filePath) as data_file:
        data = json.load(data_file)
    # pprint(data)
    features = data["features"]
    roads = []
    for f in features:
        if('geometry' in f) and (f["geometry"]["type"] != 'Point'):
            # print(f["geometry"]["coordinates"])
            road_cor_list = CoordinateUtil.getStringCoordinateFromList(f["geometry"]["coordinates"])
            roads.append(road_cor_list)
        # print(roads)
        # if(count >50):
        #     break
        count += 1

    print(roads)
    return roads

def readTripData(filePath):
    # trip_columns = ['trips.pickuplatitide', 'trips.pickuplongitude', 'trips.droplatitude', 'trips.droplongitude']
    print('Reading trip data ...')
    trip_data = pd.read_csv(filePath)
    trip_data = trip_data.dropna(how='any')
    pickups = trip_data['trips.pickuplongitude'].map(str)+ ',' +trip_data['trips.pickuplatitide'].map(str)
    dropoffs = trip_data['trips.droplongitude'].map(str)+ ','+trip_data['trips.droplatitude'].map(str)
    # trips = trip_data[trip_columns]
    trips = pd.DataFrame(
        {'pickup': pickups,
         'dropoff': dropoffs
         })
    # print(trips['pickup'] ,trips['dropoff'])
    return trips

def readManhattenTripData(filePath):
    # trip_columns = ['trips.pickuplatitide', 'trips.pickuplongitude', 'trips.droplatitude', 'trips.droplongitude']
    print('Reading trip data ...')
    trip_data = pd.read_csv(filePath)
    trip_data = trip_data[:50000]
    # print(trip_data.columns)
    trip_data = trip_data.dropna(how='any')
    pickups = trip_data['pickup_long'].map(str)+ ',' +trip_data['dropoff_lat'].map(str)
    dropoffs = trip_data['dropoff_long'].map(str)+ ','+trip_data['dropoff_lat'].map(str)
    # trips = trip_data[trip_columns]
    trips = pd.DataFrame(
        {'pickup': pickups,
         'dropoff': dropoffs
         })
    # print(trips['pickup'] ,trips['dropoff'])
    print(trips.head())
    return trips

def readNYCTripData(filePath):
    # trip_columns = ['trips.pickuplatitide', 'trips.pickuplongitude', 'trips.droplatitude', 'trips.droplongitude']
    print('Reading trip data ...')
    trip_data = pd.read_csv(filePath)
    trip_data = trip_data.dropna(how='any')
    pickups = trip_data['pickup_longitude'].map(str)+ ',' +trip_data['pickup_latitude'].map(str)
    dropoffs = trip_data['dropoff_longitude'].map(str)+ ','+trip_data['dropoff_latitude'].map(str)
    # trips = trip_data[trip_columns]
    trips = pd.DataFrame(
        {'pickup': pickups,
         'dropoff': dropoffs
         })
    # print(trips['pickup'] ,trips['dropoff'])
    return trips


def readBaseNodes(file_path):
    print('Reading Collombo Nodes ...')
    base_node_data = pd.read_csv(file_path, header=None)
    base_node_data = base_node_data.dropna(how='any')

    nodes = base_node_data[0]
    coordinates = base_node_data[1].map(str) + ',' + base_node_data[2].map(str)
    # print(nodes)
    # print(coordinates)
    return nodes, coordinates

def isShortTrip(pickup, drop):
    distance = OSRMUtil.getDistanceFromCoordinate(pickup,  drop)
    if distance < mean_dist:
        return True
    return False


def readTripsForClassify(filePath):
    print('Reading trip data...')
    trip_data = pd.read_csv(filePath)
    distances = []
    short_trips = []
    long_trips = []

    trip_data = trip_data.dropna(how='any')
    pickups = trip_data['trips.pickuplongitude'].map(str)+ ',' +trip_data['trips.pickuplatitide'].map(str)
    dropoffs = trip_data['trips.droplongitude'].map(str)+ ','+trip_data['trips.droplatitude'].map(str)
    # trips = trip_data[trip_columns]
    trips = pd.DataFrame(
        {'pickup': pickups,
         'dropoff': dropoffs
         })

    c = 0
    for index, row in trips.iterrows():
        print(row)
        if isShortTrip(row['pickup'], row['dropoff']):
            short_trips.append({'pickup':row['pickup'], 'dropoff':row['dropoff']})
        else:
            long_trips.append({'pickup':row['pickup'], 'dropoff':row['dropoff']})
        # distances.append(distance)
        if c > 75000:
            break
        c += 1
        # if len(short_trips)> 50000:
        #     break
        print(c)
    # draw_distance_hist(distances)

    # mean_distance = sum(distances)/len(distances)
    # print('Mean Distance :', mean_distance)
    # write_csv(short_trips, 'short_trips.csv')
    # write_csv(long_trips, 'long_trips')
    # print(trips['pickup'] ,trips['dropoff'])
    return short_trips, long_trips


def isPeakTrip(dateTime):
    print(dateTime)
    time = dateTime.split(' ')[1]
    trip_hour = int(time.split(':')[0])
    print(trip_hour)
    if((trip_hour > 6 and trip_hour < 10) or (trip_hour > 16 and trip_hour < 21)):
        return True
    return False


def time_trip_classifier(filePath):
    print('Reading trip data...')
    trip_data = pd.read_csv(filePath)
    peak_trips = []
    offpeak_trips = []

    trip_data = trip_data.dropna(how='any')
    pickups = trip_data['trips.pickuplongitude'].map(str) + ',' + trip_data['trips.pickuplatitide'].map(str)
    dropoffs = trip_data['trips.droplongitude'].map(str) + ',' + trip_data['trips.droplatitude'].map(str)
    times = trip_data['trips.actualpickuptime'].map(str)
    # trips = trip_data[trip_columns]
    trips = pd.DataFrame(
        {'pickup': pickups,
         'dropoff': dropoffs,
         'pickup_time' : times
         })

    c = 0
    for index, row in trips.iterrows():
        print(row)
        if isPeakTrip(row['pickup_time']):
            peak_trips.append({'pickup': row['pickup'], 'dropoff': row['dropoff']})
        else:
            offpeak_trips.append({'pickup': row['pickup'], 'dropoff': row['dropoff']})
        # distances.append(distance)
        # if c > 200000:
        #     break
        c += 1
        if len(offpeak_trips) > 75000:
            break
        print(c)

    print(len(offpeak_trips), len(peak_trips))
    return peak_trips, offpeak_trips




def read_test_trips(filePath):
    # trip_columns = ['trips.pickuplatitide', 'trips.pickuplongitude', 'trips.droplatitude', 'trips.droplongitude']
    print('Reading trip data ...')
    trip_data = pd.read_csv(filePath)
    trip_data = trip_data[75001:]
    trip_data = trip_data.dropna(how='any')
    pickups = trip_data['trips.pickuplongitude'].map(str)+ ',' +trip_data['trips.pickuplatitide'].map(str)
    dropoffs = trip_data['trips.droplongitude'].map(str)+ ','+trip_data['trips.droplatitude'].map(str)
    pickupdates = trip_data['trips.pickupdate'].map(str)
    # trips = trip_data[trip_columns]
    trips = pd.DataFrame(
        {'pickup': pickups,
         'dropoff': dropoffs,
         'pickupdate': pickupdates
         })
    # print(trips['pickup'] ,trips['dropoff'])
    return trips


