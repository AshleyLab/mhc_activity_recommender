import argparse 
from utils import * 

def parse_args(): 
    parser=argparse.ArgumentParser(description="recommend activity") 
    parser.add_argument("--user") 
    parser.add_argument("--date") 
    parser.add_argument("--activity_selection") 
    parser.add_argument("--feature_ranks",help="tsv file with feature name in column 1 and rank 1 to 10 in column 2")
    parser.add_argument("--num_choices_to_recommend",type=int,default=1)
    return parser.parse_args() 

def main(): 
    args=parse_args() 
    
if __name__=="__main__": 
    main() 
