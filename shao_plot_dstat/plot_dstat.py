#!/usr/bin/env python3

'''
This file will plot the data rate extract from dstat file
'''

import os
import logging
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import argparse
from datetime import datetime

def config_logging(debug):
    '''
       Auxiliary function to configure logging
    '''

    # https://realpython.com/python-logging/
    # https://bit.ly/2VHKM44
    logFormatter = logging.Formatter(
        "# %(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    if debug:
        rootLogger.setLevel(logging.DEBUG)

def get_csv_contents(logfile):
    fp = open(logfile)
    all_content = fp.readlines()
    #print (all_content)
    return all_content

def get_csv_header(logfile):
    all_data = get_csv_contents(logfile)
    for i in all_data:
        if 'Cmdline' in i:
            print(i)
            return i

def get_csv_data(logfile):
    all_data = get_csv_contents(logfile)
    tt = []
    for i in all_data:
        if '"' not in i:
            tt.append(i)
    return tt

def get_data_time(logfile):
    t = get_csv_data(logfile)
    data_time = []
    for i in t:
        if i == '\n':
            pass
        else:
            data_time.append('2020-'+(i.split(',')[0]))
    return data_time


def plot_dstat_recv_rate(
        data,
        xaxis=None,
        infile='',
        title = 'Network Rate',
        outfile=datetime.now().__format__('NetworkTest-%Y%m%d%H%M%S.png'),
        locator = 'second',
        unit = 'Mbps',
        debug=True):
    '''
    Will plot a data rate from dstat logfile
    Parameters
    ----------
    data : list
        The data rate list from dstat logfile
    infile : string
        Mandatory argument to show dstat log file name in the figure title
    outfile : string, optional
        Default in format `NetworkTest-%Y%m%d%H%M%S.png`, better specify in comand line
    debug : bool, optional
        Default False, it will plot the figure if set True
    '''

    plt.xlabel('Time')
    if unit == 'Kbps':
        plt.ylabel('Data Rate (Gbps)')
    elif unit == 'Mbps':
        plt.ylabel('Data Rate (Mbps)')
    elif unit == 'Gbps':
        plt.ylabel('Data Rate (Gbps)')
    else :
        plt.ylabel('Data Rate (Mbps)')

    plt.title((f'{title}\n{infile}').format(title = title, infile = infile))

    if xaxis == None:
        plt.plot(data, 'ro-')
    else:
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        if locator == 'second':
            plt.gca().xaxis.set_major_locator(mdates.SecondLocator())
        elif locator == 'minute':
            plt.gca().xaxis.set_major_locator(mdates.MinuteLocator())
        elif locator == 'hour':
            plt.gca().xaxis.set_major_locator(mdates.HourLocator())
        elif locator == 'day':
            plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        else:
            plt.gca().xaxis.set_major_locator(mdates.SecondLocator())
        plt.plot(xaxis, data, 'ro-')

    plt.gcf().autofmt_xdate()

    plt.savefig(outfile)
    if debug:
        plt.show()

def main(argv=None):

    if argv is None:
        argv = sys.argv

    # setup command line parser
    parser = argparse.ArgumentParser(
        description='Plot dstat logfile ')

    parser.add_argument(
        "--logfile",
        default='data/test.log',
        help="Filename with dstat logfile output")
    parser.add_argument(
        "--outfile",
        default=datetime.now().__format__('DstatTest-%Y%m%d%H%M%S.png'),
        help="Filename to save the plot (e.g.: dstattest-1.png)")
    parser.add_argument(
        "--locator",
        default='second',
        help="The locator in xaxis, can be second, minute, hour, day.")
    parser.add_argument(
        "--unit",
        default='Mbps',
        help="The unit of data rate , can be in [Gbps, Mbps, Kbps].")
    parser.add_argument(
        "--title",
        default='Dstat Test',
        help="Title using in the Figure (e.g.: Demo)")
    parser.add_argument("--debug",
                        help="Print debugging info",
                        action="store_true",
                        default=False)
    options = parser.parse_args()

    # configure logging
    config_logging(options.debug)

    unit = 'Mbps'
    if options.unit == 'Kbps':
        unit = 'Kbps'
    elif options.unit == 'Mbps':
        unit = 'Mbps'
    else:
        unit = 'Gbps'

    if os.path.isfile(options.logfile):
        infile =  options.logfile
        get_csv_data(infile)
        get_csv_header(infile)
        tt = get_csv_data(infile)
        recv_rate = []
        for i in tt:
            if i == '\n' :
                pass
            else:
                if unit == 'Gbps':
                    recv_rate.append(float(i.split(',')[10])*8/1024.0/1024/1024)
                elif unit == 'Mbps':
                    recv_rate.append(float(i.split(',')[10])*8/1024.0/1024)
                elif unit == 'Kbps':
                    recv_rate.append(float(i.split(',')[10])*8/1024.0)
                else:
                    recv_rate.append(float(i.split(',')[10])*8/1024.0/1024)

        timestamps = get_data_time(options.logfile)

        xs = [datetime.strptime(i, '%Y-%d-%m %H:%M:%S') for i in timestamps]

        print(xs)

        plot_dstat_recv_rate(recv_rate, xaxis=xs, title=options.title, infile=infile,locator=options.locator, unit=unit, outfile=options.outfile)
    else:
        print("Please specify a log file using dstat\n")
        print('or\n')
        print('Type `shao_plot_dstat --help` to get more informations')
        sys.exit(0)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
