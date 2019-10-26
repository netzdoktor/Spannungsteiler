from broker_util import send_demand
import pandas as pd
from datetime import time
from time import sleep


USERID = '30aa4c7f-faa4-4941-968f-3b024a5f1efe'

dataframe = pd.read_csv("data/Rentner.csv", sep=",")

for index, row in dataframe.iterrows():

    time_list = []
    time_list.append(row[0])
    time_list.append(row[1])

    time_stamp = time(time_list[0], time_list[1])
    
    send_demand(USERID, timestamp, row[2])
    sleep(0.3)