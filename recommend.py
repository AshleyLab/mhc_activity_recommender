import warnings
warnings.simplefilter(action='ignore', category=Warning)
import argparse
from collections import OrderedDict 
from utils import *
from feature_matcher import * 
from datetime import datetime
import pandas as pd
import random 
import pdb
from update_user import generate_default_preferences

def parse_args(): 
    parser=argparse.ArgumentParser(description="recommend activity")
    #required
    parser.add_argument("-user")
    parser.add_argument("-activity_category",choices=["lifestyle","training","videos","skip"])
    
    #optional (with preset defaults)
    parser.add_argument("--date",default=None,help="format:2020-03-07 15:17:00") 
    parser.add_argument("--outf",default=None,help="if None, print to console, else write string of recommended activities to a file")
    parser.add_argument("--n",type=int,default=3,help="Number of activities to recommend")
    return parser.parse_args() 

def get_user_metadata(sql_cursor,user):
    '''
    Get user feature matrix and fitness level 
    '''    
    query="SELECT feature,value,importance from user_preferences where user=%s;"
    vals=(user,)
    sql_cursor.execute(query,vals)
    user_prefs=pd.DataFrame(sql_cursor.fetchall())
    if user_prefs.shape[0]==0:
        print("WARNING! No feature preferences specified for user:"+str(user)+"; using all default preferences")
        #create a user preferences entry for the current user, specifying the defaults
        generate_default_preferences(sql_cursor,user)
        query="SELECT feature,value,importance from user_preferences where user=%s;"
        vals=(user,)
        sql_cursor.execute(query,vals)
        user_prefs=pd.DataFrame(sql_cursor.fetchall())
        
    #get the user's latest fitness level
    query="SELECT fitness_score from user_fitness where user=%s and date=(select max(date) from user_fitness where user=%s);"
    vals=(user,user)
    sql_cursor.execute(query,vals)
    fitness=sql_cursor.fetchall()
    if len(fitness)==0:
        fitness=config.default_fitness_score #default "average" fitness if non specified 
    else:
        fitness=int(fitness[0][0]) 
    return user_prefs,fitness

def rank_options(options,args):
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

    num_desired=args.n
    num_selected=0
    selected=[]
    annotations=[]
    cur_index=0
    
    while cur_index < len(ranked_options): 
        cur_activities=ranked_options[cur_index][1]
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
        cur_index+=1
    return selected


def generate_recommendation(sql_cursor,sql_db,args):
    '''
    generate an activity recommendation 
    '''

    #Extract the user's latest fitness level & activity preferences
    user_prefs,user_fitness=get_user_metadata(sql_cursor,args.user) 
    user_prefs=user_prefs.rename(columns={0:'Feature',
                               1:'Value',
                               2:'Importance'})
    
    options=dict()
    #each activity within the specified category gets a base count of 1

    #get the activities in the specified category that match the user's fitness level 
    query='select activity_hash,activity_name from activity_metadata where activity_category=%s and min_fitness_level <= %s and max_fitness_level >= %s ;'
    vals=(args.activity_category,user_fitness, user_fitness)
    sql_cursor.execute(query,vals)
    activities=pd.DataFrame(sql_cursor.fetchall())
    activities=activities.rename(columns={0:'Hash',1:'Activity'})
    for activity in activities.Hash:
        options[activity]=1
        
    #select the corresponding feature values for this subset of activities 
    query="select * from activity_features where activity_hash IN {};".format(tuple(activities.Hash))
    sql_cursor.execute(query)
    activity_feature_vals=pd.DataFrame(sql_cursor.fetchall())
    activity_feature_vals=activity_feature_vals.rename(columns={0:'Hash',
                                          1:'Feature',
                                          2:'Value'})
    
    #activities that have features with negative weights are to be excluded
    exclude={}
    for index,row in user_prefs.iterrows():
        cur_feature=row['Feature']
        cur_feature_value=row['Value']
        if str(cur_feature_value) =="nan":
            if cur_feature!="Novelty":
                continue 
        cur_feature_importance=int(row['Importance'])
        activity_cur_feature_vals=activity_feature_vals[activity_feature_vals['Feature']==cur_feature]
        hits=matchers[cur_feature](cur_feature_value, cur_feature, activity_cur_feature_vals, sql_cursor, args.user)

        if cur_feature=='Exclusion':
            #remove the activities where the exclusion criteria are met 
            exclude[hit]=1
            continue
        
        for hit in hits:
            if cur_feature_importance>0:
                options[hit]+=cur_feature_importance
            else:
                exclude[hit]=1
    
    #check user rankings of performed activities
    sql="SELECT activity_hash, rating from activity_completion where user = %s and rating is not NULL" 
    vals=(args.user,)
    sql_cursor.execute(sql,vals)
    result=pd.DataFrame(sql_cursor.fetchall()); 
    for index,row in result.iterrows():
        rated_activity=row[0]
        rating=row[1]
        if rated_activity in options:
            options[rated_activity]+=(rating*5)
            
    #remove all excluded activities (i.e. activities with features that received negative scores)
    for activity in exclude:
        options.__delitem__(activity)

    selected_hashes=rank_options(options,args)

    #get activity names for the hashes
    activity_names=activities.Activity[activities.Hash.isin(selected_hashes)].tolist()
    return selected_hashes,activity_names     

def make_output(activity_hashes, activity_names,sql_cursor,sql_db,args):
    '''
    return activity selection string 
    '''
    if args.outf is None:
        print('specified category:'+args.activity_category)
        for i in range(len(activity_hashes)): 
            print(activity_hashes[i]+'\t'+activity_names[i])
    else:
        outf=open(args.outf,'w')
        outf.write('specified category:'+args.activity_category+'\n')
        for i in range(len(activity_hashes)):
            outf.write(activity_hashes[i]+'\t'+activity_names[i]+'\n')
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
        recommended_activity_hashes, recommended_activity_names=generate_recommendation(sql_cursor,sql_db,args)
        make_output(recommended_activity_hashes, recommended_activity_names,sql_cursor,sql_db, args)

    #close mysql connection
    sql_cursor.close()
    sql_db.close()
    
    
    
    
if __name__=="__main__": 
    main() 
