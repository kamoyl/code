#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#from __main__ import *
import sys
#import getopt
import logging
import coloredlogs
import os
import datetime
#import subprocess
import time
import pandas
#import re
#import gzip
#import shutil
import multiprocessing as mp
import threading
import numpy
import csv
#import glob
import joblib
#from xlsxwriter import Workbook
import xlsxwriter
#from xlsxwriter.utility import xl_rowcol_to_cell

import config

try:
  from StringIO import StringIO
except ImportError:
  from io import StringIO

from colorama import init,Fore, Back, Style
init(autoreset=True)
from termcolor import colored
reload(sys)
sys.setdefaultencoding('utf8')

with open(new_tmp + '/' + report_file3, "a+b") as report_file3_open:
  row_list = report_file3_open.readlines()[1:2]
  max_perm = float(row_list[0].split('~')[3])
  avg_perm = float(row_list[0].split('~')[2])
  skew_factor = (100*(max_perm - avg_perm)/max_perm)
  report_file3_open.write('~~~~~System skew factor\n')
  report_file3_open.write('~~~~~' + str(skew_factor) + ' %\n')

with open(new_tmp + '/' + report_file2, "a+b") as report_file2_open:
  with open(new_tmp + '/' + report_file3, "r") as report_file3_open:
    report_file3_read = report_file3_open.read()
    report_file2_open.write('\n\n\n\n')
    report_file2_open.write(report_file3_read)

logger.info("Few manipulations for AWT extract data")
def AWTweekly(title):
  if verbose == True:
    logger.debug(config.wine + '    start: ' + config.yellow + title)
  with open(new_tmp + '/' + report_file8, "r") as report_file8_open:
    def AWTweekly(title):
      if verbose == True:
        logger.debug(config.wine + '    start: ' + config.yellow + title)
      for day_week_range in range(1,8):
        date_week = (report_date_long - datetime.timedelta(days=day_week_range)).strftime("%Y-%m-%d")
        report_file8_open.seek(0,0)
        week_prep_variable = ""
        for week_line in report_file8_open:
          if date_week in week_line:
            week_prep_variable = week_prep_variable + week_line
        week_prep_variable_fakefile = StringIO(week_prep_variable)
        df_AWT_grid_graph_weekly=pandas.read_csv(week_prep_variable_fakefile, delimiter='~',header=0,names=['TheDate','thistime','WD_ETL','WD_OTHER'])
        weekly_transpose = df_AWT_grid_graph_weekly.set_index('TheDate').T
        with open(new_tmp + '/' + report_file10, "a+b") as weekly_transpose_result:
          weekly_transpose.to_csv(weekly_transpose_result,index=True,header=1,sep='~')
          weekly_transpose_result.write('\n\n')
      if verbose == True:
        logger.debug(config.wine + '      end: ' + config.yellow + title)
    def AWTweeklyPAR(title, day_week):
      if verbose == True:
        logger.debug(config.wine + '    start: ' + config.yellow + title)
      date_week = (report_date_long - datetime.timedelta(days=day_week)).strftime("%Y-%m-%d")
      report_file8_open.seek(0,0)
      week_prep_variable = ""
      for week_line in report_file8_open:
        if date_week in week_line:
          week_prep_variable = week_prep_variable + week_line
      week_prep_variable_fakefile = StringIO(week_prep_variable)
      df_AWT_grid_graph_weekly=pandas.read_csv(week_prep_variable_fakefile, delimiter='~',header=0,names=['TheDate','thistime','WD_ETL','WD_OTHER'])
      weekly_transpose = df_AWT_grid_graph_weekly.set_index('TheDate').T
      with open(new_tmp + '/' + report_file10, "a+b") as weekly_transpose_result:
        weekly_transpose.to_csv(weekly_transpose_result,index=True,header=1,sep='~')
        weekly_transpose_result.write('\n\n')
      if verbose == True:
        logger.debug(config.wine + '      end: ' + config.yellow + title)
    if multiload == True:
      joblib_method = "processes"
      start_time_AWTweeklyRange_load = time.time()
      joblib.Parallel(n_jobs=config.cpu_cores, prefer=joblib_method)(joblib.delayed(AWTweeklyPAR)('AWT weekly in range parallel (' + joblib_method + '): ' + config.cyan  + str(day_week_range), day_week_range) for day_week_range in range(1,8) )
      end_time_AWTweeklyRange_load = time.time()
      AWTweeklyRange_seconds = [end_time_AWTweeklyRange_load, -start_time_AWTweeklyRange_load]
      time_AWTweeklyRange_seconds = sum(AWTweeklyRange_seconds)
      if showtime == True:
        logger.debug(config.limon + "   AWTweekly range of days (parallel) load: " + config.wine + "%.4f" % time_AWTweeklyRange_seconds + config.limon +  " seconds")
    else:
      start_time_AWTweeklyRange_load = time.time()
      AWTweekly('AWT weekly in range one process' + config.cyan)
      end_time_AWTweeklyRange_load = time.time()
      AWTweeklyRange_seconds = [end_time_AWTweeklyRange_load, -start_time_AWTweeklyRange_load]
      time_AWTweeklyRange_seconds = sum(AWTweeklyRange_seconds)
      if showtime == True:
        logger.debug(config.limon + "   AWTweekly range of days (same process/thread) load: " + config.wine + "%.4f" % time_AWTweeklyRange_seconds + config.limon +  " seconds")
  if verbose == True:
    logger.debug(config.wine + '      end: ' + config.yellow + title)

