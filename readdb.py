
import MySQLdb
import time
import json

db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
cursor = db.cursor()

cursor.execute("select events.county,(count(*)/counties.area) as e_per_a,count(*) as events,counties.pop,counties.area from events,counties where counties.name=events.county group by events.county order by e_per_a desc limit 20;")
userdatalist=cursor.fetchall()
for data in userdatalist:
    print (json.dumps(userdatalist))