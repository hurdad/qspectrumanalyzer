#!/usr/bin/python

## Copyright [2018] <Alexander Hurd>"

from __future__ import print_function

import argparse
import zmq


def read_data(args):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(args.server)
    socket.setsockopt_string(zmq.SUBSCRIBE, unicode(args.filter))

    while True:
        result = socket.recv_string()
        print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="python radio_server data-client")
    parser.add_argument('-s', '--server', default='tcp://localhost:5557', help='Radio Server ZMQ Pub Address')
    parser.add_argument('-f', '--filter', default='', help='ZMQ Subcribe Topic Filter')

    args = parser.parse_args()

    read_data(args)