def AWTmonthly(title):
  if verbose == True:
    logger.debug(config.wine + '    start: ' + config.yellow + title)
  with open(new_tmp + '/' + report_file8, "r") as report_file8_open:
    df_AWT_grid_graph_monthly=pandas.read_csv(new_tmp + '/' + report_file8, "r",delimiter='~',header=0,names=['TheDate','thistime','WD_ETL','WD_OTHER'])
    df_AWT_grid_graph_monthly_pivot = df_AWT_grid_graph_monthly.pivot_table(index='TheDate', columns='thistime', values=['WD_ETL','WD_OTHER'], aggfunc=numpy.sum)
    df_AWT_grid_graph_monthly_pivot.to_csv(new_tmp + '/' + report_file11,index=True,header=1,sep='~')
  if verbose == True:
    logger.debug(config.wine + '      end: ' + config.yellow + title)

def AWTdaily(title):
  if verbose == True:
    logger.debug(config.wine + '    start: ' + config.yellow + title)
  with open(new_tmp + '/' + report_file8, "r") as report_file8_open:
    next(report_file8_open)
    day_date_list = [ ]
    for day_line in report_file8_open:
      day_date = day_line.split('~')[0]
      day_date_list.append(day_date)
    days_list_set = set(day_date_list)
    days_list = list(days_list_set)
    days_list_sorted = sorted(days_list)
    days_sorted_amount = len(days_list_sorted)
    for day in days_list_sorted:
      report_file8_open.seek(0,0)
      day_line_string = ""
      for day_line in report_file8_open:
        if day in day_line:
          day_line_string = day_line_string + day_line
      daily_file = StringIO(day_line_string)
      df_AWT_grid_graph=pandas.read_csv(daily_file,delimiter='~',header=0,names=['TheDate','thistime','WD_ETL','WD_OTHER'])
      daily_transpose = df_AWT_grid_graph.set_index('TheDate').T
      with open(new_tmp + '/' + report_file12, "a+b") as daily_transpose_final:
        daily_transpose.to_csv(daily_transpose_final,index=True,header=1,sep='~')
        daily_transpose_final.write('\n\n')
  os.remove(new_tmp + '/' + report_file8)
  if verbose == True:
    logger.debug(config.wine + '      end: ' + config.yellow + title)

