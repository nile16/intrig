import feedparser
import MySQLdb
import time


#The table 'events' must be created before running this script. 
#    CREATE TABLE `events` ( `time` int(11), `title` varchar(256), `summary` varchar(512), `city` varchar(64), `link` varchar(256))
#        ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_swedish_ci;
db = MySQLdb.connect(host="localhost", user='root', passwd='apa', db='police', use_unicode=True, charset="utf8")
cursor = db.cursor()

#Parse RSS feeds into variables in the form of dicts. Every dict has a key 'entries' which value is a list. 
#The list items represent police statements in the form of dicts. These statements dicts have keys like 'title' and 'link' 
police_rss    = feedparser.parse('https://polisen.se/Aktuellt/Handelser/Handelser-i-hela-landet/?feed=rss')


#Loop through the lists of events and add the titles not already in the database. 
#Escape character ' in the titles to prevent the SQL commands from breaking.
for item in police_rss['entries']:
    county=item['title'][item['title'].rfind(',')+2:]
    cursor.execute("SELECT * FROM events WHERE title='"+item['title'].replace("'", r"\'")+"';")
    if (len(cursor.fetchall())==0):
        cursor.execute("INSERT INTO events (time,title,summary,county,link)  VALUES ('"+str(int(time.mktime(item['published_parsed'])))+"','"+item['title'].replace("'", r"\'")+"','"+item['summary']+"','"+county+"','"+item['link']+"')")

#Delete all items older than one year from reasent table 
cursor.execute("DELETE FROM events WHERE time<"+str(time.time()-31536000))

db.commit()

db.close()
