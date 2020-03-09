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
    parser.add_argument("--feature_ranks",default=None, help="tsv file with feature name in column 1, feature value in column 2,  rank 0 to 10 in column 3")
    parser.add_argument("--outf",default=None,help="if None, print to console, else write string of recommended activities to a file")
    return parser.parse_args() 


def generate_recommendation(sql_cursor,sql_db,args):
    '''
    generate an activity recommendation 
    '''
    activity_options=pd.read_csv(metadata[args.activity_category],header=0,sep='\t')
    features=pd.read_csv(args.feature_ranks,header=None,sep='\t')

    assert features[2].min()>=0
    assert features[2].max()<=10
    
    #features=features.sort_values(by=2,ascending=False)
    print(features)
    
    options=dict()
    #each activity gets a base count of 1
    activities=activity_options['Activity'].tolist()
    for activity in activities:
        options[activity]=1
        
    for index,row in features.iterrows():
        cur_feature=row[0]
        cur_feature_value=row[1]
        cur_feature_importance=row[2]
        hits=matchers[cur_feature](cur_feature_value, cur_feature, activity_options, sql_cursor, args.user)
        for hit in hits:
            options[hit]+=cur_feature_importance
            
    #rank options by those with highest hits 
    ranked_options=sorted(options.items(),key=lambda x: x[1], reverse=True)
    max_score=ranked_options[0][1]
    recommended_activities=[ranked_options[0][0]] 
    for i in range(1,len(ranked_options)):
        cur_score=ranked_options[i][1]
        if cur_score < max_score:
            break
        else:
            recommended_activities.append(ranked_options[i][0])

    #randomly select an activity
    selected_activity=random.choice(recommended_activities)
    return selected_activity,recommended_activities 

def make_output(activity,choices,sql_cursor,sql_db,args):
    '''
    populate database with activity selection string 
    return activity selection string 
    '''
    #write activity entry to db
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
        print('selected activity:'+str(activity))
        print('options:'+str(choices))
    else:
        outf=open(args.outf,'w')
        outf.write('specified category:'+args.activity_category+'\n')
        outf.write('selected activity:'+activity+'\n')
        outf.write('options:'+'\t'.join(choices)+'\n')
        outf.close()
       
def main():
    #read program arguments
    args=parse_args()
    
    #create mysql connection
    sql_db,sql_cursor =open_mysql_connection()

    if args.activity_category=="skip":
        #user selected to skip exercise
        make_output('skip','skip',sql_cursor,sql_db, args)
    else:
        #recommend an exercise
        recommendation,choices=generate_recommendation(sql_cursor,sql_db,args)
        make_output(recommendation,choices,sql_cursor,sql_db, args)

    #close mysql connection
    sql_cursor.close()
    sql_db.close()
    
    
    
    
if __name__=="__main__": 
    main() 
