# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 14:04:53 2019
function: download future_tick_data form JointQuant
@author: Administrator
"""
import pandas as pd
from jqdata import *
import os

pinzhong_list = ['A', 'B', 'BB', 'C', 'CS', 'FB', 'I', 'J', 'EG', 'JD', 'JM', 'L', 
                 'M', 'P', 'PP', 'V', 'Y', 'CY', 'CF', 'RS', 'SF', 'SM', 'SR', 'TA', 
                 'WH', 'ZC', 'AP', 'RM', 'FG', 'JR', 'LR', 'MA', 'OI', 'PM', 'RI', 
                 'AG', 'AU', 'AL', 'BU', 'CU', 'FU', 'HC', 'SP','PB', 'RB', 'RU', 
                 'SN', 'WR', 'ZN', 'NI', 'SC', 'IC', 'IF', 'IH', 'T', 'TF']#品种列表

#获取交易日list，最早起始日为2010-1-1
def trading_days(start_date='2010-1-1', end_date=None, count=None):
    temp_dates = get_trade_days(start_date, end_date, count)
    dates = []
    for temp_d in temp_dates:
        d = temp_d.__format__('%Y-%m-%d')
        dates.append(d)
    return dates


#获取某一品种、某一日期对应的主力合约
def contract(pinzhong, date):
    return get_dominant_future(underlying_symbol=pinzhong, date=date)


#获取某一品种在某区间的tick数据，每个交易日输出一个csv
def download_one_contract(pinzhong, start_date='2010-1-1', end_date=None, count=None):
    dates = trading_days(start_date, end_date=None, count=None)
    fold = 'D:\\tick_data\\' + pinzhong + '\\'
    if os.path.exists(fold):
        pass
    else:
        os.mkdir(fold)
    try:
        for i in range(len(dates)):
            heyue = contract(pinzhong, dates[i])
            temp_dir = fold + heyue[:-5] + '_' + dates[i] + '.csv'
            if os.path.exists(temp_dir):
                pass
            else:
                ticks = get_ticks(security=heyue, start_dt=dates[i], end_dt=dates[i+1], count=None, 
                                  fields=['time','current','high','low','volume','money','position',
                                          'a1_v','a1_p','b1_v','b1_p'])
                ticks = pd.DataFrame(ticks)
                ticks.to_csv(temp_dir)
    except IndexError:
        print(heyue[:-5] + '下载完毕')


#批量获取品种列表中，所有品种在某区间的tick数据，每个品种每个交易日输出一个csv
def dowmload_all_contracts(pinzhong_list, start_date='2010-1-1', end_date=None, count=None):
    for p in pinzhong_list:
        download_one_contract(p, start_date, end_date=None, count=None)
    print('整完了，老铁')
