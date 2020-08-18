import pdb
#how much variability in feature value is allowed for a 'match' on a continuous feature
tolerances={}
tolerances['Duration']=10

def match_continuous_feature(desired_val, feature, features_df,cursor, user):
    desired_val=float(desired_val)
    features_df['Value']=features_df['Value'].astype(float) 
    tolerance_val=tolerances[feature]
    return features_df[abs(features_df['Value']-desired_val)<tolerance_val]['Hash'].tolist() 

def match_categorical_feature(desired_val, feature, features_df,cursor, user):
    hits=[]
    desired_vals=desired_val.lower().split('/')  
    for index,row in features_df.iterrows():
        cur_category=row['Value'].lower()
        for desired_val in desired_vals:
            if cur_category.__contains__(desired_val):
                hits.append(row['Hash'])
    return hits

def match_novelty(desired_val, feature, features_df, sql_cursor,user):
    hits=[]
    sql="SELECT activity_hash from activity_completion where user = %s"
    vals=(user,)
    sql_cursor.execute(sql,vals)
    seen=[i for i in sql_cursor.fetchall()]
    for index,row in features_df.iterrows():
        cur_activity=row['Hash']
        if cur_activity not in seen:
            hits.append(cur_activity)
    return hits

def match_string(desired_val, feature, features_df, sql_cursor,user):
    #if user doesn't provide a preference for this feature, return [] 
    if desired_val=="NA":
        return []
    #otherwise, return all activity hashes where the feature value string contains the desired_val string 
    return features_df[features_df.Value.str.contains(desired_val)].Hash.tolist()

matchers={}
matchers['Duration']=match_continuous_feature
matchers['Category']=match_categorical_feature
matchers['Intensity']=match_categorical_feature
matchers['Focus']=match_categorical_feature
matchers['GroupVIndividual']=match_categorical_feature
matchers['InstructorGender']=match_categorical_feature
matchers['ClassGender']=match_categorical_feature
matchers['Novelty']=match_novelty
matchers['Instructor']=match_string
matchers['Discipline']=match_categorical_feature
matchers['Exclusion']=match_string
