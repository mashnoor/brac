from flask import Flask, request
from brac import getPrediction
from dateutil import parser
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
    #now = datetime.datetime.now()
    now = parser.parse(str(time_H) + ":" + str(time_M))
    estimated_time = now + datetime.timedelta(seconds=estimated_second)
    estimated_hour = estimated_second/3600.0
    estimated_minute = estimated_hour - int(estimated_hour)
    estimated_minute = int(estimated_minute*60)
    msg = "Time Required (Apprx.) : " + str(int(estimated_hour)) + " hours and " + str(estimated_minute) + " minutes\n"
    
    msg += "You will reach there at " + str(estimated_time.hour) + ":" + str(estimated_time.minute)
    return msg

@app.route('/getplaces')
def getPlaces():
    f = open('places_sorted.txt')
    data = f.read()
    f.close()
    return data

@app.route('/feedback', methods=["POST"])
def feedback():
    fb = request.form.get('feedback')
    with open("feedbacks.txt", "a") as f:
        f.write(str(fb) + "\n")
    return "Thanks for your feedback"

@app.route('/contribute', methods=["POST"])
def contribute():
    start_place = request.form.get('start_place')
    stop_place = request.form.get('stop_place')
    time_start = request.form.get('time_start')
    duration = request.form.get('duration')
    vehicle = request.form.get('vehicle')
    weekday = request.form.get('weekday')
    string = str(start_place) + " " + str(stop_place) + " " + str(time_start) + " " + str(duration) + " " + str(vehicle) + " " + str(weekday)+"\n"
    with open("contribution.txt", "a") as f:
        f.write(string)
    return "Thanks for  you contribution!"

if __name__=="__main__":
    app.run(port=1234, host='0.0.0.0')
