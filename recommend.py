import argparse
import mysql.connector
from utils import * 
from datetime import datetime

def parse_args(): 
    parser=argparse.ArgumentParser(description="recommend activity") 
    parser.add_argument("--user") 
    parser.add_argument("--date",default=None,help="format:2020-03-07 15:17:00") 
    parser.add_argument("--activity_selection",choices=["lifestyle","training","video","skip"]) 
    parser.add_argument("--feature_ranks",default=None, help="tsv file with feature name in column 1 and rank 1 to 10 in column 2")
    parser.add_argument("--outf",default=None,help="if None, print to console, else write string of recommended activities to a file")
    return parser.parse_args() 

def open_mysql_connection():
    #values imported from utils.py
    sql_db = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        passwd=mysql_password,
        database=mysql_db)
    
    sql_cursor = sql_db.cursor()
    return sql_db, sql_cursor

def make_output(activity,sql_cursor,sql_db,args):
    '''
    populate database with activity selection string 
    return activity selection string 
    '''
    #write activity entry to db
    sql="INSERT INTO activities (user, date, activity) VALUES (%s, %s, %s)"
    if args.date is None:
        cur_datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        cur_datetime=args.date
        
    vals=[args.user,cur_datetime, activity]
    sql_cursor.execute(sql,vals)
    sql_db.commit() 
    
    if args.outf is None:
        print(str(activity))
    else:
        outf=open(args.outf,'w')
        outf.write(activity)
        outf.close()
       
def main():
    #read program arguments
    args=parse_args()
    
    #create mysql connection
    sql_db,sql_cursor =open_mysql_connection()

    if args.activity_selection=="skip":
        #user selected to skip exercise
        make_output('skip',sql_cursor,sql_db, args)
    else:
        #recommend an exercise
        recommendation=get_recommendation(sql_cursor,sql_db,args)
        make_output(recommendation,sql_cursor,sqld_db, args)

    #close mysql connection
    sql_db.close()
    
    
    
    
if __name__=="__main__": 
    main() 
