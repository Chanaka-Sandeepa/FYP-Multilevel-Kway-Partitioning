import simplejson

def write_partitions(partitions):
    f = open('output.txt', 'w')
    simplejson.dump(partitions, f)
    f.close()
