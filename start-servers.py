import subprocess
import argparse

nservers = 0
cur_port = 0
ncores = 0
cur_core = 0

class memcached(object):
    """
    Stores memcached process state.

    Exposes a UDP and/or TCP port with the given port number(s).
    """

    def __init__(self, tcp_port, udp_port, nb_threads, core, debug):
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.nb_threads = nb_threads
        self.debug = debug

        self.args = ["taskset"]
        self.args.extend(["-c", str(core)])
        self.args.extend(["memcached"])
        if debug:
            self.args.append("-vv")
        if tcp_port > 0:
            self.args.extend(["-p", str(tcp_port)])
        self.args.extend([ "-U", str(udp_port), "-t", str(nb_threads)])
        # print self.args
        self.p = subprocess.Popen(self.args)

    def stop(self):
        self.p.terminate()


def increment_udp_port(port):
    global cur_port
    p = port + cur_port
    cur_port = (cur_port +1) % nservers
    return p


def increment_core_num(core):
    global cur_core
    p = core + cur_core
    cur_core = (cur_core +1) % ncores
    return p


def start_servers(tcp_port, udp_port, nb_threads, nb_servers, debug):
    mc_list = []

    for _ in range(nb_servers):
        up = increment_udp_port(udp_port)
        nc = increment_core_num(0)
        mc_list.append(memcached(tcp_port, up, nb_threads, nc, debug))
        if tcp_port > 0:
            tcp_port += 1
    return mc_list


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="tcp port number", type=int)
    parser.add_argument("-u", help="udp port number", type=int)
    parser.add_argument("-t", help="Number of threads per server", type=int)
    parser.add_argument("--nb_servers", help="number of instances to create", type=int)
    parser.add_argument("--nb_core", help="number of cores", type=int)
    parser.add_argument("--debug", help="Enable debugging", action="store_true")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    tcp_port = args.p
    udp_port = args.u if args.u else 12345
    nb_threads = args.t if args.t else 4
    nb_servers = args.nb_servers if args.nb_servers else 1
    debug = args.debug
    nservers = nb_servers
    ncores = args.nb_core if args.nb_servers else 1

    mc_list = start_servers(tcp_port, udp_port, nb_threads, nb_servers, debug)
    while True:
        quit = raw_input("quit? y/n")
        if "y" in quit:
            break

    for mc in mc_list:
        mc.stop()
