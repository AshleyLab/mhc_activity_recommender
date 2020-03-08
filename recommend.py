import argparse
from utils import *
from feature_matcher import * 
from datetime import datetime

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
    activity_options=pd.read_csv(metadata[args.activity_category],header=True,sep='\t')
    features=pd.read_csv(args.feature_ranks,header=None,sep='\t')
    assert features[2].min>=0
    assert features[2].max<=10
    
    features=features.sort_values(by=2,reverse=True)
    print(features)
    options=OrderedDict
    

def make_output(activity,sql_cursor,sql_db,args):
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
        print(str(activity))
    else:
        outf=open(args.outf,'w')
        outf.write(activity)
        outf.close()
       
def main():
    #read program arguments
    args=parse_args()
    
    #create mysql connection
    sql_db,sql_cursor =open_mysql_connection()

    if args.activity_category=="skip":
        #user selected to skip exercise
        make_output('skip',sql_cursor,sql_db, args)
    else:
        #recommend an exercise
        recommendation=generate_recommendation(sql_cursor,sql_db,args)
        make_output(recommendation,sql_cursor,sqld_db, args)

    #close mysql connection
    sql_db.close()
    
    
    
    
if __name__=="__main__": 
    main() 
