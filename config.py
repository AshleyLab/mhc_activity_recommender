#cache mysql credentials here -- this is very bad and not secure, but nothing in the demo db is valuable
mysql_host='localhost'
mysql_user='root'
mysql_password='password'
mysql_db='mhc_rec'

#match of exercise category to activity metadata 
metadata={'lifestyle':'activities/PhysicalActivity.tsv',
          'training':'activities/EnduranceSessions.tsv',
          'video':'activities/ExerciseVideoLinks.tsv'}

#list of features to use
modifiable_feature_file='metadata/ModifiableFeatures.tsv'


#fitness thresholds
max_fitness_score=5
min_fitness_score=1
default_fitness_score=3
