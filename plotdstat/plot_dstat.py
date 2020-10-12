#!/usr/bin/env python3

'''
This file will plot the data rate extract from iperf3 JSON file
'''

import os
import logging
import numpy as np
import matplotlib.pyplot as plt
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


def plot_dstat_recv_rate(
        data,
        infile='',
        title = 'Network Rate',
        outfile=datetime.now().__format__('NetworkTest-%Y%m%d%H%M%S.png'),
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

    plt.xlabel('Time (s)')
    plt.ylabel('Data Rate (Gbps)')
    plt.title((f'{title}\n{infile}').format(title = title, infile = infile))
    plt.plot(data, 'ro-')
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
                recv_rate.append(float(i.split(',')[10])*8/1024.0/1024/1024)

        plot_dstat_recv_rate(recv_rate, infile=infile, outfile=options.outfile)
    else:
        print("Please specify a log file using dstat")
        sys.exit(0)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
