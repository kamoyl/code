#!/usr/bin/env python2.7

import sys

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored

import config

print(Fore.RED + 'some red text')
print('automatically back to default color again')

print(config.wine + 'some red text')
#print('\033[30m') # and reset to default color
print(config.lime + 'test')
print ('test')
print(colored('Hello, World!', 'green', 'on_red'))

