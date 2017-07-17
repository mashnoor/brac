from flask import Flask, request
from brac import getPrediction

import datetime


app = Flask(__name__)

@app.route('/gettime', methods = ['POST'])
def gettime():
    start = request.form.get('start')
    stop = request.form.get('stop')
    time_H = request.form.get('time_h')
    time_M = request.form.get('time_m')
    weekday = request.form.get('weekday')
    vehicle = request.form.get('vehicle')
    estimated_second = float(getPrediction(start, stop, time_H, time_M, weekday, vehicle))
    now = datetime.datetime.now()
    estimated_time = now + datetime.timedelta(seconds=estimated_second)
    estimated_hour = estimated_second/3600.0
    msg = "Time Required (Apprx.) : " + str(estimated_hour) + " hours\n"
    
    msg += "You will reach there at " + str(estimated_time.hour) + ":" + str(estimated_time.minute)
    return msg

@app.route('/getplaces')
def getPlaces():
    f = open('places_sorted.txt')
    data = f.read()
    f.close()
    return data

if __name__=="__main__":
    app.run(port=1234)