def convert_to_excel(title, exportFileName):
  start_time_excel_load = time.time()
  if verbose == True:
    logger.debug(config.wine + '    start: ' + config.yellow + title)
  workbook = xlsxwriter.Workbook(new_tmp + '/' + exportFileName, {'strings_to_numbers': True})
  columns = {}
  rows = {}
  logger.info('    Converting exported data into M$ Excel sheet (loading data): ' + config.cyan + export_file)
  def LoadingToWorkbookPAR(title, filename):
    if verbose == True:
      logger.debug(config.wine + '    start: ' + config.yellow + title)
  #for filename in report_output_list:
    spamReader = csv.reader((open(new_tmp + '/' + filename, 'rb')), delimiter='~', quotechar='"')
    newWorksheetName = filename.replace('.out', '')
    worksheet = workbook.add_worksheet(newWorksheetName)
    for rowx, row in enumerate(spamReader):
      for colx, value in enumerate(row):
        worksheet.write(rowx, colx, value)
        columns[newWorksheetName + '_columns']=colx+1
        rows[newWorksheetName + '_rows']=rowx+1
    if verbose == True:
      logger.debug(config.wine + '      end: ' + config.yellow + title)
  joblib_method = "threads"
  joblib.Parallel(n_jobs=config.cpu_cores, prefer=joblib_method)(joblib.delayed(LoadingToWorkbookPAR)('loading in parallel (' + joblib_method + '): ' + config.cyan  + report_file, report_file) for report_file in report_output_list )
  end_time_excel_load = time.time()
  excel_load_seconds = [end_time_excel_load, -start_time_excel_load]
  time_excel_load_seconds = sum(excel_load_seconds)
  if showtime == True:
    logger.debug(config.limon + "Data loaded to excel time: " + config.wine + "%.4f" % time_excel_load_seconds + config.limon +  " seconds")
  logger.info('    Converting exported data into M$ Excel sheet (actual convert data): ' + config.cyan + export_file)
  # color scale in overall_system_activity
  format_green = workbook.add_format({'bg_color': '#C6EFCE',})
  format_orange = workbook.add_format({'bg_color': '#FFEB9C',})
  format_red = workbook.add_format({'bg_color': '#FFC7CE',})
  format_navy = workbook.add_format({'bg_color': '#001f3f',})
  format_blue = workbook.add_format({'bg_color': '#0074D9',})
  format_aqua = workbook.add_format({'bg_color': '#7FDBFF',})
  format_teal = workbook.add_format({'bg_color': '#39CCCC',})
  format_olive = workbook.add_format({'bg_color': '#3D9970',})
  format_lime = workbook.add_format({'bg_color': '#01FF70',})
  format_yellow = workbook.add_format({'bg_color': '#FFDC00',})
  format_maroon = workbook.add_format({'bg_color': '#85144b',})
  format_fuchsia = workbook.add_format({'bg_color': '#F012BE',})
  bold = workbook.add_format({'bold': True})

  #format of numbers
  format_decimal = workbook.add_format()
  format_decimal.set_num_format('0.00')
  format_cut_decimal = workbook.add_format()
  format_cut_decimal.set_num_format('0')
  format_text = workbook.add_format({'num_format': '@'})
  #merging format:
  merge_format = workbook.add_format({
    'bold': 1,
    'border': 0,
    'align': 'center',
    'valign': 'vcenter'})
  # sheets
  worksheet_1_Diskspace = workbook.get_worksheet_by_name('1_Diskspace')
  worksheet_2_Diskspace_trend = workbook.get_worksheet_by_name('2_Diskspace_trend')
  worksheet_3_cpu_COD_busy_monthly = workbook.get_worksheet_by_name('3_cpu_COD_busy_monthly')
  worksheet_4_cpu_ImpactCPU_monthly = workbook.get_worksheet_by_name('4_cpu_ImpactCPU_monthly')
  worksheet_5_flow_control_heat_map = workbook.get_worksheet_by_name('5_flow_control_heat_map')
  worksheet_7_Ampconfig = workbook.get_worksheet_by_name('7_Ampconfig')
  worksheet_8_cpu_Hourly_Details = workbook.get_worksheet_by_name('8_cpu_Hourly_Details')
  worksheet_9_cpu_Weekday_Details = workbook.get_worksheet_by_name('9_cpu_Weekday_Details')
  worksheet_10_AWT_grid_graph_daily = workbook.get_worksheet_by_name('6_AWT_grid_graph_daily')
  worksheet_11_AWT_grid_graph_weekly = workbook.get_worksheet_by_name('6_AWT_grid_graph_weekly')
  worksheet_12_AWT_grid_graph_monthly = workbook.get_worksheet_by_name('6_AWT_grid_graph_monthly')
  # autofilter (should be dynamically created - accordingly to amount of columns)
  worksheet_7_Ampconfig.autofilter('A1:H1')
  worksheet_3_cpu_COD_busy_monthly.autofilter('A1:Z1')
  #worksheet_4_cpu_ImpactCPU_monthly.autofilter('A1:Y1')
  worksheet_8_cpu_Hourly_Details.autofilter('A1:V1')
  worksheet_9_cpu_Weekday_Details.autofilter('A1:G1')
  # Make the header row larger.
  worksheet_1_Diskspace.set_row(0, None, bold)
  worksheet_1_Diskspace.set_row(23, None, bold)
  worksheet_1_Diskspace.set_row(25, None, bold)
  worksheet_2_Diskspace_trend.set_row(0, None, bold)
  worksheet_3_cpu_COD_busy_monthly.set_row(0, None, bold)
  worksheet_4_cpu_ImpactCPU_monthly.set_row(0, None, bold)
  worksheet_5_flow_control_heat_map.set_row(0, None, bold)
  worksheet_10_AWT_grid_graph_daily.set_row(0, None, bold)
  worksheet_10_AWT_grid_graph_daily.set_row(1, None, bold)
  worksheet_11_AWT_grid_graph_weekly.set_row(0, None, bold)
  worksheet_11_AWT_grid_graph_weekly.set_row(1, None, bold)
  worksheet_12_AWT_grid_graph_monthly.set_row(0, None, bold)
  worksheet_12_AWT_grid_graph_monthly.set_row(1, None, bold)
  worksheet_7_Ampconfig.set_row(0, None, bold)
  worksheet_8_cpu_Hourly_Details.set_row(0, None, bold)
  worksheet_9_cpu_Weekday_Details.set_row(0, None, bold)
  # some format applied on sheet tabs
  worksheet_7_Ampconfig.set_tab_color('yellow')
  worksheet_3_cpu_COD_busy_monthly.set_tab_color('green')
  worksheet_4_cpu_ImpactCPU_monthly.set_tab_color('#16A085')
  worksheet_8_cpu_Hourly_Details.set_tab_color('#ff00ff')
  worksheet_9_cpu_Weekday_Details.set_tab_color('#0000ff')
  worksheet_1_Diskspace.set_tab_color('#A569BD')
  worksheet_2_Diskspace_trend.set_tab_color('#2980B9')
  worksheet_5_flow_control_heat_map.set_tab_color('#FF851B')
  worksheet_10_AWT_grid_graph_daily.set_tab_color('lime')
  worksheet_12_AWT_grid_graph_monthly.set_tab_color('#03FF70')
  worksheet_11_AWT_grid_graph_weekly.set_tab_color('#05FF70')

  # decimal format applied to some columns:
  worksheet_1_Diskspace.set_column('A:E', 15)
  worksheet_1_Diskspace.set_column('F:F', 23)
  worksheet_3_cpu_COD_busy_monthly.set_column('A:C', 16)
  worksheet_3_cpu_COD_busy_monthly.set_column('D:AA', 6, format_cut_decimal)
  worksheet_3_cpu_COD_busy_monthly.set_column('AB:AB', 23, format_cut_decimal)
  worksheet_4_cpu_ImpactCPU_monthly.set_column('A:A', 10)
  worksheet_4_cpu_ImpactCPU_monthly.set_column('B:Y', 6, format_cut_decimal)
  worksheet_4_cpu_ImpactCPU_monthly.set_column('Z:Z', 15)
  worksheet_5_flow_control_heat_map.set_column('A:A', 10)
  worksheet_5_flow_control_heat_map.set_column('B:AW', 5)
  worksheet_5_flow_control_heat_map.set_column('AX:AX', 17)
  worksheet_10_AWT_grid_graph_daily.set_column('A:A', 11)
  worksheet_10_AWT_grid_graph_daily.set_column('B:EN', 10)
  worksheet_11_AWT_grid_graph_weekly.set_column('A:A', 16)
  worksheet_11_AWT_grid_graph_weekly.set_column('B:EN', 10)
  worksheet_11_AWT_grid_graph_weekly.set_row(42, 20, format_cut_decimal)
  worksheet_11_AWT_grid_graph_weekly.set_row(43, 20, format_cut_decimal)
  worksheet_12_AWT_grid_graph_monthly.set_column('A:A', 10)
  worksheet_12_AWT_grid_graph_monthly.set_column('B:KC', 8)
  worksheet_12_AWT_grid_graph_monthly.set_row(35, None, format_cut_decimal)
  worksheet_7_Ampconfig.set_column('A:H', 23, format_cut_decimal)
  #conditional formatting 
  worksheet_3_cpu_COD_busy_monthly.conditional_format('D2:AB' + str(rows['3_cpu_COD_busy_monthly_rows']), {'type':   'cell',
    'criteria': '<=',
    'value':    50,
    'format':   format_green})
  worksheet_3_cpu_COD_busy_monthly.conditional_format('D2:AC' + str(rows['3_cpu_COD_busy_monthly_rows']), {'type':   'cell',
    'criteria': 'between',
    'minimum':  51,
    'maximum':  80,
    'format':   format_orange})
  worksheet_3_cpu_COD_busy_monthly.conditional_format('D2:AC' + str(rows['3_cpu_COD_busy_monthly_rows']), {'type':   'cell',
    'criteria': '>=',
    'value':    81,
    'format':   format_red})
  worksheet_4_cpu_ImpactCPU_monthly.conditional_format('B2:Z' + str(rows['4_cpu_ImpactCPU_monthly_rows']), {'type':   'cell',
    'criteria': '<=',
    'value':    50,
    'format':   format_green})
  worksheet_4_cpu_ImpactCPU_monthly.conditional_format('B2:Z' + str(rows['4_cpu_ImpactCPU_monthly_rows']), {'type':   'cell',
    'criteria': 'between',
    'minimum':  51,
    'maximum':  80,
    'format':   format_orange})
  worksheet_4_cpu_ImpactCPU_monthly.conditional_format('B2:Z' + str(rows['4_cpu_ImpactCPU_monthly_rows']), {'type':   'cell',
    'criteria': '>=',
    'value':    81,
    'format':   format_red})
  worksheet_5_flow_control_heat_map.conditional_format('B2:AX' + str(rows['5_flow_control_heat_map_rows']), {'type':   'cell',
    'criteria': '<=',
    'value':    0,
    'format':   format_green})
  worksheet_5_flow_control_heat_map.conditional_format('B2:AX' + str(rows['5_flow_control_heat_map_rows']), {'type':   'cell',
    'criteria': 'between',
    'minimum':  0.1,
    'maximum':  0.99,
    'format':   format_orange})
  worksheet_5_flow_control_heat_map.conditional_format('B2:AX' + str(rows['5_flow_control_heat_map_rows']), {'type':   'cell',
    'criteria': '>=',
    'value':    1,
    'format':   format_red})
  Diskspace_trend = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
  Diskspace_trend.set_style(10)

  Diskspace_trend.add_series({
    'name': '=1_Diskspace!$E$1',
    'categories': '=1_Diskspace!$A$2:$A$' + str(rows['1_Diskspace_rows']-8),
    'values': '=1_Diskspace!$E$2:$E$' + str(rows['1_Diskspace_rows']-8),
  })
  Diskspace_trend.add_series({
    'name': '=1_Diskspace!$F$1',
    'categories': '=1_Diskspace!$A$2:$A$' + str(rows['1_Diskspace_rows']-8),
    'values': '=1_Diskspace!$F$2:$F$' + str(rows['1_Diskspace_rows']-8),
  })
  Diskspace_trend.set_legend({
    'position': 'right'
  })
  Diskspace_trend.set_size({'width': 1400, 'height': 550})
  worksheet_2_Diskspace_trend.insert_chart('A1', Diskspace_trend)

  chart_cpu_per_hour = workbook.add_chart({'type': 'line'})
  chart_cpu_per_hour.set_title ({'name': '=3_cpu_COD_busy_monthly!$AB$1'})
  chart_cpu_per_hour.add_series({
    'name': '=3_cpu_COD_busy_monthly!$AB$1',
    'categories': '=3_cpu_COD_busy_monthly!$B$2:$B$' + str(rows['3_cpu_COD_busy_monthly_rows']),
    'values': '=3_cpu_COD_busy_monthly!$AB$2:$AB$' + str(rows['3_cpu_COD_busy_monthly_rows']),
    'line':   {'width': 2.25},
    'marker': {
      'type': 'automatic',
      'size': '5',
      },
  })
  chart_cpu_per_hour.set_size({'width': 1300, 'height': 550})
  worksheet_3_cpu_COD_busy_monthly.insert_chart('A38', chart_cpu_per_hour)

