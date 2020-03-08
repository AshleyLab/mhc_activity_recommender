def match_duration(desired_val, feat_importance, activities_df):
    return []

def match_category(desired_val, feat_importance, activities_df):
    return []

def match_intensity(desired_val, feat_importance, activities_df):
    return []

def match_focus(desired_val, feat_importance, activties_df):
    return []

def match_group_v_individual(desired_val, feat_importance, activities_df):
    return []

def match_instructor_gender(desired_val, feat_importance, activities_df):
    return []

def match_class_gender(desired_val, feat_importance, activities_df):
    return []

def match_novelty(desired_val, feat_importance, activities_df):
    return []

matchers={}
matchers['Duration']=match_duration
matchers['Category']=match_category
matchers['Intensity']=match_intensity
matchers['Focus']=match_focus
matchers['GroupVIndividual']=match_group_v_individual
matchers['InstructorGender']=match_instructor_gender
matchers['ClassGender']=match_class_gender
matchers['Novelty']=match_novelty
