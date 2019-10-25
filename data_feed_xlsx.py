import broker_util
import pandas as pd
import os

TYPE = 'battery'
USER = 1
USERID = 'bla'

file = './Messdaten.xlsx'

if TYPE is 'source':
    column = 'Energieproduktion [W]'
elif TYPE is 'battery':
    column = 'Batterie Sollwert [%]'
elif TYPE is 'user':
    if USER is 1:
        column = 'Energieverbrauch1 [W]'
    elif USER is 2:
        column = 'Energieverbrauch2 [W]'
    elif USER is 3:
        column = 'Energieverbrauch3 [W]'

dataframe = pd.read_excel(file)
dataframe = dataframe[0:96]
dataframe = dataframe[0:5]

for index, row in dataframe.iterrows():
    timestamp = row['Unnamed: 0']
    value = row[column]
    if TYPE is 'source':
        broker_util.send_offer(USERID, timestamp, value)
    elif TYPE is 'battery':
        broker_util.send_fill_level(USERID, timestamp, value)
    elif TYPE is 'user':
        broker_util.send_demand(USERID, timestamp, value)
