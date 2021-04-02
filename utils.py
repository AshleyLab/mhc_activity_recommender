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


import requests
def validVideoId(id):
    r = requests.get("https://img.youtube.com/vi/%s/mqdefault.jpg" % id)
    return (r.status_code == 200)

def embedifyYoutubeUrl(s):
    """ 
    :param s: url of youtube video either in format https://www.youtube.com/watch?v=ID or https://youtu.be/Q9MnfvJAg5s
    :return: url in format for embedding video

    This should probably be moved to a Flask function at some point
    """
    embed_url = "https://www.youtube.com/embed/%s"
    if "=" in s:
        youtube_id =  s.split("=")[-1]
    else:
        youtube_id =  s.split("/")[-1]
    if not validVideoId(youtube_id):
        print("WARNING: Youtube id: %s is invalid" % youtube_id)
    return embed_url % youtube_id
