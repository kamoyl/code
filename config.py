#!/usr/bin/env python2.7

import os
import sys
import datetime
import logging
import coloredlogs
import socket
from netaddr import IPNetwork, IPAddress
import getopt

wine = '\x1b[38;2;191;000;000m'
limon = '\x1b[38;2;191;255;000m'
lime = '\x1b[38;2;000;255;000m'
red = '\x1b[38;2;255;000;000m'
blue = '\x1b[38;2;000;128;255m'
cyan = '\x1b[38;2;000;255;255m'
green = '\x1b[38;2;000;128;000m'
yellow = '\x1b[38;2;255;255;000m'

os.environ["WINE"] = wine
os.environ["LIMON"] = limon
os.environ["LIME"] = lime
os.environ["RED"] = red
os.environ["BLUE"] = blue
os.environ["CYAN"] = cyan
os.environ["GREEN"] = green
os.environ["YELLOW"] = yellow

current_directory = os.getcwd()
user_home_dir = os.environ['HOME']

office_network = "172.16.0.0/12"
vpn1_network = "10.65.64.0/18"
vpn2_network = "129.189.0.0/16"

current_timestamp = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
os.environ["CURRENT_TIMESTAMP"] = current_timestamp
office_network = '172.16.0.0/12'
vpn_network = '10.65.64.0/18 129.189.0.0/16'
dbalog = "MONITORING"
dbalogv = "MONITORINGV"
os.environ["DBALOG"] = dbalog
os.environ["DBALOGV"] = dbalogv

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG',milliseconds=True)

def usage():
  print(lime + '   -o, --output=' + blue + '   directory to which will go all LOGs and TMPs')
  print(blue + '                   default: ' + cyan + os.environ['HOME'] + '/var')
  print(lime + '   -v, --verbose' + blue + '   verbose')

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

vpn=0
office=0
default_local_ip = get_ip()
if IPAddress(default_local_ip) in IPNetwork(office_network):
  office=1
elif IPAddress(default_local_ip) in IPNetwork(vpn1_network):
  vpn=1
elif IPAddress(default_local_ip) in IPNetwork(vpn2_network):
  vpn=1
