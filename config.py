#!/usr/bin/env python2.7

import os
import datetime
import logging
import coloredlogs
import socket
from multiprocessing import cpu_count
from netaddr import IPNetwork, IPAddress
import getopt
import gzip
import shutil

#definition of used colours
wine = '\x1b[38;2;191;000;000m'
limon = '\x1b[38;2;191;255;000m'
lime = '\x1b[38;2;000;255;000m'
red = '\x1b[38;2;255;000;000m'
blue = '\x1b[38;2;000;128;255m'
cyan = '\x1b[38;2;000;255;255m'
green = '\x1b[38;2;000;128;000m'
yellow = '\x1b[38;2;255;255;000m'

#few important static variables commonly used
current_directory = os.getcwd()
current_timestamp = datetime.datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
yesterday_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
yesterday_date_long = datetime.datetime.now() - datetime.timedelta(days=1)
today_date = datetime.datetime.now().strftime("%Y-%m-%d")
today_date_long = datetime.datetime.now()
dbalog = "MONITORING"
dbalogv = "MONITORINGV"
#networks
office_network = "172.16.0.0/12"
vpn1_network = "10.65.64.0/18"
vpn2_network = "129.189.0.0/16"
vpn=0
office=0
#amount of cores (for parallel processing)
cpu_cores = cpu_count()

#export colours to BASH, for bteq to use
os.environ["WINE"] = wine
os.environ["LIMON"] = limon
os.environ["LIME"] = lime
os.environ["RED"] = red
os.environ["BLUE"] = blue
os.environ["CYAN"] = cyan
os.environ["GREEN"] = green
os.environ["YELLOW"] = yellow
#some of important variables for being recognized in BASH subprocesses
user_home_dir = os.environ['HOME']
os.environ["CURRENT_TIMESTAMP"] = current_timestamp
os.environ["DBALOG"] = dbalog
os.environ["DBALOGV"] = dbalogv
os.environ["TODAY"] = today_date
os.environ["YESTERDAY"] = yesterday_date
os.environ["VPN1_NETWORK"] = vpn1_network
os.environ["VPN2_NETWORK"] = vpn2_network
os.environ["OFFICE_NETWORK"] = office_network

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG',milliseconds=True)

#funtions used accros all scripts
#general usage definition - accros all scripts, more specific one will have this one as a part
def usage():
  print(lime + '   -o, --output=' + blue + '   directory to which will go all LOGs and TMPs')
  print(blue + '                   default: ' + cyan + os.environ['HOME'] + '/var')
  print(lime + '   -v, --verbose' + blue + '   verbose')
  print(lime + '   -h, --help' + blue + '      help')

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

default_local_ip = get_ip()

def isOFFICEnetwork(local_ip):
  if IPAddress(local_ip) in IPNetwork(office_network):
    office=1
  elif IPAddress(local_ip) in IPNetwork(vpn1_network):
    vpn=1
  elif IPAddress(local_ip) in IPNetwork(vpn2_network):
    vpn=1

def outArchive(title, filename, srcenv, temporary_dir, *verbosity):
  #if verbose == True:
  logger.debug(wine + '    start: ' + yellow + title)
  archive_file_extension = ("_" + srcenv + "_" + current_timestamp + ".outdone")
  new_name = str(filename)[:-4] + archive_file_extension
  os.rename(temporary_dir + '/' + filename, temporary_dir + '/' + new_name)
  with open(temporary_dir + '/' + new_name, 'rb') as new_name_in:
      with gzip.open(temporary_dir + '/' + new_name + '.gz', 'wb') as new_name_out:
        shutil.copyfileobj(new_name_in, new_name_out)
        os.remove(temporary_dir + '/' + new_name)
  #if verbose == True:
  logger.debug(wine + '      end: ' + yellow + title)

def logArchive(title, filename, logs_dir):
  #if verbose == True:
  logger.debug(wine + '    start: ' + yellow + title)
  with open(logs_dir + '/' + filename, 'rb') as new_name_in:
    with gzip.open(logs_dir + '/' + filename + '.gz', 'wb') as new_name_out:
      shutil.copyfileobj(new_name_in, new_name_out)
      os.remove(logs_dir + '/' + filename)
  #if verbose == True:
  logger.debug(wine + '      end: ' + yellow + title)
