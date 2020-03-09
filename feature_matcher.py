import pdb
#how much variability in feature value is allowed for a 'match' on a continuous feature
tolerances={}
tolerances['Duration']=10

def match_continuous_feature(desired_val, feature, activities_df,cursor, user):
    desired_val=float(desired_val)
    tolerance_val=tolerances[feature]
    return activities_df[abs(activities_df[feature]-desired_val)<tolerance_val]['Activity'].tolist() 

def match_categorical_feature(desired_val, feature, activities_df,cursor, user):
    hits=[]
    desired_val=desired_val.lower() 
    for index,row in activities_df.iterrows():
        cur_category=row[feature].lower()
        if cur_category.__contains__(desired_val):
            hits.append(row['Activity'])
    return hits

def match_novelty(desired_val, feature, activities_df, sql_cursor,user):
    hits=[]
    sql="SELECT activity from activities where user = %s"
    vals=(user,)
    sql_cursor.execute(sql,vals)
    seen=[i for i in sql_cursor.fetchall()]
    for index,row in activities_df.iterrows():
        cur_activity=row['Activity']
        if cur_activity not in seen:
            hits.append(cur_activity)
    return hits


matchers={}
matchers['Duration']=match_continuous_feature
matchers['Category']=match_categorical_feature
matchers['Intensity']=match_categorical_feature
matchers['Focus']=match_categorical_feature
matchers['GroupVIndividual']=match_categorical_feature
matchers['InstructorGender']=match_categorical_feature
matchers['ClassGender']=match_categorical_feature
matchers['Novelty']=match_novelty
