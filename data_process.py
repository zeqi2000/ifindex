import pandas as pd
import csv
import numpy as np

def load_dataset(datapath = "data/simple_acci_point.csv"):
    data = pd.read_csv(datapath)
    data = data.dropna(subset = ['Longitude','Latitude'] )

    # print(len(data))
    return data

def norm_sub(aa:list):
    data = np.array(aa)
    n = len(data)
    positive_num = (data >= 0).sum()
    while (positive_num != n) :
        total = sum(data)
        diff = total - sum(data[data > 0])  # 该值一般为负

        for i, item in enumerate(data):
            if item > 0:
                data[i] = item + diff / positive_num
            else:
                data[i] = 0
        # print(data)
        positive_num = (data >= 0).sum()

    return data.tolist()