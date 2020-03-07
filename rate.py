import argparse 
def parse_args(): 
    parser=argparse.ArgumentParser(description="rank an exercise activity -1,0,1")
    parser.add_argument("--user") 
    parser.add_argument("--date") 
    parser.add_argument("--activity_category") 
    parser.add_argument("--activity_name") 
    parser.add_argument("--rank",type=int) 
    return parser.parse_args() 


def main(): 
    args=parse_args() 
if __name__=="__main__": 
    main() 

