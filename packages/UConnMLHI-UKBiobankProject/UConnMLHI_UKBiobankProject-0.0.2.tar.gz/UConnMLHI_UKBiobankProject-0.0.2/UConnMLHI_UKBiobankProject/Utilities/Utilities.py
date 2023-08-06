__author__ = 'Xinyu Wang'

import os
import sys
import time
import datetime
import numpy as np
import pandas as pd
def print_time(*args):

    print(str(datetime.datetime.now())[:-7],*args)
    return

def read_file(file_path,low_memory=False,index_col=0,special_extension=False):
    if os.path.isfile(file_path):
        if file_path.split('.')[-1] ==  'dta':
            print_time('[read file] Find dta file')
            df = pd.read_stata(file_path)
        elif file_path.split('.')[-1] ==  'tsv':
            print_time('[read file] Find tsv file')
            df = pd.read_csv(file_path, sep='\t', index_col=index_col, low_memory=low_memory)
            # print(df)
        elif file_path.split('.')[-1] == 'csv':
            print_time('[read file] Find csv file')
            df = pd.read_csv(file_path, index_col=index_col, low_memory=low_memory)
        elif special_extension:
            return
        else:
            return
        return df
    else:
        print_time('[read file] File not exists.')
        return
