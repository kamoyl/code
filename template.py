#!/usr/bin/python

import sys

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored

wine = print('\x1b[38;2;191;000;000m')
lime = print('\x1b[38;2;191;255;000m')

print(Fore.RED + 'some red text')
print('automatically back to default color again')

print('\033[31m' + 'some red text')
print('\033[30m') # and reset to default color
print('\x1b[38;2;191;255;000m' + 'test')

print(colored('Hello, World!', 'green', 'on_red'))

