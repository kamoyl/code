#!/usr/bin/env python2.7

import sys
import getopt
import logging
import coloredlogs
import os

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored

import config

def usage():
  print(config.cyan + 'Usage:')
  print(__file__ + ' [-o DIRECTORY] -h -v')
  print(config.cyan + 'This script is only template which by default has only few options, and none is mandatory\n')
  print(config.lime + '   -o' + config.blue + '   directory to which will go all LOGs and TMPs')
  print(config.blue + '        default: ' + os.environ['HOME'] + '/var')
  print(config.lime + '   -v' + config.blue + '   verbose')
  print(config.lime + '   -h' + config.blue + '   help')

try:
  opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
except getopt.GetoptError as err:
  # print help information and exit:
  print str(err)  # will print something like "option -a not recognized"
  usage()
  sys.exit(2)
output = None
verbose = False

for o, a in opts:
  if o in ("-v", "--verbose"):
    verbose = True
  elif o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-o", "--output"):
    output = a
  else:
    assert False, "unhandled option"

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG',milliseconds=True)

if output:
  if verbose == True:
    logger.debug("all LOGs and TMPs will go then to: " + config.current_directory + '/' + output)
else:
  if verbose == True:
    logger.warning("-o is empty, so TMP and LOG dir will be default: " + config.user_home_dir + '/var')


exit()
#logger.debug("this is a debugging message")
#logger.info("this is an informational message")
#logger.warning("this is a warning message")
#logger.error("this is an error message")
#logger.critical("this is a critical message")

print(Fore.RED + 'some red text')
print('automatically back to default color again')

print(config.red + 'some red text')
print(config.green + 'some green text')
print(config.blue + 'some blue text')
print(config.yellow + 'some yellow text')
print(config.cyan + 'some cyan text')
print(config.lime + 'some lime text')
print(config.limon + 'some limon text')
print(config.wine + 'some wine text')
#print('\033[30m') # and reset to default color
print ('test')
print(colored('Hello, World!', 'green', 'on_red'))