# daily grap AWT in a loop - 30 charts must be here
  name = 1
  wd_etl = 3
  wd_other = 4
  chart = 1
  bolding = 0
  for x in xrange(1, 32):
    #merging:
    worksheet_10_AWT_grid_graph_daily.merge_range('C' + str(name) + ':EN' + str(name), None, merge_format)
    worksheet_10_AWT_grid_graph_daily.set_row(bolding, None, bold)
    worksheet_10_AWT_grid_graph_daily.set_row(name, None, bold)
    daily_gridgraph = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
    daily_gridgraph.set_title ({'name': '=6_AWT_grid_graph_daily!$B$' + str(name)}) #next B7
    daily_gridgraph.set_style(10)

    daily_gridgraph.add_series({
      'name': '=6_AWT_grid_graph_daily!$A$3',
      'categories': '=6_AWT_grid_graph_daily!$B$2:$EN$2',
      'values': '=6_AWT_grid_graph_daily!$B$' + str(wd_etl) + ':$EN$' + str(wd_etl),     #next B9, B15 +6
    })
    daily_gridgraph.add_series({
      'name': '=6_AWT_grid_graph_daily!$A$4',
      'categories': '=6_AWT_grid_graph_daily!$B$2:$EN$2',
      'values': '=6_AWT_grid_graph_daily!$B$' + str(wd_other) + ':$F$' + str(wd_other),       #next B10, B16...
    })
    daily_gridgraph.set_legend({
      'position': 'right'
    })
    daily_gridgraph.set_x_axis({'name': 'Time: HH:MM'})
    daily_gridgraph.set_y_axis({'name': 'Workload'})
    daily_gridgraph.set_size({'width': 1880, 'height': 400})
    worksheet_10_AWT_grid_graph_daily.insert_chart('A' + str(chart), daily_gridgraph) #next chart A7
    worksheet_10_AWT_grid_graph_daily.conditional_format('B' + str(wd_etl)  + ':EN' + str(wd_other), {'type':   'cell',
      'criteria': '<=',
      'value':    50,
      'format':   format_green})
    worksheet_10_AWT_grid_graph_daily.conditional_format('B' + str(wd_etl)  + ':EN' + str(wd_other), {'type':   'cell',
      'criteria': 'between',
      'minimum':  51,
      'maximum':  80,
      'format':   format_orange})
    worksheet_10_AWT_grid_graph_daily.conditional_format('B' + str(wd_etl)  + ':EN' + str(wd_other), {'type':   'cell',
      'criteria': '>=',
      'value':    81,
      'format':   format_red})
    chart = chart + 20
    name = name + 6
    wd_etl = wd_etl + 6
    wd_other = wd_other + 6
    bolding = bolding + 6
  #weekly
  worksheet_11_AWT_grid_graph_weekly.write(42, 0, 'Avg WD_ETL')
  worksheet_11_AWT_grid_graph_weekly.write(43, 0, 'Avg WD_OTHER')
  for col in xrange(1, 144):
    cell1 = xlsxwriter.utility.xl_rowcol_to_cell(2, col)
    cell2 = xlsxwriter.utility.xl_rowcol_to_cell(8, col)
    cell3 = xlsxwriter.utility.xl_rowcol_to_cell(14, col)
    cell4 = xlsxwriter.utility.xl_rowcol_to_cell(20, col)
    cell5 = xlsxwriter.utility.xl_rowcol_to_cell(26, col)
    cell6 = xlsxwriter.utility.xl_rowcol_to_cell(32, col)
    cell7 = xlsxwriter.utility.xl_rowcol_to_cell(38, col)
    cell11 = xlsxwriter.utility.xl_rowcol_to_cell(3, col)
    cell21 = xlsxwriter.utility.xl_rowcol_to_cell(9, col)
    cell31 = xlsxwriter.utility.xl_rowcol_to_cell(15, col)
    cell41 = xlsxwriter.utility.xl_rowcol_to_cell(21, col)
    cell51 = xlsxwriter.utility.xl_rowcol_to_cell(27, col)
    cell61 = xlsxwriter.utility.xl_rowcol_to_cell(33, col)
    cell71 = xlsxwriter.utility.xl_rowcol_to_cell(39, col)
    worksheet_11_AWT_grid_graph_weekly.write_formula(42, col, '=AVERAGE(' + str(cell1) + ',' + str(cell2) + ',' + str(cell3) + ',' + str(cell4) + ',' + str(cell5) + ',' + str(cell6) + ',' + str(cell7) + ')')
    worksheet_11_AWT_grid_graph_weekly.write_formula(43, col, '=AVERAGE(' + str(cell11) + ',' + str(cell21) + ',' + str(cell31) + ',' + str(cell41) + ',' + str(cell51) + ',' + str(cell61) + ',' + str(cell71) + ')')
  worksheet_11_AWT_grid_graph_weekly.conditional_format('B43:EN44', {'type':   'cell',
    'criteria': '<=',
    'value':    50,
    'format':   format_green})
  worksheet_11_AWT_grid_graph_weekly.conditional_format('B43:EN44', {'type':   'cell',
    'criteria': 'between',
    'minimum':  51,
    'maximum':  80,
    'format':   format_orange})
  worksheet_11_AWT_grid_graph_weekly.conditional_format('B43:EN44', {'type':   'cell',
    'criteria': '>=',
    'value':    81,
    'format':   format_red})
  chart_gridgraph_weekly = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
  chart_gridgraph_weekly.set_title ({'name': 'AWT Grid Graph - last 7 days'})
  chart_gridgraph_weekly.add_series({
    'name': '=6_AWT_grid_graph_weekly!$A$3',
    'categories': '=6_AWT_grid_graph_weekly!$B$2:$EN$2',
    'values': '=6_AWT_grid_graph_weekly!$B$43:$EN$43',
  })

  chart_gridgraph_weekly.add_series({
    'name': '=6_AWT_grid_graph_weekly!$A$4',
    'categories': '=6_AWT_grid_graph_weekly!$B$2:$EN$2',
    'values': '=6_AWT_grid_graph_weekly!$B$44:$EN$44',
  })

  chart_gridgraph_weekly.set_x_axis({'name': 'Time: HH:MM'})
  chart_gridgraph_weekly.set_y_axis({'name': 'Workload average'})
  chart_gridgraph_weekly.set_size({'width': 1880, 'height': 650})
  worksheet_11_AWT_grid_graph_weekly.insert_chart('A1', chart_gridgraph_weekly)
  #monthly
  worksheet_12_AWT_grid_graph_monthly.write(35, 0, 'Avg')
  worksheet_12_AWT_grid_graph_monthly.merge_range('C1:EO1', None, merge_format)
  worksheet_12_AWT_grid_graph_monthly.merge_range('EQ1:KC1', None, merge_format)
  for col in xrange(1, 289):
    cellX = xlsxwriter.utility.xl_rowcol_to_cell(3, col)
    cellY = xlsxwriter.utility.xl_rowcol_to_cell(33, col)
    worksheet_12_AWT_grid_graph_monthly.write_formula(35, col, '=AVERAGE(' + str(cellX) + ':' + str(cellY) + ')')
  worksheet_12_AWT_grid_graph_monthly.conditional_format('B36:KC36', {'type':   'cell',
    'criteria': '<=',
    'value':    50,
    'format':   format_green})
  worksheet_12_AWT_grid_graph_monthly.conditional_format('B36:KC36', {'type':   'cell',
   'criteria': 'between',
    'minimum':  51,
    'maximum':  80,
    'format':   format_orange})
  worksheet_12_AWT_grid_graph_monthly.conditional_format('B36:KC36', {'type':   'cell',
    'criteria': '>=',
    'value':    81,
    'format':   format_red})
  worksheet_12_AWT_grid_graph_monthly.conditional_format('B4:KC' + str(rows['6_AWT_grid_graph_monthly_rows']), {'type':   'cell',
    'criteria': '<=',
    'value':    50,
    'format':   format_green})
  worksheet_12_AWT_grid_graph_monthly.conditional_format('B4:KC' + str(rows['6_AWT_grid_graph_monthly_rows']), {'type':   'cell',
    'criteria': 'between',
    'minimum':  51,
    'maximum':  80,
    'format':   format_orange})
  worksheet_12_AWT_grid_graph_monthly.conditional_format('B4:KC' + str(rows['6_AWT_grid_graph_monthly_rows']), {'type':   'cell',
    'criteria': '>=',
    'value':    81,
    'format':   format_red})
  chart_gridgraph = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
  chart_gridgraph.set_title ({'name': 'AWT Grid Graph - last 31 days'})
  chart_gridgraph.add_series({
    'name': '=6_AWT_grid_graph_monthly!$B$1',
    'categories': '=6_AWT_grid_graph_monthly!$B$2:$EO$2',
    'values': '=6_AWT_grid_graph_monthly!$B$36:$EO$36',
  })

  chart_gridgraph.add_series({
    'name': '=6_AWT_grid_graph_monthly!$EP$1',
    'categories': '=6_AWT_grid_graph_monthly!$B$2:$EO$2',
    'values': '=6_AWT_grid_graph_monthly!$EP$36:$KC$36',
  })

  chart_gridgraph.set_x_axis({'name': 'Time: HH:MM'})
  chart_gridgraph.set_y_axis({'name': 'Workload average'})
  chart_gridgraph.set_size({'width': 1880, 'height': 500})
  worksheet_12_AWT_grid_graph_monthly.insert_chart('A37', chart_gridgraph)

  # order of sheets in workbook
  workbook.worksheets_objs.sort(key=lambda x: x.name)
  workbook.close()
  if verbose == True:
    logger.debug(config.wine + '      end: ' + config.yellow + title)

