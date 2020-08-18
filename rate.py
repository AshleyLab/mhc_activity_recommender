import argparse
import config 
from utils import *
from datetime import datetime

def parse_args(): 
    parser=argparse.ArgumentParser(description="rank an exercise activity -1,0,1")
    parser.add_argument("-user") 
    parser.add_argument("-activity_hash",type=str,default=None)
    parser.add_argument("-activity_category",choices=["lifestyle","training","videos","skip"])
    parser.add_argument("-rating",type=int, choices=[-1,0,1])
    parser.add_argument("-exertion",type=int,choices=range(6,21))
    parser.add_argument("-attempted",type=bool,choices=[True,False])
    parser.add_argument("--exertion_mismatch_thresh_to_adjust_fitness",type=int,default=2,help="if user's reported exertion differs from the expected exertion for the ativity by this much (or greater), adjust the user's fitness score")
    return parser.parse_args() 


def main(): 
    #read program arguments
    args=parse_args()
    
    #create mysql connection
    sql_db,sql_cursor =open_mysql_connection()
    cur_date=datetime.now()

    if args.activity_category=="skip":
        query="INSERT into activity_completion (user, date,  activity_category) values (%s, %s, %s);"
        vals=(args.user,  cur_date,  args.activity_category)
        sql_cursor.execute(query,vals)
    else:
        #update the activity_completion table to record this activity/user/date 
        query="INSERT into activity_completion (user, date, activity_hash, activity_category, rating, exertion, attempted) values (%s, %s, %s, %s, %s, %s, %s);"
        vals=(args.user,  cur_date, args.activity_hash, args.activity_category, args.rating, args.exertion, args.attempted)
        sql_cursor.execute(query,vals)

        #update the user's calculated fitness level if the reported exertion differs by thresh
        #get the current fitness score for the user 
        query="SELECT fitness_score from user_fitness where user=%s and date=(select max(date) from user_fitness where user=%s);"
        vals=(args.user,args.user)
        sql_cursor.execute(query,vals)
        fitness=sql_cursor.fetchall()
        if len(fitness)==0:
            fitness=config.default_fitness_score #default "average" fitness if non specified 
        else:
            fitness=int(fitness[0][0])
    
        #get the expected exertion values for this activity 
        query="SELECT target_exertion_min, target_exertion_max from activity_metadata where activity_hash=%s;"
        vals=(args.activity_hash,)
        sql_cursor.execute(query,vals)
        expected_exertion=sql_cursor.fetchall()[0]
        print(str(expected_exertion))
        min_expected_exertion=expected_exertion[0]
        max_expected_exertion=expected_exertion[1]


        #update the user's fitness score if needed (based on how exertion they report compares to expected exertion) 
        if (min_expected_exertion - args.exertion) > args.exertion_mismatch_thresh_to_adjust_fitness:
            #increase user's fitness score by 1
            if fitness < config.max_fitness_score:
                fitness+=1
        elif (args.exertion - max_expected_exertion) > args.exertion_mismatch_thresh_to_adjust_fitness:
            #decrease user's fitness score by 1    
            if fitness > config.min_fitness_score:
                fitness-=1

        #write new fitness score to database
        query="INSERT into user_fitness (user, date, fitness_score) VALUES (%s, %s, %s);"
        vals=(args.user, cur_date,fitness)
        sql_cursor.execute(query,vals)

        
    sql_db.commit()
    sql_cursor.close()
    sql_db.close()
        
if __name__=="__main__": 
    main() 

