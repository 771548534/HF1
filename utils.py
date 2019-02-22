'''
测试工具类函数
'''

import matplotlib.pyplot as plt
import pandas as pd

def draw(file_path):
    df = pd.read_csv(file_path, header=0)['current']
    plt.plot(df)
    plt.show()