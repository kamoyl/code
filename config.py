#!/usr/bin/env python2.7

import os
import datetime
import socket

wine = '\x1b[38;2;191;000;000m'
limon = '\x1b[38;2;191;255;000m'
lime = '\x1b[38;2;000;255;000m'
red = '\x1b[38;2;255;000;000m'
blue = '\x1b[38;2;000;128;255m'
cyan = '\x1b[38;2;000;255;255m'
green = '\x1b[38;2;000;128;000m'
yellow = '\x1b[38;2;255;255;000m'

current_directory = os.getcwd()
user_home_dir = os.environ['HOME']

current_timestamp = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
koen_network = '172.16.0.0/12'
vpn_network = '10.65.64.0/18 129.189.0.0/16'

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
