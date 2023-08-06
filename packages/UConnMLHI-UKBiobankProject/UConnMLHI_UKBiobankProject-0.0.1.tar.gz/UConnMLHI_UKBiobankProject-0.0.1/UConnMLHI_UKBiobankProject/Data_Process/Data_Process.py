__auther__ = 'Xinyu Wang'

import numpy as np
import pandas as pd

# Import Utilities
from ..Utilities.Utilities import *




def dta2csv(file_path,return_df=False):
    print_time('[dta2csv] Starts.')

    # Load dta file this will take a long time on diagnosis data
    df = read_file(file_path)
    if df is not None:
        print_time('[dta2csv] Data loaded.')
    else:
        print_time('[dta2csv] No data loaded, ends.')
        return
    # Changes extension from .dta to .csv
    file_name = '.'.join(file_path.split('/')[-1].split('.')[:-1]+['csv'])
    file_path = '/'.join(file_path.split('/')[:-1]+[file_name])
    df.to_csv(file_path)
    print_time('[dta2csv] Saved to csv.')

    # Returns df if return_df = True
    if return_df:
        print_time('[dta2csv] Returns DataFrame.')
        return df
    else:
        return

def remove_missing_entries(df):
    # Get # of missing entries in each row
    missing_in_each_row = []

    for i in range(m):
            sum_str = 0
            if isinstance(f.loc[i][0], str):
                    sum_str = sum(f[ch] == '')

            missing_in_each_row.append(sum_str + sum(pd.isnull(f.loc[i])))

    print('start filter row')
    print(missing_in_each_row[:1000])
    filter_list = pd.DataFrame({'missing_in_each_row':missing_in_each_row})
    f = f[filter_list['missing_in_each_row'] < n/2]

    m,n = f.shape
    print(f.shape)

    headers = list(f)

    # Get # of missing entries in each column
    missing_in_each_column = []
    for i in range(n):
            current_header = headers[i]
            ch = current_header
            # ch = 'n_25920_2_0'
            # counter_sum = 0
            sum_str = 0
            if isinstance(f[ch][0], str):
                    sum_str = sum(f[ch] == '')
            missing_in_each_column.append(sum_str + sum(pd.isnull(f[ch])))
            # print('current:',i,'/',n, temp)

    f = f.T

    print('start filter column')
    print(missing_in_each_column)
    filter_list = pd.DataFrame({'missing_in_each_column':missing_in_each_column})
    # print(filter_list.shape)

    f = f[(filter_list < m/2)['missing_in_each_column'].values.tolist()]
    f = f.T

    return

def select_healthy_subject(self):
    pass

def ICD_parser(file_path,keywords=[],nodes=[]):
    # ['drug', 'alcohol', 'opiate', 'cocaine', 'hallucinogen', 'steroid']
    # df = pd.read_csv('/home/xinyu/src/mih/coding19.tsv',sep='\t',index_col=0)
    # Init variables
    column_description = 'meaning'
    column_coding = 'coding'
    column_node = 'node_id'
    column_parent_node = 'parent_id'
    # keywords_dict is used to store the keyword
    keywords_dict = {}
    keywords_statistics = {}
    keywords_cumulative = pd.Series()

    # nodes_dict is used to store the nodes
    nodes_dict = {}
    nodes_statistics = {}
    nodes_cumulative = pd.Series()

    # Read file
    df = pd.read_file(file_path)

    # For each keyword, find the nodes (and their childrens) which relates to it.
    for keyword in keywords:
        nodes_current = df[df[column_description].str.contains(keyword,case=False)][column_node]
        while True:
            nodes_new = pd.concat([nodes_current,df[df[column_parent_node].isin(nodes_current)][column_node]]).drop_duplicates()
            if nodes_current.shape[0] == nodes_new.shape[0]:
                break
            else:
                nodes_current = nodes_new
        keywords_dict [keyword] = nodes_new
        keywords_statistics[keyword] = nodes_new.shape[0]
        keywords_cumulative = pd.concat([keywords_cumulative,nodes_new]).drop_duplicates()

    for node in nodes:
        nodes_current = df[df[column_node].isin([node])][column_node]
        while True:
            nodes_new = pd.concat([nodes_current,df[df[column_parent_node].isin(nodes_current)][column_node]]).drop_duplicates()
            if nodes_current.shape[0] == nodes_new.shape[0]:
                break
            else:
                nodes_current = nodes_new
        nodes_dict [keyword] = nodes_new
        nodes_statistics[keyword] = nodes_new.shape[0]
        nodes_cumulative = pd.concat([nodes_cumulative,nodes_new]).drop_duplicates()

    return pd.concat([keywords_cumulative,nodes_cumulative]).drop_duplicates()
