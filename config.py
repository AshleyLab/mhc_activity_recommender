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
nonmodifiable_feature_file='metadata/NonmodifiableFeatures.tsv'
modifiable_feature_file='metadata/ModifiableFeatures.tsv'
