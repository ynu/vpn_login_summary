#!/usr/bin/env python3
#coding=utf-8

import os
import os.path
import glob
import re
from mylogger import logger

def find_log_files(dir):
    log_files = []
    for file in glob.glob(dir + os.path.sep + "notice.*"):
        log_files.append(file) 
    return log_files

# pattern = re.compile(r'(?:.*)vpn=vpn user="(\d+)(?:@vpn)?"(?:.*)')
pattern = re.compile(r'(?:.*)vpn=vpn user="(\d+)(?:@vpn)?(?:.*)')
def parse(line):
    match = pattern.match(line)
    if match:
        vpn_account = match.group(1)
        logger.debug('find vpn account {}', vpn_account)
        return vpn_account
    return None

summary_data = {}
def parse_log_file(log_file):
    with open(log_file) as file:
        for line in file:
            vpn_account = parse(line)
            if vpn_account:
                if not vpn_account in summary_data:
                    summary_data[vpn_account] = 1
                else:
                    summary_data[vpn_account] += 1
            else:
                logger.debug('not find vpn account in {}', line)

def write_result_to_csv(csv_file_path):
    import csv
    with open(csv_file_path, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["vpn_account", "counts"])
        for key, value in summary_data.items(): 
            logger.info('write summary data {}', [key, value])
            spamwriter.writerow([key, value])

for log_file in find_log_files('data'):
    logger.info('process log file {}', log_file)
    parse_log_file(log_file)
logger.info('write summary data file {}', "summary.csv")
write_result_to_csv("summary.csv")