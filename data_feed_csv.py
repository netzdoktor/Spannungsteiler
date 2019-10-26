from spannungsteiler.util.broker_util import send_demand
import pandas as pd
from datetime import time
from time import sleep
import sys

if len(sys.argv) != 3:
    raise Exception('Give USERID and PROFILE parameters')

USERID = sys.argv[1]
PROFILE = int(sys.argv[2])

if PROFILE == 1:
    dataframe = pd.read_csv("data/MisterX.csv", sep=",")
elif PROFILE == 2:
    dataframe = pd.read_csv("data/Rentner.csv", sep=",")
elif PROFILE == 3:
    dataframe = pd.read_csv("data/Student.csv", sep=",")
else:
    raise Exception("Give valid PROFILE")

for index, row in dataframe.iterrows():

    time_list = []
    time_list.append(row[0])
    time_list.append(row[1])

    time_stamp = time(time_list[0], time_list[1])

    send_demand(USERID, timestamp, row[2])
    sleep(0.3)
