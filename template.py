#!/usr/bin/env python2.7

import sys
import getopt
import logging
import coloredlogs
import os
import datetime
import subprocess
import time
import pandas
import re
import gzip
import shutil

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored

import config

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG',milliseconds=True)

start_time_template = str(datetime.datetime.now())
start_time_template_seconds = time.time()

def usage():
  print(config.cyan + 'Usage:')
  print(__file__ + ' [-s, --source_env=<PROD|PROD10|PROD11|DTA|host>] [-o, --output=DIRECTORY] [-d, --date=<DATE(YYYY-MM-DD)/WEEK_NR(XX)>] [-u, --user=TECH_USER] [-n, --report_number=REPORT_NUMBER] -v, --verbose -h, --help')
  print(config.cyan + 'This script is only template which by default has only few options, and none is mandatory\n')
  config.usage()
  print(config.lime + '   -h, --help' + config.blue + '      help')

try:
  opts, args = getopt.getopt(sys.argv[1:], "hs:o:d:u:n:v", ["help", "source_env=", "output=", "date=", "user=", "report_number=", "verbose"])
except getopt.GetoptError as err:
  print str(err)  # will print something like "option -a not recognized"
  usage()
  sys.exit(2)
output = None
verbose = False
user = None
report_number = None
report_date = None
source_env = None
env = None
script_path = os.path.realpath(__file__)
scripts_home = os.path.dirname(script_path)

for o, a in opts:
  if o in ("-v", "--verbose"):
    verbose = True
  elif o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-s", "--source_env"):
    source_env = a
    env = source_env
    os.environ["ENV"] = env
  elif o in ("-o", "--output"):
    output = a
  elif o in ("-d", "--date"):
    report_date = a
    os.environ["REPORT_DATE"] = report_date
  elif o in ("-u", "--user"):
    user = a
  elif o in ("-n", "--report_number"):
    report_number = a
    os.environ["REPORT_NUMBER"] = report_number
  else:
    assert False, "unhandled option"

if not env:
  logger.error('Source environment MUST be set with: ' + config.cyan + '-s, --source_env=<PROD|PROD10|PROD11|DTA|host>')
  exit()

if env == 'PROD':
  print('environment is: ' + env)

if not report_number:
  logger.error('Report number MUST be set with: ' + config.cyan + '-n, --report_number=')
  exit()

if not report_date:
  report_date = datetime.datetime.now().strftime("%Y-%m-%d")
  os.environ["REPORT_DATE"] = report_date

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
os.environ["SCRIPTS_HOME"] = scripts_home
report_file1 = "7_Ampconfig.out" 
report_file2 = "1_Diskspace.out"
report_file3 = "2_Diskspace_trend.out"
report_file4 = "8_cpu_Hourly_Details.out"
report_file5 = "3_cpu_COD_busy_monthly.out"
report_file6 = "9_cpu_Weekday_Details.out"
report_file7 = "4_cpu_ImpactCPU_monthly.out"
report_file8 = "6_AWT_grid_graph.out"
report_file9 = "5_flow_control_heat_map.out"
report_file10 = "6_AWT_grid_graph_weekly.out"
confluence_pageid = "62013301"
confluence_history_pageid = "62013304"
report_title = (report_number + " - capacity weekly report on: " + env)
export_file_extension = (env + "_" + report_date + ".xlsx")
log_file_extension = (config.current_timestamp + ".log")
export_file = (report_number + "_Capacity_weekly_" + export_file_extension)
log_file = (report_title + "_" + log_file_extension)

if verbose == True:
  logger.debug('current timestamp is: ' + config.blue + config.current_timestamp)
  logger.debug('my default ip is: ' + config.blue + config.get_ip())
  if config.office == 1:
    logger.debug(config.blue + 'office_network is present')
    office_ip = config.default_local_ip
    os.environ["OFFICE_IP"] = office_ip
  elif config.vpn == 1:
    logger.debug(config.blue + 'vpn is present')
    vpn_ip = config.default_local_ip
    os.environ["VPN_IP"] = vpn_ip
  else:
    logger.debug(config.blue + 'not connected to the office')

os.environ["REPORT_FILE1"] = report_file1
os.environ["REPORT_FILE2"] = report_file2
os.environ["REPORT_FILE3"] = report_file3
os.environ["REPORT_FILE4"] = report_file4
os.environ["REPORT_FILE5"] = report_file5
os.environ["REPORT_FILE6"] = report_file6
os.environ["REPORT_FILE7"] = report_file7
os.environ["REPORT_FILE8"] = report_file8
os.environ["REPORT_FILE9"] = report_file9
os.environ["EXPORT_FILE"] = export_file
os.environ["CONFLUENCE_PAGEID"] = confluence_pageid
os.environ["CONFLUENCE_HISTORY_PAGEID"] = confluence_history_pageid
os.environ["REPORT_TITLE"] = report_title
os.environ["EXPORT_FILE_EXTENSION"] = export_file_extension
os.environ["LOG_FILE_EXTENSION"] = log_file_extension
os.environ["LOG_FILE"] = log_file

