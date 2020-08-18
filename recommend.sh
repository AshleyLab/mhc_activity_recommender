#skip activity 
python recommend.py \
       -user testuser\
       -activity_category skip

#recommend a series  of 5 activities using feature values/weights from test_feature_sets/test_feature_ranks.tsv, with replacement potentially
python recommend.py \
       -user testuser\
       -activity_category videos \
       --n 5

#recommend a random series of activities, with replacement 
python recommend.py \
       -user testuser2\
       -activity_category videos \
       --n 3
