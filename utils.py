import mysql.connector

#cache mysql credentials here -- this is very bad and not secure, but nothing in the demo db is valuable
mysql_host='localhost'
mysql_user='root'
mysql_password='password'
mysql_db='mhc_rec'


#math of exercise category to activity metadata 
metadata={'lifestyle':'activities/lifestyle.tsv',
          'training':'activities/training.tsv',
          'video':'activities/ExerciseVideoLinks.tsv'}

def open_mysql_connection():
    #values imported from utils.py
    sql_db = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        passwd=mysql_password,
        database=mysql_db)
    
    sql_cursor = sql_db.cursor()
    return sql_db, sql_cursor
