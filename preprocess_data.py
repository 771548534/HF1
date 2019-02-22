'''
created time: 2019-2-14 10:54
function: 读取tick_data，并转化为data+label。因模型目标是不隔夜的高频数据，所以读取并转化数据时，以交易日为单位，
          不可跨交易日。目前，该功能仅限于处理单个品种。
'''
import pandas as pd
import numpy as np
import os


fee = 4  # 手续费，单位元
slip = 0  # 滑点，单位元


def file_list(path):
    '''
    :return: 列表，获取某一品种文件夹下所有文件名
    '''
    return os.listdir(path)


def handle_data(path, use='train', input_len=256, pre_len=20):
    '''
    读取列表中的文件，经处理后存储为data和label
    :param path: 文件夹路径
    :param use: 数据用途，'train'或'validation'
    :param input_len: 每个训练样本中，用于输入/训练的序列长度，也即在csv中采集的行数量
    :param pre_len: 用接下来pre—len个当前价格确定每个样本的label
    :output: 处理好的data和label文件，csv格式
    '''
    if os.path.exists(path):

        FILE_LIST = file_list(path)

        # 将样本reshape成一行的shape
        shape = (1, input_len * 8)
        temp_arr = np.zeros((shape[0], shape[1] + 1))
        for file in FILE_LIST:

            print('开始清洗', file)

            whole_data = pd.read_csv(path + '\\' + file, header=0)
            diff = whole_data['volume'].diff()
            whole_data.insert(5, 'diff', diff)
            whole_data.drop(['Unnamed: 0', 'time', 'volume', 'money', 'position'], axis=1, inplace=True)
            for i in range(len(whole_data) - input_len + 1):

                # 每次输入的序列，shape=(input_len, 8)
                single_data_df = whole_data.iloc[i: i + input_len]
                # 将df转化为数组并毁成shape(1, inputlen * 8)
                single_data_arr = single_data_df.values
                single_data_arr = single_data_arr.reshape(shape)

                # 输入序列最后一行的卖盘价和买盘价
                ask = single_data_df.iloc[-1]['a1_p']
                bid = single_data_df.iloc[-1]['b1_p']

                # 接下来pre_len条数据中，成交价格的最高价和最低价
                high = whole_data['current'].iloc[i + input_len: i + input_len + pre_len].max()
                low = whole_data['current'].iloc[i + input_len: i + input_len + pre_len].min()

                # 判定label为持平1、上涨2和下跌0，考虑手续费fee和滑点slip成本
                if high > ask + fee + slip:
                    single_label = 2
                elif low < bid - fee - slip:
                    single_label = 0
                else:
                    single_label = 1

                # 将label添加至single_data_arr最后面
                single_data_arr = np.append(single_data_arr, single_label)

                #将本条数据single_data_arr拼接至temp_arr
                temp_arr = np.vstack((temp_arr, single_data_arr))

            print(file, '清洗完成')

        if use == 'train':
            print('正在保存训练数据', 'D:\\Data\\train_data\\' + FILE_LIST[0][:2] + '.csv')
            np.savetxt('D:\\Data\\train_data\\' + FILE_LIST[0][:2] + '.csv',
                       temp_arr[1:], delimiter=',')
        else:
            print('正在保存验证数据', 'D:\\Data\\validation_data\\' + FILE_LIST[0][:2] + '.csv')
            np.savetxt('D:\\Data\\validation_data\\' + FILE_LIST[0][:2] + '.csv',
                       temp_arr[1:], delimiter=',')

        print('Job done!')
    else:
        print('老铁，请输入有效文件夹路径！')






