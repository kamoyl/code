#!/usr/bin/env python2.7

import sys,getopt

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored

import config

def usage():
  print('help')

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

if output:
  print('-o is ' + output)
else:
  print('-o is empty')
  exit()

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

