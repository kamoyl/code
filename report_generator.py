#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import getopt
import logging
import coloredlogs
import os
import datetime
import subprocess
import time
#import pandas
#import re
#import gzip
#import shutil
#import multiprocessing as mp
#import threading
#import numpy
#import csv
#import glob
from joblib import Parallel, delayed
#from xlsxwriter import Workbook
#from xlsxwriter.utility import xl_rowcol_to_cell

try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored
reload(sys)
sys.setdefaultencoding('utf8')

import config

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG',milliseconds=True)

start_time_template_seconds = time.time()

def usage():
  print(config.cyan + 'Usage:\n\n')
  print(config.cyan + 'This script manages all Teradata reports, creates excel sheets, manage confluence and Jira\n\n')
  print(__file__ + '\n' + '                [-s, --source_env=' + config.green + '<PROD|PROD10|PROD11|DTA|host>' + config.cyan + ']\n' 
                        '                [-d, --date=' + config.green + '<DATE(YYYY-MM-DD)/WEEK_NR(XX)>' + config.cyan + ']\n' + 
                        '                [-u, --user=' + config.green + 'TECH_USER' + config.cyan + ']\n' +  
                        '                [-n, --report_number=' + config.green + 'REPORT_NUMBER' + config.cyan + ']\n\n' +  
                        '                [-o, --output=' + config.green + 'DIRECTORY' + config.cyan + ']\n' +
                        '                [-v, --verbose\n' +  
                        '                [-h, --help\n')
  config.usage()

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
    os.environ["VERBOSE"] = "yes"
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
    report_date_long = a + ' 10:00:00.999999'
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

if env != 'PROD':
  logger.error('Source env MUST be PROD now')
  exit(1)
else:
  print('environment is: ' + env)

if not report_date:
  report_date = config.yesterday_date
  report_date_long = config.yesterday_date_long
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
        logger.debug("all LOGs will go to: " + config.blue + new_log + config.lime + " and TMPs will go then to: " + config.blue + new_tmp)
    except OSError as err:
      logger.error("Creating directory failed - possibly permission denied")
      exit(2)
  else:
    if verbose == True:
      logger.debug("Directory for tmp and logs exists: " + config.blue + new_var)
      logger.debug("all LOGs will go to: " + config.blue + new_log + config.lime + " and TMPs will go then to: " + config.blue + new_tmp)
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
        logger.debug("all LOGs will go to: " + config.blue + new_log + config.lime + " and TMPs will go then to: " + config.blue + new_tmp)
    except OSError as err:
      logger.error("Creating directory failed - possibly permission denied")
      exit(2)
  else:
    if verbose == True:
      logger.debug("Directory for tmp and logs exists: " + config.blue + new_var)
      logger.debug("all LOGs will go to: " + config.blue + new_log + config.lime + " and TMPs will go then to: " + config.blue + new_tmp)

os.environ["TMP"] = new_tmp
os.environ["VAR"] = new_var
os.environ["LOG"] = new_log
os.environ["SCRIPTS_HOME"] = scripts_home

report_number_list=[302]
report_number_list_len = len(report_number_list)

if not report_number:
  logger.error('Report number MUST be set with: ' + config.cyan + '-n, --report_number=')
  exit(1)
elif report_number == "302":
  logger.info('Preparing report ' + config.cyan + report_number + config.white + ' files for ' + config.cyan + report_date)
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
  report_file11 = "6_AWT_grid_graph_monthly.out"
  report_file12 = "6_AWT_grid_graph_daily.out"
  os.environ["REPORT_FILE1"] = report_file1
  os.environ["REPORT_FILE2"] = report_file2
  os.environ["REPORT_FILE3"] = report_file3
  os.environ["REPORT_FILE4"] = report_file4
  os.environ["REPORT_FILE5"] = report_file5
  os.environ["REPORT_FILE6"] = report_file6
  os.environ["REPORT_FILE7"] = report_file7
  os.environ["REPORT_FILE8"] = report_file8
  os.environ["REPORT_FILE9"] = report_file9
  report_output_list = [report_file1, report_file2, report_file3, report_file4, report_file5, report_file6, report_file7, report_file9, report_file10, report_file11, report_file12]
  report_output_list_len = len(report_output_list)
  confluence_pageid = "62013301"
  confluence_history_pageid = "62013304"
  os.environ["CONFLUENCE_PAGEID"] = confluence_pageid
  os.environ["CONFLUENCE_HISTORY_PAGEID"] = confluence_history_pageid
  report_title = (report_number + " - capacity weekly report on: " + env)
  os.environ["REPORT_TITLE"] = report_title
  export_file_extension = (env + "_" + report_date + ".xlsx")
  export_file = (report_number + "_Capacity_weekly_" + export_file_extension)
  os.environ["EXPORT_FILE_EXTENSION"] = export_file_extension
  os.environ["EXPORT_FILE"] = export_file
  log_file_extension = (config.current_timestamp + ".log")
  log_file1 = (report_title + "_" + log_file_extension)
  os.environ["LOG_FILE_EXTENSION"] = log_file_extension
  os.environ["LOG_FILE1"] = log_file1
  log_file_list = [log_file1]
  log_file_list_len = len(log_file_list)
