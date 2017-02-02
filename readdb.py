from flask import Flask, request
from flask_cors import CORS #Used to allow http requsets from other servers than the one this code runs on
import MySQLdb #Used to communicate with MySQL database
import json #Used to format data to JSON format

app = Flask(__name__)
CORS(app)


@app.route('/total')
def total():
    db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("select events.county,count(*) as events,(count(*)/counties.area) as e_per_a,(count(*)/counties.pop)*10000 as e_per_p,counties.pop,counties.area from events,counties where counties.name=events.county group by events.county order by events desc limit 20;")
    result=cursor.fetchall()
    y=[]
    for data in result:
        x=[]
        x.append(data[0].encode('utf-8')) #County
        x.append(str(data[1]))            #e
        x.append(str(data[2]))            #e/a
        x.append(str(data[3]))            #e/p
        x.append(str(data[4]))            #pop
        x.append(str(data[5]))            #area
        y.append(x)
    return(json.dumps(y))

@app.route('/area')
def area():
    db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("select events.county,count(*) as events,(count(*)/counties.area) as e_per_a,(count(*)/counties.pop)*10000 as e_per_p,counties.pop,counties.area from events,counties where counties.name=events.county group by events.county order by e_per_a desc limit 20;")
    result=cursor.fetchall()
    y=[]
    for data in result:
        x=[]
        x.append(data[0].encode('utf-8')) #County
        x.append(str(data[1]))            #e
        x.append(str(data[2]))            #e/a
        x.append(str(data[3]))            #e/p
        x.append(str(data[4]))            #pop
        x.append(str(data[5]))            #area
        y.append(x)
    return(json.dumps(y))

@app.route('/pop')
def pop():
    db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute("select events.county,count(*) as events,(count(*)/counties.area) as e_per_a,(count(*)/counties.pop)*1000 as e_per_p,counties.pop,counties.area from events,counties where counties.name=events.county group by events.county order by e_per_p desc limit 20;")
    result=cursor.fetchall()
    y=[]
    for data in result:
        x=[]
        x.append(data[0].encode('utf-8')) #County
        x.append(str(data[1]))            #e
        x.append(str(data[2]))            #e/a
        x.append(str(data[3]))            #e/p
        x.append(str(data[4]))            #pop
        x.append(str(data[5]))            #area
        y.append(x)
    return(json.dumps(y))


@app.route('/search',methods = ['POST'])
def search():
    received_data=request.get_data()
    words=received_data.split()
    query="SELECT * FROM events WHERE "
    if len(words)==1:
        query+="title LIKE '%"+words[0]+"%'"
    else:
        query+="( "
        for y in range(len(words)):
            query+="( title LIKE '%"+words[y]+"%' OR summary LIKE '%"+words[y]+"%') "
            if y!=len(words)-1:
                query+=" AND "
        query+=" )"
    query+=" ORDER BY time DESC LIMIT 10"
    #print(query)
    db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
    cursor = db.cursor()
    cursor.execute(query)
    result=cursor.fetchall()
    y=[]
    for data in result:
        x=[]
        x.append(data[0])                 #Unix time stamp
        x.append(data[1].encode('utf-8')) #Title
        x.append(data[2].encode('utf-8')) #Summary
        x.append(data[3].encode('utf-8')) #County
        x.append(data[4].encode('utf-8')) #Link
        y.append(x)
    return(json.dumps(y))
	
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1203)