start_time_bash_seconds = time.time()
#os.system(scripts_home + '/template.bash')
#subprocess.call(scripts_home + '/report.bteq', shell=True, stdout=subprocess.PIPE)
try:
#  subprocess.check_call(scripts_home + '/report.bteq', shell=False, stdout = subprocess.PIPE)
  logger.debug('LOG file of running BTEQ: ' + new_log + log_file)
except:
  logger.error("bteq script failed")
  sys.exit(1)
end_time_bash_seconds = time.time()
bash_seconds = [end_time_bash_seconds, -start_time_bash_seconds]

with open(new_tmp + '/' + report_file3, "a+b") as report_file3_open:
  row_list = report_file3_open.readlines()[1:2]
  max_perm = float(row_list[0].split('~')[4])
  avg_perm = float(row_list[0].split('~')[3])
  skew_factor = (100*(max_perm - avg_perm)/max_perm)
  report_file3_open.write('~~~~~System skew factor\n')
  report_file3_open.write('~~~~~' + str(skew_factor) + ' %\n')

with open(new_tmp + '/' + report_file2, "a+b") as report_file2_open:
  with open(new_tmp + '/' + report_file3, "r") as report_file3_open:
    report_file3_read = report_file3_open.read()
    report_file2_open.write('\n')
    report_file2_open.write('\n')
    report_file2_open.write('\n')
    report_file2_open.write('\n')
    report_file2_open.write(report_file3_read)

logger.debug("Few manipulations for AWT extract data")

report_file8_open = open(new_tmp + '/' + report_file8, "r")
report_file10_open = open(new_tmp + '/' + report_file10, "a+b")

for day_week_range in range(1,8):
  date_week = str(datetime.datetime.now() - datetime.timedelta(days=day_week_range))[:10]
  report_file8_open.seek(0,0)
  for week_line in report_file8_open:
    if date_week in week_line:
      report_file10_open.write(week_line)

end_time_template_seconds = time.time()
template_seconds = [end_time_template_seconds, -start_time_template_seconds]

time_template_seconds = sum(template_seconds)
time_bash_seconds = sum(bash_seconds)

python_seconds = [time_template_seconds, -time_bash_seconds]
time_python_seconds = sum(python_seconds)

#to delete
logger.debug(config.limon + "Run time: " + config.wine + "%.4f" % time_template_seconds + config.limon +  " seconds")
logger.debug(config.limon + "BASH script run for: " + config.wine + "%.4f" % time_bash_seconds + config.limon +  " seconds")
logger.debug(config.limon + "Python script run for: " + config.wine + "%.4f" % time_python_seconds + config.limon + " seconds")
exit()
#to delete



logger.debug("Archiving all output files")
report_output_list = [report_file1, report_file2, report_file3, report_file4, report_file5, report_file6, report_file7, report_file8, report_file9, report_file10]
report_output_list_len = len(report_output_list)
for report_file in range(0, report_output_list_len):
  archive_file_extension = ("_" + env + "_" + config.current_timestamp + ".outdone")
  new_name = str(report_output_list[report_file])[:-4] + archive_file_extension
  os.rename(new_tmp + '/' + report_output_list[report_file], new_tmp + '/' + new_name)
  with open(new_tmp + '/' + new_name, 'rb') as new_name_in:
    with gzip.open(new_tmp + '/' + new_name + '.gz', 'wb') as new_name_out:
      shutil.copyfileobj(new_name_in, new_name_out)
      os.remove(new_tmp + '/' + new_name)

with open(new_log + '/' + log_file, 'rb') as new_name_in:
  with gzip.open(new_log + '/' + log_file + '.gz', 'wb') as new_name_out:
    shutil.copyfileobj(new_name_in, new_name_out)
    os.remove(new_log + '/' + log_file)
  
logger.debug(config.limon + "Run time: " + config.wine + "%.4f" % time_template_seconds + config.limon +  " seconds")
logger.debug(config.limon + "BASH script run for: " + config.wine + "%.4f" % time_bash_seconds + config.limon +  " seconds")
logger.debug(config.limon + "Python script run for: " + config.wine + "%.4f" % time_python_seconds + config.limon + " seconds")