weekly = mp.Process(target=AWTweekly, args=('AWT weekly spawned (separated process): ' + config.cyan + report_file10,))
monthly = mp.Process(target=AWTmonthly, args=('AWT monthly spawned (separated process): ' + config.cyan + report_file11,))
daily = mp.Process(target=AWTdaily, args=('AWT daily spawned (separated process): ' + config.cyan + report_file12,))
convert = mp.Process(target=convert_to_excel, args=('Convertion of files into Excel sheet (separated process): ' + config.cyan + export_file, export_file, ))

#w = threading.Thread(target=AWTweekly, args=('AWT weekly spawned',))
#m = threading.Thread(target=AWTmonthly, args=('AWT monthly spawned',))
#d = threading.Thread(target=AWTdaily, args=('AWT monthly spawned',))
if multiload == True:
  start_time_AWTweekly_load = time.time()
  weekly.start()
  start_time_AWTmonthly_load = time.time()
  monthly.start()
  start_time_AWTdaily_load = time.time()
  daily.start()

  monthly.join()
  end_time_AWTmonthly_load = time.time()
  weekly.join()
  end_time_AWTweekly_load = time.time()
  daily.join()
  end_time_AWTdaily_load = time.time()

  AWTmonthly_load_seconds = [end_time_AWTmonthly_load, -start_time_AWTmonthly_load]
  time_AWTmonthly_load_seconds = sum(AWTmonthly_load_seconds)
  AWTweekly_load_seconds = [end_time_AWTweekly_load, -start_time_AWTweekly_load]
  time_AWTweekly_load_seconds = sum(AWTweekly_load_seconds)
  AWTdaily_load_seconds = [end_time_AWTdaily_load, -start_time_AWTdaily_load]
  time_AWTdaily_load_seconds = sum(AWTdaily_load_seconds)
  if showtime == True:
    logger.debug(config.limon + "AWTdaily calculation time (separated process: " + config.cyan + str(multiload) + config.limon +  "): " + config.wine + "%.4f" % time_AWTdaily_load_seconds + config.limon +  " seconds")
    logger.debug(config.limon + "AWTweekly calculation time (separated process: " + config.cyan + str(multiload) + config.limon +  "): " + config.wine + "%.4f" % time_AWTweekly_load_seconds + config.limon +  " seconds")
    logger.debug(config.limon + "AWTmonthly calculation time: " + config.wine + "%.4f" % time_AWTmonthly_load_seconds + config.limon +  " seconds")
