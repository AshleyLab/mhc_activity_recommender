'''
Script to create a mysql DB instance 
'''
import pdb
import config 
from utils import *
import argparse
import mysql.connector
import pandas as pd

    
def create_mysql_db(sql_cursor):
    #check if database exists 
    sql_cursor.execute("SHOW DATABASES;")
    result=[i for i in sql_cursor.fetchall()]
    print(str(result))
    if (mysql_db,) not in result:
        #the database does not exist, we create it
        sql_cursor.execute("CREATE DATABASE "+mysql_db)
    return 


    
def populate_lifestyle(sql_cursor,features):    
    lifestyle=pd.read_csv(metadata['lifestyle'],header=0,sep='\t')
    for index,row in lifestyle.iterrows():
        activity=row['Activity']
        for feature in features:
            if feature in row:
                cur_feature=feature
                cur_feature_val=row[feature] 
                activity_hash=create_activity_hash(activity)
                query="INSERT into activity_metadata (activity_hash, activity_name, activity_category, feature, feature_value) VALUES (%s, %s, %s, %s, %s);"
                vals=(activity_hash,activity,'lifestyle',cur_feature,str(cur_feature_val))
                sql_cursor.execute(query,vals) 
    print("populated lifestyle activity metadata table")
    
def populate_training(sql_cursor,features): 
    training=pd.read_csv(metadata['training'],header=0,sep='\t')
    disciplines=[str(i) for i in training['Discipline']]
    while 'nan' in disciplines:
        disciplines.remove('nan')
    for index,row in training.iterrows():
        feature_dict=row.to_dict() 
        for discipline in disciplines:
            activity=':'.join([str(i) for i in [discipline,feature_dict['Duration'],feature_dict['Intensity'],feature_dict['Description']]])
            activity_hash=create_activity_hash(activity)
            for feature in features:
                if feature in feature_dict:
                    cur_feature=feature
                    cur_feature_val=feature_dict[cur_feature]
                    query="INSERT into activity_metadata (activity_hash, activity_name, activity_category, feature, feature_value) VALUES (%s, %s, %s, %s, %s);"
                    vals=(activity_hash,activity,'training',cur_feature,str(cur_feature_val))
                    sql_cursor.execute(query,vals)
    print("populated training activity metadata table")

def populate_videos(sql_cursor,features):
    videos=pd.read_csv(metadata['video'],header=0,sep='\t')
    for index,row in videos.iterrows():
        activity=row['URL']
        activity_hash=create_activity_hash(activity)
        feature_dict=row.to_dict()
        for feature in features:
            if feature in feature_dict:
                cur_feature=feature
                cur_feature_val=feature_dict[feature]
                query="INSERT into activity_metadata (activity_hash, activity_name, activity_category, feature, feature_value) VALUES (%s, %s, %s, %s, %s);"
                vals=(activity_hash, activity, 'videos', cur_feature, str(cur_feature_val))
                sql_cursor.execute(query,vals)
    print("population videos activity metadata table")

def create_activity_metadata_table(sql_cursor):
    #remove existing table if it exists
    try:
        sql_cursor.execute("DROP TABLE activity_metadata;")
    except:
        pass 
    query="CREATE TABLE activity_metadata (activity_hash VARCHAR(255), activity_name VARCHAR(255), activity_category VARCHAR(255), feature VARCHAR(255), feature_value VARCHAR(255))"
    sql_cursor.execute(query) 

def populate_activity_metadata_table(sql_cursor):
    features=open(config.feature_file,'r').read().strip().split('\n')
    print("features:"+str(features))
    populate_lifestyle(sql_cursor,features)
    populate_training(sql_cursor,features)
    populate_videos(sql_cursor,features)

def create_user_preferences_table(sql_cursor):
    #remove existing table if it exists
    try:
        sql_cursor.execute("DROP TABLE user_preferences;")
    except:
        pass 

    query="CREATE TABLE user_preferences (activity_hash VARCHAR(255), activity_name VARCHAR(255), activity_category VARCHAR(255), feature VARCHAR(255), feature_value VARCHAR(255))"
    sql_cursor.execute(query)
    
def create_user_fitness_table(sql_cursor):
    #remove existing table if it exists
    try:
        sql_cursor.execute("DROP TABLE user_fitness;")
    except:
        pass 
    
    query="CREATE TABLE user_fitness (user VARCHAR(255), date DATE, fitness_score DOUBLE)"
    sql_cursor.execute(query) 

def create_activity_completion_table(sql_cursor):
    try:
        sql_cursor.execute("DROP TABLE activity_completion;")
    except:
        pass 
    query="CREATE TABLE activity_completion (user VARCHAR(255), date DATE, activity_hash DOUBLE, rating INT, exertion INT, Attempted BOOL)"
    sql_cursor.execute(query) 
    
def create_and_populate_tables():
                         
    #create database if it doesn't exist
    sql_db = mysql.connector.connect(
        host=config.mysql_host,
        user=config.mysql_user,
        passwd=config.mysql_password)
    
    sql_cursor = sql_db.cursor()
    print("mysql connection established")
    
    #create mysql db if it does not exist 
    create_mysql_db(sql_cursor)

    #connect to the db
    sql_db,sql_cursor=open_mysql_connection()
    
    #create and populate activity_metadata table
    create_activity_metadata_table(sql_cursor)
    populate_activity_metadata_table(sql_cursor)

    #create user_preference table
    create_user_preferences_table(sql_cursor)

    #create user_fitness table
    create_user_fitness_table(sql_cursor)

    #create activity_completion table
    create_activity_completion_table(sql_cursor)
    sql_db.commit()
    sql_db.close()
    sql_cursor.close()
    
    
def main():
    create_and_populate_tables()

    
if __name__=="__main__":
    main()
    
