#skip activity 
python recommend.py \
       --user testuser\
       --date "2020-03-07 15:21:00" \
       --activity_category skip

#recommend a series  of 5 activities using feature values/weights from test_feature_sets/test_feature_ranks.tsv, with replacement potentially
python recommend.py \
       --user testuser\
       --date "2020-03-06 15:21:00" \
       --activity_category video \
       --feature_ranks test_feature_sets/test_feature_ranks.tsv \
       --n 5 \
       --with_replacement \
       --prob_duplicate 0.3


#recommend a random series of activities, with replacement 
python recommend.py \
       --user testuser\
       --date "2020-03-16 15:21:00" \
       --activity_category video \
       --feature_ranks test_feature_sets/random_feature_ranks.tsv \
       --n 10 \
       --with_replacement \
       --prob_duplicate 0.3
