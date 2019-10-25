import broker_util
import pandas as pd
import time

TYPE = 'user'
USER = 1
USERID = '30aa4c7f-faa4-4941-968f-3b024a5f1efe'

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

for index, row in dataframe.iterrows():
    timestamp = str(row['Unnamed: 0'])
    value = row[column]
    if TYPE is 'source':
        broker_util.send_offer(USERID, timestamp, value)
    elif TYPE is 'battery':
        broker_util.send_fill_level(USERID, timestamp, value)
    elif TYPE is 'user':
        broker_util.send_demand(USERID, timestamp, value)
    time.sleep(0.03)