else:
  logger.error('Wrong or none-existing report number, exiting')
  exit(1)

config.isOFFICEnetwork(config.default_local_ip)

if verbose == True:
  logger.debug('current timestamp is: ' + config.blue + config.current_timestamp)
  logger.debug('my default ip is: ' + config.blue + config.get_ip())
  if config.office == 1:
    if verbose == True:
      logger.debug(config.blue + 'office_network is present')
    office_ip = config.default_local_ip
    os.environ["OFFICE_IP"] = office_ip
  elif config.vpn == 1:
    if verbose == True:
      logger.debug(config.blue + 'vpn is present')
    vpn_ip = config.default_local_ip
    os.environ["VPN_IP"] = vpn_ip
  else:
    if verbose == True:
      logger.debug(config.blue + 'not connected to the office')

#running appropriate BTEQ script
start_time_bash_seconds = time.time()
try:
  subprocess.check_call(scripts_home + '/bteq/report_' + report_number + '.bteq', shell=False, stdout = subprocess.PIPE)
  if verbose == True:
    logger.debug('LOG file of running BTEQ: ' + config.blue +  new_log + '/'  + log_file1)
except:
  logger.error("bteq script failed")
  sys.exit(1)
end_time_bash_seconds = time.time()
bash_seconds = [end_time_bash_seconds, -start_time_bash_seconds]
time_bash_seconds = sum(bash_seconds)

#running appropriate script for building final report based on BTEQ data
start_time_report_seconds = time.time()
#import report_302
#try:
exec(open(scripts_home + '/report_' + report_number + '.py').read())
#except:
#  logger.error("Excel conversion script failed")
#  sys.exit(1)
end_time_report_seconds = time.time()
report_seconds = [end_time_report_seconds, -start_time_report_seconds]
time_report_seconds = sum(report_seconds)

start_time_compression = time.time()
#one-by-one:
#for report_file in report_output_list:
#  config.outArchive('archiving one-by-one: ' + config.cyan + report_file, report_file, env, new_tmp)
#for log_file in log_file_list:
#  config.logArchive('archiving one-by-one: ' + config.cyan + log_file, log_file, new_log)
#in parallel
#joblib_method = "processes"
joblib_method = "threads"
Parallel(n_jobs=config.cpu_cores, prefer=joblib_method)(delayed(config.outArchive)('archiving in parallel (' + joblib_method + '): ' + config.cyan  + report_file, report_file, env, new_tmp) for report_file in report_output_list )
Parallel(n_jobs=config.cpu_cores, prefer=joblib_method)(delayed(config.logArchive)('archiving in parallel (' + joblib_method + '): ' + config.cyan  + log_file, log_file, new_log) for log_file in log_file_list )
end_time_compression = time.time()
compression_seconds = [end_time_compression, -start_time_compression]
time_compression_seconds = sum(compression_seconds)
if verbose == True:
  logger.debug(config.limon + "compression time: " + config.wine + "%.4f" % time_compression_seconds + config.limon +  " seconds")

end_time_template_seconds = time.time()
template_seconds = [end_time_template_seconds, -start_time_template_seconds]
time_template_seconds = sum(template_seconds)

python_seconds = [time_template_seconds, -time_bash_seconds, -time_report_seconds]
time_python_seconds =sum(python_seconds)

if verbose == True:
  logger.debug(config.limon + "Run time: " + config.wine + "%.4f" % time_template_seconds + config.limon +  " seconds")
  logger.debug(config.limon + "BASH script run for: " + config.wine + "%.4f" % time_bash_seconds + config.limon +  " seconds")
  logger.debug(config.limon + "Python script run for: " + config.wine + "%.4f" % time_python_seconds + config.limon + " seconds")
  logger.debug(config.limon + "Report build script run for: " + config.wine + "%.4f" % time_report_seconds + config.limon + " seconds")
