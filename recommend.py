import argparse
from collections import OrderedDict 
from utils import *
from feature_matcher import * 
from datetime import datetime
import pandas as pd
import random 
import pdb

def parse_args(): 
    parser=argparse.ArgumentParser(description="recommend activity") 
    parser.add_argument("--user") 
    parser.add_argument("--date",default=None,help="format:2020-03-07 15:17:00") 
    parser.add_argument("--activity_category",choices=["lifestyle","training","video","skip"]) 
    parser.add_argument("--feature_ranks",default=None, help="tsv file with feature name in column 1, feature value in column 2,  rank 0 to 10 in column 3, or -1 to exclude")
    parser.add_argument("--outf",default=None,help="if None, print to console, else write string of recommended activities to a file")
    parser.add_argument("--n",type=int,default=1,help="Number of activities to recommend")
    parser.add_argument("--with_replacement",default=False,action="store_true",help="allow the same activitiy to be recommended multiple times")
    parser.add_argument("--prob_duplicate",type=float,default=0.5,help="tune this parameter from 0 to 1 to control how many activities are reported multiple times; 0 = many repeats; 1 = no repeats")
    return parser.parse_args() 


def generate_recommendation(sql_cursor,sql_db,args):
    '''
    generate an activity recommendation 
    '''
    activity_options=pd.read_csv(metadata[args.activity_category],header=0,sep='\t')
    features=pd.read_csv(args.feature_ranks,header=None,sep='\t')

    assert features[2].min()>=-1
    assert features[2].max()<=10
    
    #print(features)
    
    options=dict()
    #each activity gets a base count of 1
    activities=activity_options['Activity'].tolist()
    for activity in activities:
        options[activity]=1

    #activities that have features with negative weights are to be excluded
    exclude={}
    for index,row in features.iterrows():
        cur_feature=row[0]
        cur_feature_value=row[1]
        if str(cur_feature_value) =="nan":
            continue 
        cur_feature_importance=int(row[2])
        hits=matchers[cur_feature](cur_feature_value, cur_feature, activity_options, sql_cursor, args.user)
        for hit in hits:
            if cur_feature_importance>0:
                options[hit]+=cur_feature_importance
            else:
                exclude[hit]=1
    
    #check user rankings of performed activities
    sql="SELECT activity, rank from activities where user = %s and rank is not NULL" 
    vals=(args.user,)
    sql_cursor.execute(sql,vals)
    result=[i for i in sql_cursor.fetchall()]
    for entry in result:
        rated_activity=entry[0]
        rating=entry[1]
        if rated_activity in options:
            options[rated_activity]+=rating
            
    #remove all excluded activities (i.e. activities with features that received negative scores)
    for activity in exclude:
        options.__delitem__(activity)


    #create buckets of score --> activity
    options_rev={}
    for activity in options:
        score=options[activity]
        if score not in options_rev:
            options_rev[score]=[activity]
        else:
            options_rev[score].append(activity)
    #rank options by those with highest hits 
    ranked_options=sorted(options_rev.items(),key=lambda x: x[0], reverse=True)
    #print(ranked_options) 
    num_desired=args.n
    num_selected=0
    selected=[]
    annotations=[]
    cur_index=0
    while cur_index < len(ranked_options): 
        i=cur_index
        cur_activities=ranked_options[i][1]
        #shuffle in place
        random.shuffle(cur_activities)
        for activity in cur_activities: 
            if num_selected < num_desired:
                selected.append(activity)
                num_selected+=1
            else:
                break
        if num_selected==num_desired:
            break
        if args.with_replacement is True:
            if random.random() < args.prob_duplicate: 
                cur_index+=1
        else:
            cur_index+=1
    return selected

def make_output(activities,sql_cursor,sql_db,args):
    '''
    populate database with activity selection string 
    return activity selection string 
    '''
    #write activity entry to db
    for activity in activities:
        sql="INSERT INTO activities (user, date, activity_category, activity) VALUES (%s, %s, %s, %s)"
        if args.date is None:
            cur_datetime=datetime.now()
        else:
            cur_datetime=datetime.strptime(args.date,'%Y-%m-%d %H:%M:%S')
        
        vals=(args.user, cur_datetime, args.activity_category, activity)
        sql_cursor.execute(sql,vals)
        sql_db.commit() 
    
    if args.outf is None:
        print('specified category:'+args.activity_category)
        for activity in activities:
            print(activity)
    else:
        outf=open(args.outf,'w')
        outf.write('specified category:'+args.activity_category+'\n')
        for activity in activities:
            outf.write(activity+'\n')
        outf.close()
       
def main():
    #read program arguments
    args=parse_args()
    
    #create mysql connection
    sql_db,sql_cursor =open_mysql_connection()

    if args.activity_category=="skip":
        #user selected to skip exercise
        make_output(['skip']*args.n,sql_cursor,sql_db, args)
    else:
        #recommend an exercise
        recommendations=generate_recommendation(sql_cursor,sql_db,args)
        make_output(recommendations,sql_cursor,sql_db, args)

    #close mysql connection
    sql_cursor.close()
    sql_db.close()
    
    
    
    
if __name__=="__main__": 
    main() 
