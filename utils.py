import mysql.connector
import argparse
from config import * 

def open_mysql_connection():
    #values imported from utils.py
    sql_db = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        passwd=mysql_password,
        database=mysql_db)
    
    sql_cursor = sql_db.cursor()
    return sql_db, sql_cursor

def create_activity_hash(to_hash):
    '''
    hash the activity title to a unique, reproducible value stored in the database. 
    '''
    return hash(str(to_hash))

def args_object_from_args_dict(args_dict):
    '''
    pass in arguments as a dictionary in python
    '''
    args_object=argparse.Namespace()
    for key in args_dict:
        vars(args_object)[key]=args_dict[key]
    return args_object

def embedifyYoutubeUrl(s):
    return "https://www.youtube.com/embed/%s" % s.split("/")[-1]
