#!/usr/bin/env python2.7

import sys
import getopt
import logging
import coloredlogs
import os
import tempfile
import teradata
import datetime
#import time

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored

import config

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG',milliseconds=True)

start_time_template = str(datetime.datetime.now())
start_time_template_seconds = float(start_time_template[-9:])
start_time_template_minutes = int(start_time_template[-12:-10])

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
script_path = os.path.realpath(__file__)
scripts_home = os.path.dirname(script_path)

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
  new_var = output
  new_tmp = new_var + '/' + 'tmp'
  new_log = new_var + '/' + 'log'
  if not os.path.exists(new_var):
    try:
      os.mkdir(new_var)
      os.mkdir(new_tmp)
      os.mkdir(new_log)
      if verbose == True:
        logger.debug("Successfully created the directory: " + config.blue + new_var)
        logger.debug("all LOGs and TMPs will go then to: "+ config.blue + output)
    except OSError as err:
      logger.error("Creating directory failed - possibly permission denied")
      exit(2)
  else:
    if verbose == True:
      logger.debug("Directory for tmp and logs exists: " + config.blue + new_var)
else:
  new_var = config.user_home_dir + '/var'
  new_tmp = new_var + '/' + 'tmp'
  new_log = new_var + '/' + 'log'
  if not os.path.exists(new_var):
    try:
      os.mkdir(new_var)
      os.mkdir(new_tmp)
      os.mkdir(new_log)
      if verbose == True:
        logger.debug("Successfully created the directory: " + config.blue + new_var)
        logger.debug("all LOGs and TMPs will go then to: " + config.blue + new_var)
    except OSError as err:
      logger.error("Creating directory failed - possibly permission denied")
      exit(2)
  else:
    if verbose == True:
      logger.debug("Directory for tmp and logs exists: " + config.blue + new_var)

os.environ["TMP"] = new_tmp
os.environ["VAR"] = new_var
os.environ["LOG"] = new_log
os.environ["SCRIPTS_HPOME"] = scripts_home

start_time_bash = str(datetime.datetime.now())
start_time_bash_seconds = float(start_time_bash[-9:])
start_time_bash_minutes = int(start_time_bash[-12:-10])
bash_seconds = [start_time_bash_seconds, -start_time_bash_seconds]
bash_minutes = [start_time_bash_minutes, -start_time_bash_minutes]
os.system(scripts_home + '/template.bash')
end_time_bash = str(datetime.datetime.now())
end_time_bash_seconds = float(end_time_bash[-9:])
end_time_bash_minutes = int(end_time_bash[-12:-10])
bash_seconds = [end_time_bash_seconds, -start_time_bash_seconds]
bash_minutes = [end_time_bash_minutes, -start_time_bash_minutes]
#xlsx_file_path = os.getenv('XLSX_FILE_PATH')

if verbose == True:
  logger.debug('current timestamp is: ' + config.blue + config.current_timestamp)
  logger.debug('my default ip is: ' + config.blue + config.get_ip())

end_time_template = str(datetime.datetime.now())
end_time_template_seconds = float(end_time_template[-9:])
end_time_template_minutes = int(end_time_template[-12:-10])
template_seconds = [end_time_template_seconds, -start_time_template_seconds]
template_minutes = [end_time_template_minutes, -start_time_template_minutes]

time_template_seconds = sum(template_seconds)
time_template_minutes = sum(template_minutes)
time_bash_seconds = sum(bash_seconds)
time_bash_minutes = sum(bash_minutes)

python_minutes = [time_template_minutes, -time_bash_minutes]
python_seconds = [time_template_seconds, -time_bash_seconds]
time_python_minutes = sum(python_minutes)
time_python_seconds = sum(python_seconds)

logger.debug("Run time: " + str(time_template_minutes) + " minutes, and: " + "%.4f" % time_template_seconds + " seconds")
logger.debug("BASH script run for: " + str(time_bash_minutes) + " minutes, and: " + "%.4f" % time_bash_seconds + " seconds")
logger.debug("Python script run for: " + str(time_python_minutes) + " minutes, and: " + "%.4f" % time_python_seconds + " seconds")


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

