#### I.- EXTRACCIÓN
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta as td
pd.set_option('display.max_columns',500)

df = pd.read_csv('../ETL/Reservations_Work.csv')

###### DEJARLO COMO EL LAYOUT #################
area = 'Nuevo Vallarta'
sitegroup = 'The Grand Mayan'
roomtype = 'Grand Mayan Suite'
mix = 'IN'
season = ['Season Int' if mix == 'IN' else 'Temp Nal' for i in range(1)][0]

df = df[(df['Area'] == area) & \
    (df['SiteGroup'] == sitegroup) & \
    (df['RoomType'] == roomtype) & \
    (df['Mix_NA_IN'] == mix)].reset_index(drop = True)

df['FirstNight'] = pd.to_datetime(df['FirstNight'],format = '%d/%m/%Y')
df['Year'] = [d.year for d in df['FirstNight']]
df['Weekday'] = [d.isoweekday() - 4 if d.isoweekday() >= 5 else \
                 d.isoweekday() + 3 for d in df['FirstNight']]

ls_cols = ['FirstNight',season,'Reservations',
           'Semana_Myn','Weekday','Year']
df = df[ls_cols]
# print(df.shape)
# print(df.head())
################ ESTO SE BORRA #########################

### II.- DESTEMPORALIZACIÓN ###########
# A) CARDINALIDAD

## EN __INNIT__ AGREGAR CUALES FECHAS TE FALTAN EN EL ETL
pivotDate = '01/01/2018' #<------------------------ __INNIT__
pivotDate = datetime.datetime.strptime(pivotDate,'%d/%m/%Y')

trainingDates = pd.date_range(start = datetime.datetime(pivotDate.year-1,
                                                      pivotDate.month,
                                                      pivotDate.day),
                            end =   datetime.datetime(pivotDate.year,
                                                      pivotDate.month,
                                                      pivotDate.day)+td(days=-1))
df_card = pd.DataFrame(trainingDates,columns = ['FirstNight'])
df_card['Card'] = 1
df = df.merge(df_card, on = ['FirstNight'], how = 'left')

df_card = df[df['Card'] == 1].groupby([season], 
                                      as_index = False)[['Reservations']].count()

print(trainingDates)
print(df_card['Reservations'].sum())
print(df[df['Card'] == 1].shape)









# exit()

# print(df[df['FirstNight'] == pivotDate])
# trainingYear = np.unique(df['Year'])[1]

# print(trainingYear)
# print(min(df['FirstNight']))
# print(max(df['FirstNight']))


