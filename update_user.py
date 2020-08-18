'''
update user exercise preferences; if user not in database, insert them
'''
from datetime import datetime
import config
from utils import *
import argparse
import mysql.connector
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="updated user information")
    parser.add_argument("-user",help='unique user identifier')
    parser.add_argument("-user_pref_file",help="tab-separated file with columns Feature, Value, Importance")
    parser.add_argument("--user_fitness_level",type=int,choices=[1,2,3,4,5],default=None,help="fitness level 1 (lowest) - 5 (highest)")
    return parser.parse_args()

def generate_default_preferences(sql_cursor,user):
    #generate the default preference set for the user (these will be overwritten/updated by user's customized preference list where provided)
    features=open(config.modifiable_feature_file,'r').read().strip().split('\n')
    for feature in features:
        query="INSERT into user_preferences (user, feature, value, importance) VALUES (%s, %s, %s, %s);"
        vals=(user,feature,'NA',0)
        sql_cursor.execute(query,vals)
        
    

def update_user_preferences(sql_cursor,user,user_prefs):
    #if the user is not currently in the table, start with random feature preferences
    query="SELECT * from user_preferences where user=%s;";
    vals=(user,)
    sql_cursor.execute(query,vals)
    result=[i for i in sql_cursor.fetchall()]
    if len(result)==0:
        generate_default_preferences(sql_cursor,user)
        
    for index,row in user_prefs.iterrows():
        cur_feature=row['Feature']
        cur_feature_value=row['Value']
        cur_feature_importance=row['Importance']
        if str(cur_feature_importance)=="nan":
            cur_feature_importance=0
        #check to see if user/feature combination exists in user_preferences table; if it exists, update the feature value; if it does not exist, insert it into database
        query="SELECT * FROM user_preferences WHERE user=%s and feature=%s;"
        vals=(user,cur_feature)
        sql_cursor.execute(query,vals)
        result=[i for i in sql_cursor.fetchall()]
        if len(result)==0:
            #insert
            query="INSERT into user_preferences (user, feature, value, importance) VALUES (%s, %s, %s, %s);"
            vals=(user,cur_feature,str(cur_feature_value),cur_feature_importance)
        else:
             #update
            query="UPDATE user_preferences set value=%s, importance=%s WHERE user=%s AND feature=%s;"
            vals=(str(cur_feature_value), cur_feature_importance, user, cur_feature)
        print(str(vals))
        sql_cursor.execute(query,vals)
    print("updated user feature preferences") 
    return

        
def update_user_fitness(sql_cursor,user,user_fitness_level):
    query="INSERT into user_fitness (user, date, fitness_score) VALUES (%s, %s, %s);"
    vals=(user,datetime.now(),user_fitness_level)
    sql_cursor.execute(query,vals)
    print("updated user fitness")
    return


def main():
    args=parse_args()

    #connect to the db
    sql_db,sql_cursor=open_mysql_connection()

    #load the user feature preferences 
    user_prefs=pd.read_csv(args.user_pref_file,header=0,sep='\t')
    assert 'Feature' in user_prefs.columns
    assert 'Value' in user_prefs.columns
    assert 'Importance' in user_prefs.columns

    #update user feature preferences
    update_user_preferences(sql_cursor,args.user,user_prefs)

    #if fitness level is provided, update  it 
    if args.user_fitness_level is not None:
        update_user_fitness(sql_cursor,args.user,args.user_fitness_level)

    sql_db.commit()
    sql_db.close()
    sql_cursor.close()


if __name__=="__main__":
    main()
    
