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
    
def populate_lifestyle(sql_cursor,modifiable_features):    
    lifestyle=pd.read_csv(metadata['lifestyle'],header=0,sep='\t')

    #Update activity_metadata table 
    for index,row in lifestyle.iterrows():
        activity=row['Activity']
        activity_hash=create_activity_hash(activity)
        query="INSERT into activity_metadata (activity_hash, activity_name, activity_category, min_fitness_level, max_fitness_level, target_exertion_min, target_exertion_max) values (%s, %s, %s, %s, %s, %s, %s);"
        vals=(activity_hash,
              activity,
              'lifestyle',
              row['min_fitness_level'],
              row['max_fitness_level'],
              row['target_exertion_min'],
              row['target_exertion_max'])
        sql_cursor.execute(query,vals)

        #Update activity_features table 
        for feature in modifiable_features:
            if feature in row:
                cur_feature=feature
                cur_feature_val=str(row[feature])
                query="INSERT into activity_features (activity_hash, feature, feature_value) VALUES ( %s, %s, %s);"
                vals=(activity_hash,cur_feature,str(cur_feature_val))
                sql_cursor.execute(query,vals)
    print("populated lifestyle activity metadata table")
    
def populate_training(sql_cursor,modifiable_features): 
    training=pd.read_csv(metadata['training'],header=0,sep='\t')
    disciplines=[str(i) for i in training['Discipline']]
    while 'nan' in disciplines:
        disciplines.remove('nan')
    for index,row in training.iterrows():
        for discipline in disciplines:
            activity=':'.join([str(i) for i in [discipline,row['Duration'],row['Intensity'],row['Description']]])
            activity_hash=create_activity_hash(activity)
            query="INSERT into activity_metadata (activity_hash, activity_name, activity_category, min_fitness_level, max_fitness_level, target_exertion_min, target_exertion_max) values (%s, %s, %s, %s, %s, %s, %s);"
            vals=(activity_hash,
                  activity,
                  'training',
                  row['min_fitness_level'],
                  row['max_fitness_level'],
                  row['target_exertion_min'],
                  row['target_exertion_max'])
            sql_cursor.execute(query,vals)

            for feature in modifiable_features:
                if feature in row: 
                    cur_feature=feature
                    cur_feature_val=str(row[cur_feature])
                    query="INSERT into activity_features (activity_hash, feature, feature_value) VALUES (%s, %s, %s);"
                    vals=(activity_hash, cur_feature, cur_feature_val)
                    sql_cursor.execute(query,vals)                    
    print("populated training activity metadata table")

def populate_videos(sql_cursor,modifiable_features):
    videos=pd.read_csv(metadata['video'],header=0,sep='\t')
    for index,row in videos.iterrows():
        activity=row['URL']
        activity_hash=create_activity_hash(activity)
        query="INSERT into activity_metadata (activity_hash, activity_name, activity_category, min_fitness_level, max_fitness_level, target_exertion_min, target_exertion_max) values (%s, %s, %s, %s, %s, %s, %s);"
        vals=(activity_hash,
              activity,
              'videos',
              row['min_fitness_level'],
              row['max_fitness_level'],
              row['target_exertion_min'],
              row['target_exertion_max'])
        sql_cursor.execute(query,vals)
        for feature in modifiable_features:
            if feature in row:
                cur_feature=feature
                cur_feature_val=str(row[cur_feature])                
                query="INSERT into activity_features (activity_hash, feature, feature_value ) VALUES (%s, %s, %s);"
                vals=(activity_hash,cur_feature,cur_feature_val)
                sql_cursor.execute(query,vals)
    print("population videos activity metadata table")

def populate_activity_tables(sql_cursor):
    modifiable_features=open(config.modifiable_feature_file,'r').read().strip().split('\n')
    populate_lifestyle(sql_cursor,modifiable_features)
    populate_training(sql_cursor,modifiable_features)
    populate_videos(sql_cursor,modifiable_features)

    
def create_activity_metadata_table(sql_cursor):
    #remove existing table if it exists
    try:
        sql_cursor.execute("DROP TABLE activity_metadata;")
    except:
        pass 
    query="CREATE TABLE activity_metadata (activity_hash VARCHAR(255), activity_name VARCHAR(255), activity_category VARCHAR(255), min_fitness_level INT, max_fitness_level INT, target_exertion_min INT, target_exertion_max INT)"
    sql_cursor.execute(query) 

def create_activity_feature_table(sql_cursor):
    #remove existing table if it exists
    try:
        sql_cursor.execute("DROP TABLE activity_features;")
    except:
        pass 
    query="CREATE TABLE activity_features (activity_hash VARCHAR(255), feature VARCHAR(255), feature_value VARCHAR(255))"
    sql_cursor.execute(query) 

    
def create_user_preferences_table(sql_cursor):
    #remove existing table if it exists
    try:
        sql_cursor.execute("DROP TABLE user_preferences;")
    except:
        pass 

    query="CREATE TABLE user_preferences (user VARCHAR(255), feature VARCHAR(255), value VARCHAR(255), importance INT);"
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
    query="CREATE TABLE activity_completion (user VARCHAR(255), date DATE, activity_hash DOUBLE, rating INT, exertion INT, attempted BOOL)"
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
    create_activity_feature_table(sql_cursor)
    populate_activity_tables(sql_cursor)

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
    
