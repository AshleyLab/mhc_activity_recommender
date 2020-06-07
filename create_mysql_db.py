'''
Script to create a mysql DB instance 
'''
import argparse
from utils import *
import mysql.connector

def parse_args():
    parser=argparse.ArgumentParser(description="create mysql database and tables")
    parser.add_argument("--lifestyle")
    parser.add_argument("--training")
    parser.add_argument("--video")
    return parser.parse_args() 
    

def create_mysql_db(sql_cursor):
    #check if database exists 
    sql_cursor.execute("SHOW DATABASES")
    result=[i for i in sql_cursor.fetchall()]
    if mysql_db not in result:
        #the database does not exist, we create it
        sql_cursor.execute("CREATE DATABASE %s",(mysql_db))
    return 

def create_activity_metadata_table(sql_cursor):
    query="CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))"
    pass

def populate_activity_metadata_table(sql_cursor,args):
    pass

def create_user_preferences_table(sql_cursor):
    pass

def create_user_fitness_table(sql_cursor):
    pass

def create_activity_completion_table(sql_cursor):
    pass

    
def create_and_populate_tables(args):
    if type(args)==type({}):
        args=args_object_from_args_dict(args)
    
    #create database if it doesn't exist
    sql_connector=mysql.connector(host=mysql_host,
                         user=mysql_user,
                         passwd=mysql_password)
    sql_cursor = sql_connector.cursor()
    
    #create mysql db if it does not exist 
    create_mysql_db(sql_cursor)

    #connect to the db
    sql_db,sql_cursor=open_mysql_connection()
    
    #create and populate activity_metadata table
    create_activity_metadata_table(sql_cursor)
    populate_activity_metadata_table(sql_cursor,args)

    #create user_preference table
    create_user_preferences_table(sql_cursor)

    #create user_fitness table
    create_user_fitness_table(sql_cursor)

    #create activity_completion table
    create_activity_completion_table(sql_cursor)
    
def main():
    args=parse_args()
    create_and_populate_tables(args)

    
if __name__=="__main__":
    main()
    
