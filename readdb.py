from flask import Flask, request
from flask_cors import CORS, cross_origin #Used to allow http requsets from other servers than the one this code runs on
import MySQLdb #Used to communicate with MySQL database
import time
import json #Used to format data to JSON format

app = Flask(__name__)
CORS(app)


@app.route('/area')
def byarea():
    db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("select events.county,(count(*)/counties.area) as e_per_a,count(*) as events,counties.pop,counties.area from events,counties where counties.name=events.county group by events.county order by e_per_a desc limit 20;")
    result=cursor.fetchall()
    y=[]
    for data in result:
        x=[]
        x.append(data[0].encode('utf-8'))
        x.append(str(data[1]))
        x.append(str(data[2]))
        x.append(str(data[3]))
        x.append(str(data[4]))
        y.append(x)
    return(json.dumps(y))


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1203)
