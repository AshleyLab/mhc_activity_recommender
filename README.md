# mhc_activity_recommender
recommender system of activities for users in MHC 3.0 coaching studies 

Example:
```
./recommend.sh 
                  0         1   2
0          Duration        30  10
1          Category       Abs   9
2         Intensity      High  10
3             Focus  Strength   6
4  GroupVIndividual     Group   4
5  InstructorGender       M/F   3
6       ClassGender       M/F   0
7           Novelty       NaN  10

specified category:video

selected activity:https://youtu.be/CBWQGb4LyAM

selected activity metadata[array(['https://youtu.be/CBWQGb4LyAM', 30, 'Cardio & HIIT Workout',
       'High', 'cardio/strength', 'Group', 'F', 'F', 'Popsugar fitness',
       'Charlee Atkins', nan], dtype=object), array(['https://youtu.be/CBWQGb4LyAM', 30,
       'No-Equipment Cardio & HIIT Workout', 'High', 'cardio',
       'Small group', 'F', 'F', 'POPSUGAR Fitness', 'Charlee Atkins',
       'No'], dtype=object)]

options:['https://youtu.be/CBWQGb4LyAM']
```


Video activities: 
https://docs.google.com/spreadsheets/d/1FEOD2jktd0L3D9_rPbxHPAjDywnwO0z8s5oLYMHgE6E/edit#gid=0


mysql credentials for "dummy" database
user=root
password=password

mysql> use mhc_rec
Database changed
mysql> show tables; 
+-------------------+
| Tables_in_mhc_rec |
+-------------------+
| activities        |
+-------------------+
1 row in set (0.00 sec)

mysql> describe activities 
    -> ; 
+----------+---------------+------+-----+---------+-------+
| Field             | Type          | Null | Key | Default | Extra |
+----------+---------------+------+-----+---------+-------+
| user              | varchar(100)  | YES  |     | NULL    |       |
| date              | datetime      | YES  |     | NULL    |       |
| activity_category |varchar(1000)  | YES  |     | NULL    |       |
| activity 	    | varchar(1000) | YES  |     | NULL    |       |
| rank     	    | tinyint(4)    | YES  |     | NULL    |       |
+----------+---------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
