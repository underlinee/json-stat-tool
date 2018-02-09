#!/usr/bin/python

from datetime import datetime, timedelta
import importlib
import argparse

import puller

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('module', help='an module for log analyzing')
    parser.add_argument('file', help='a file which contains target log file list')

    parser.add_argument('--start', help='start date of the log file [yyyymmdd]')
    parser.add_argument('--end', help='end date of the log file [yyyymmdd]')

    args = parser.parse_args()

    start = datetime.strptime(args.start, '%Y%m%d')
    end = datetime.strptime(args.end, '%Y%m%d')
    date = start

    puller = puller.LogPuller(args.file)
    files = []
    while date <= end:
        files = files + puller.pull(date)
        date = date + timedelta(1)

    analizer = importlib.import_module(args.module).Analizer()
    print(analizer.analize(files))
