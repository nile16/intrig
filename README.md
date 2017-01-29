# intrig

readrss.py reads the police's RSS feed and stores the data in a MySQL database. readrss is run as a cron job on top of every hour.

readdb.py is a flask application that listen to port 1203 and executes select commands in the MySQL database and returns the result as JSON.