else:
  start_time_AWTweekly_load = time.time()
  AWTweekly('AWT weekly run (same process/thread): ' + config.cyan + report_file10)
  end_time_AWTweekly_load = time.time()
  start_time_AWTmonthly_load = time.time()
  AWTmonthly('AWT monthly run (same process/thread): ' + config.cyan + report_file11)
  end_time_AWTmonthly_load = time.time()
  start_time_AWTdaily_load = time.time()
  AWTdaily('AWT daily run (same process/thread): ' + config.cyan + report_file12)
  end_time_AWTdaily_load = time.time()

  AWTmonthly_load_seconds = [end_time_AWTmonthly_load, -start_time_AWTmonthly_load]
  time_AWTmonthly_load_seconds = sum(AWTmonthly_load_seconds)
  AWTweekly_load_seconds = [end_time_AWTweekly_load, -start_time_AWTweekly_load]
  time_AWTweekly_load_seconds = sum(AWTweekly_load_seconds)
  AWTdaily_load_seconds = [end_time_AWTdaily_load, -start_time_AWTdaily_load]
  time_AWTdaily_load_seconds = sum(AWTdaily_load_seconds)
  
  if showtime == True:
    logger.debug(config.limon + "AWTdaily calculation time (same process/thread): " + config.wine + "%.4f" % time_AWTdaily_load_seconds + config.limon +  " seconds")
    logger.debug(config.limon + "AWTweekly calculation time (same process/thread): " + config.wine + "%.4f" % time_AWTweekly_load_seconds + config.limon +  " seconds")
    logger.debug(config.limon + "AWTmonthly calculation time (same process/thread): " + config.wine + "%.4f" % time_AWTmonthly_load_seconds + config.limon +  " seconds")

start_time_excel_conversion = time.time()
if multiload == True:
  convert.start()
  convert.join()
else:
  convert_to_excel('Convertion of files into Excel sheet (same process/thread): ' + config.cyan + export_file, export_file)
end_time_excel_conversion = time.time()
excel_conversion_seconds = [end_time_excel_conversion, -start_time_excel_conversion]
time_excel_conversion_seconds = sum(excel_conversion_seconds)
if showtime == True:
  logger.debug(config.limon + "Excel conversion time: " + config.wine + "%.4f" % time_excel_conversion_seconds + config.limon +  " seconds")
