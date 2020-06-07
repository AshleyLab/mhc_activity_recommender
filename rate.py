import argparse
from utils import *
from datetime import datetime

def parse_args(): 
    parser=argparse.ArgumentParser(description="rank an exercise activity -1,0,1")
    parser.add_argument("--user") 
    parser.add_argument("--date")
    parser.add_argument("--activity_category",choices=['lifestyle','training','video','skip'])
    parser.add_argument("--activity",type=str)
    parser.add_argument("--rating",type=int, choices=[-1,0,1])
    parser.add_argument("--exertion",type=int,choices=range(6,21))
    parser.add_argument("--attempted",type=bool,choices=[True,False])
    return parser.parse_args() 


def main(): 
    #read program arguments
    args=parse_args()
    
    #create mysql connection
    sql_db,sql_cursor =open_mysql_connection()
    cur_date=datetime.strptime(args.date, '%Y-%m-%d %H:%M:%S')

    #hash the activity
    activity_hash=create_activity_hash(args.activity)

    #update the activity rating and exertion score
    sql="UPDATE activities set rating = %s, exertion = %s WHERE user = %s AND date = %s AND activity_hash = %s "
    vals=(args.rating, args.exertion, args.user, cur_date, activity_hash)
    sql_cursor.execute(sql,vals)
    sql_db.commit()

    #update the user's calculated fitness level
    

    check_sql="SELECT * from activities WHERE user = %s AND date = %s AND activity_category = %s"
    check_vals=(args.user,cur_date, args.activity_category)
    sql_cursor.execute(check_sql,check_vals)
    result=sql_cursor.fetchall()
    for output in result:
        print(output)
    sql_cursor.close()
    sql_db.close()
        
if __name__=="__main__": 
    main() 

