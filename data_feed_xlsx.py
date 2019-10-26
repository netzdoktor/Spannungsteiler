import broker_util
import pandas as pd
import time

TYPE = 'user'
USER = 1
USERID = '30aa4c7f-faa4-4941-968f-3b024a5f1efe'

file = './Messdaten.xlsx'

if USER is 1:
    column = 'Energieverbrauch1 [W]'
elif USER is 2:
    column = 'Energieverbrauch2 [W]'
elif USER is 3:
    column = 'Energieverbrauch3 [W]'

dataframe = pd.read_excel(file)
dataframe = dataframe[0:96]

for index, row in dataframe.iterrows():
    timestamp = str(row['Unnamed: 0'])
    broker_util.send_offer(USERID, timestamp, row["Energieproduktion [W]"])
    broker_util.send_fill_level(USERID, timestamp, row["Batterie Sollwert [%]"])
    broker_util.send_demand(USERID, timestamp, row[column])
    time.sleep(0.3)
