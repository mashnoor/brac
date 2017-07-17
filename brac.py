#Thesis Project

from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import json
from datetime import timedelta
from sklearn.metrics import mean_squared_error
import math

df = pd.read_excel('all_data.xlsx')
places = json.loads(open('places_sorted.txt').read())
'''
Sort the all places
places = open('places.txt').read().replace('\r', '').split("\n")
places.sort()
with open('places_sorted.txt', 'w+') as f:
    f.write(json.dumps(places))
print places
'''
place_mapping = {}
total_places = len(places)


vehicle_mapping = {'Car' : 0.0, 'Bus' : 1.0}
weekday_mapping = {'Saturday' : 0., 'Sunday' : 1., 'Monday' : 2., 'Tuesday' : 3., 'Wednesday' : 4., 'Thursday' : 5., 'Friday' : 6.}
for i in range(0, total_places):
    place_mapping[places[i]] = float(i)


#df['Start_Pos'] = df['Start_Pos'].str.strip().map(place_mapping)
#df['Stop_Pos'] = df['Stop_Pos'].str.strip().map(place_mapping)
#df['Weekday'] = df['Weekday'].str.strip().map(weekday_mapping)
train_X = []
train_Y = []

for index, row in df.iterrows():
    try:
        curr_x = []
        start_pos = place_mapping[str(row['Start_Pos']).strip()]
        stop_pos = place_mapping[str(row['Stop_Pos']).strip()]
        weekday = weekday_mapping[str(row['Weekday']).strip()]
        vehicle = vehicle_mapping[str(row['Vehicle']).strip()]
        start_t_h = float(str(row['Start_T']).strip().split(':')[0])
        start_t_m = float(str(row['Start_T']).strip().split(':')[1])
        stop_t_h = float(str(row['Stop_T']).strip().split(':')[0])
        stop_t_m = float(str(row['Stop_T']).strip().split(':')[1])
        t1 = timedelta(hours=stop_t_h, minutes=stop_t_m)
        t2 = timedelta(hours=start_t_h, minutes=start_t_m)
        duration = (t1-t2).seconds


        curr_x.append(start_pos)
        curr_x.append(stop_pos)
        curr_x.append(weekday)
        curr_x.append(vehicle)
        curr_x.append(start_t_h)
        curr_x.append(start_t_m)
        train_X.append(curr_x)
        train_Y.append(duration)
    except Exception as e:
        pass




#clf = MLPRegressor(activation='logistic', solver='sgd', max_iter=500000, hidden_layer_sizes=(50, 50, 50, 50, 50), verbose=True)
clf = KNeighborsRegressor()
clf.fit(train_X, train_Y)


def getPrediction(start, stop, time_h, time_m, weekday, vehicle):
    start_idx = place_mapping[start]
    stop_idx = place_mapping[stop]
    weekday_idx = weekday_mapping[weekday]
    vehicle_idx = vehicle_mapping[vehicle]

    x = []
    x.append(start_idx)
    x.append(stop_idx)
    x.append(weekday_idx)
    x.append(vehicle_idx)
    x.append(float(time_h))
    x.append(float(time_m))

    return str(clf.predict([x])[0])




#Machine Learning Part

'''
Input Things
1. Start_Pos
2. Stop_Pos
3. Start_H
4. Strat_M
5. Week Day

Output
Time
'''
