# mhc_activity_recommender
recommender system of activities for users in MHC 3.0 coaching studies 

Example:
```
./recommend.sh 
specified category:skip
selected activity:skip
options:skip

---------------------------------------------------------
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
Example for rating an activity
```
./rate.sh 
('testuser', datetime.datetime(2020, 3, 7, 15, 21), 'skip', 'skip', 1)
('testuser', datetime.datetime(2020, 3, 6, 15, 21), 'video', 'https://youtu.be/CBWQGb4LyAM', 1)
```

Video activities: 
https://docs.google.com/spreadsheets/d/1FEOD2jktd0L3D9_rPbxHPAjDywnwO0z8s5oLYMHgE6E/edit#gid=0

```
mysql credentials for example database
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

mysql> describe activities; 
+-------------------+---------------+------+-----+---------+-------+
| Field             | Type          | Null | Key | Default | Extra |
+-------------------+---------------+------+-----+---------+-------+
| user              | varchar(100)  | YES  |     | NULL    |       |
| date              | datetime      | YES  |     | NULL    |       |
| activity_category | varchar(1000) | YES  |     | NULL    |       |
| activity_hash     | varchar(1000) | NO   |     | NULL    |       |
| rating            | tinyint(4)    | YES  |     | NULL    |       |
| fitness           | int(11)       | YES  |     | NULL    |       |
| exertion          | int(11)       | YES  |     | NULL    |       |
| attempted         | tinyint(1)    | YES  |     | NULL    |       |
+-------------------+---------------+------+-----+---------+-------+
8 rows in set (0.00 sec)

mysql> select * from activities; 
+----------+---------------------+-------------------+------------------------------+------+
| user     | date                | activity_category | activity                     | rank |
+----------+---------------------+-------------------+------------------------------+------+
| testuser | 2020-03-06 15:21:00 | video             | https://youtu.be/CBWQGb4LyAM |    1 |
| testuser | 2020-03-07 15:21:00 | skip              | skip                         |    1 |

```
