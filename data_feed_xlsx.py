import broker_util
import pandas as pd
import time
import sys

if len(sys.argv) != 3:
    raise Exception('Give USERID and PROFILE parameters')
USERID = sys.argv[1]
PROFILE = int(sys.argv[2])

file = './data/Messdaten.xlsx'

if PROFILE is 1:
    column = 'Energieverbrauch1 [W]'
elif PROFILE is 2:
    column = 'Energieverbrauch2 [W]'
elif PROFILE is 3:
    column = 'Energieverbrauch3 [W]'
else:
    raise Exception(str(PROFILE) + ' is not a valid profile.')

dataframe = pd.read_excel(file)
dataframe = dataframe[0:96]

for index, row in dataframe.iterrows():
    timestamp = str(row['Unnamed: 0'])
    broker_util.send_offer(USERID, timestamp, row["Energieproduktion [W]"])
    broker_util.send_fill_level(USERID, timestamp, row["Batterie Sollwert [%]"])
    broker_util.send_demand(USERID, timestamp, row[column])
    time.sleep(1)
