import os
import sys

durtime = 10
log_dir = sys.argv[1]
log_files = os.listdir(log_dir)
rlist = list()
wlist = list()

class stats(object):
    def __init__(self, request_type=None, throughput=None, avg=None, ld={}):
        self.request_type = request_type
        self.throughput = throughput
        self.avg = avg
        self.lat_distribution = ld

    def pretty_print(self):
        print "request type: {}".format(self.request_type)
        print "throughput: {} requests per second".format(self.throughput)
        print "average: {} us".format(self.avg)
        # print "latency distribution: {}".format(self.lat_distribution)


def parse_stats(fn):
    read_stats = None
    write_stats = None
    curr_stats = None
    with open(fn, "r") as f:

        for line in f:
            if line.startswith("Request type"):
                request_type = line.split(None)[-1].strip()
                if request_type == "get":
                    curr_stats = read_stats = stats(request_type)
                else:
                    curr_stats = write_stats = stats(request_type)
            elif line.startswith("Measured RTTs"):
                curr_stats.throughput = int(line.split(None)[-1].strip())
            elif line.startswith("RTT min"):
                curr_stats.avg = int(line.split('/')[3].strip())
                
            elif line.startswith("RTT distribution for 'get'"):
                curr_stats = read_stats
            elif line.startswith("RTT distribution for 'set'"):
                curr_stats = write_stats
                
            elif line.startswith("["):
                interval_start = int(line.split("-", 1)[0].strip()[1:])
                height = int(line.split(None)[-1].strip())
                curr_stats.lat_distribution[interval_start] = height
            
            elif line.startswith("Over 10000"):
                curr_stats[10000] = line.split(None)[-1].strip()
    return (read_stats, write_stats)


def aggreate(sl, rtype):
    sllen = len(sl)
    print sllen
    total_stats = stats(rtype, throughput=0, avg=0)

    for sat in sl:
        total_stats.throughput += sat.throughput
        total_stats.avg += sat.avg

    total_stats.throughput /= durtime
    total_stats.avg /= sllen
    total_stats.pretty_print()

    
for f in log_files:
    fn = log_dir + f;
    rs, ws = parse_stats(fn)
    # rs.pretty_print()
    rlist.append(rs)
    wlist.append(ws)
aggreate(rlist, "get")
