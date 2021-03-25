# mhc_activity_recommender
recommender system of activities for users in MHC 3.0 coaching studies 

Recommender diagram: https://app.lucidchart.com/invitations/accept/eedbfd98-0913-4939-9364-426563929ba2

## 0) Pre-requesits

* Install [MySql](https://dev.mysql.com/downloads/mysql/)
* Install python libraries ie `pip install mysql-connector-python` (TODO: Requirements.txt)

## 1) Verify that the configuration & activity source files are updated.

`config.py` contains configuration details for:  
a) connection to MySQLDB  
b) paths to the PhysicalActivity.tsv, EnduranceSessions.tsv, ExerciseVideoLinks.tsv exercise metadata  
c) Path to list of features users can modify preferences for (i.e.  metadata/ModifiableFeatures.tsv)  
d) Fitness thresholds (min=1, max=5, default =3)  

## 2) Set up the MySQL database backend

execute:

```
python create_mysql_db.py
```

This sets up the MySQL database (mhc_rec), creates (overwrites!) the tables, and populates the "activity_features" and "activity_metadata" tables:

```
mysql> show tables; 
+---------------------+
| Tables_in_mhc_rec   |
+---------------------+
| activity_completion |
| activity_features   |
| activity_metadata   |
| user_fitness        |
| user_preferences    |
+---------------------+
5 rows in set (0.00 sec)

mysql> describe activity_metadata; 
+---------------------+--------------+------+-----+---------+-------+
| Field               | Type         | Null | Key | Default | Extra |
+---------------------+--------------+------+-----+---------+-------+
| activity_hash       | varchar(255) | YES  |     | NULL    |       |
| activity_name       | varchar(255) | YES  |     | NULL    |       |
| activity_category   | varchar(255) | YES  |     | NULL    |       |
| min_fitness_level   | int(11)      | YES  |     | NULL    |       |
| max_fitness_level   | int(11)      | YES  |     | NULL    |       |
| target_exertion_min | int(11)      | YES  |     | NULL    |       |
| target_exertion_max | int(11)      | YES  |     | NULL    |       |
+---------------------+--------------+------+-----+---------+-------+
7 rows in set (0.00 sec)

mysql> describe activity_features; 
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| activity_hash | varchar(255) | YES  |     | NULL    |       |
| feature       | varchar(255) | YES  |     | NULL    |       |
| feature_value | varchar(255) | YES  |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

mysql> describe activity_completion; 
+-------------------+--------------+------+-----+---------+-------+
| Field             | Type         | Null | Key | Default | Extra |
+-------------------+--------------+------+-----+---------+-------+
| user              | varchar(255) | YES  |     | NULL    |       |
| date              | date         | YES  |     | NULL    |       |
| activity_hash     | varchar(255) | YES  |     | NULL    |       |
| activity_category | varchar(255) | YES  |     | NULL    |       |
| rating            | int(11)      | YES  |     | NULL    |       |
| exertion          | int(11)      | YES  |     | NULL    |       |
| attempted         | tinyint(1)   | YES  |     | NULL    |       |
+-------------------+--------------+------+-----+---------+-------+
7 rows in set (0.00 sec)

mysql> describe user_fitness; 
+---------------+--------------+------+-----+---------+-------+
| Field         | Type         | Null | Key | Default | Extra |
+---------------+--------------+------+-----+---------+-------+
| user          | varchar(255) | YES  |     | NULL    |       |
| date          | date         | YES  |     | NULL    |       |
| fitness_score | double       | YES  |     | NULL    |       |
+---------------+--------------+------+-----+---------+-------+
3 rows in set (0.00 sec)

mysql> describe user_preferences; 
+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| user       | varchar(255) | YES  |     | NULL    |       |
| feature    | varchar(255) | YES  |     | NULL    |       |
| value      | varchar(255) | YES  |     | NULL    |       |
| importance | int(11)      | YES  |     | NULL    |       |
+------------+--------------+------+-----+---------+-------+
4 rows in set (0.00 sec)
```


## 3) Populate user preferences & fitness levels

```
python update_user.py --help 
usage: update_user.py [-h] [-user USER] [-user_pref_file USER_PREF_FILE]
                      [--user_fitness_level {1,2,3,4,5}]

updated user information

optional arguments:
  -h, --help            show this help message and exit
  -user USER            unique user identifier
  -user_pref_file USER_PREF_FILE
                        tab-separated file with columns Feature, Value,
                        Importance
  --user_fitness_level {1,2,3,4,5}
                        fitness level 1 (lowest) - 5 (highest)
```

Execute the script `update_user.sh` for an example of the input values 

## 4) Generate activity recommendations

```
 python recommend.py --help 
usage: recommend.py [-h] [-user USER]
                    [-activity_category {lifestyle,training,videos,skip}]
                    [--outf OUTF] [--n N]

recommend activity

optional arguments:
  -h, --help            show this help message and exit
  -user USER
  -activity_category {lifestyle,training,videos,skip}
  --outf OUTF           if None, print to console, else write string of
                        recommended activities to a file
  --n N                 Number of activities to recommend
```

Execute `recommend.sh` as an example

## 5) Rate the activities and adjust user's fitness levels

```
python rate.py --help 
usage: rate.py [-h] [-user USER] [-activity_hash ACTIVITY_HASH]
               [-activity_category {lifestyle,training,videos,skip}]
               [-rating {-1,0,1}]
               [-exertion {6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}]
               [-attempted {True,False}]
               [--exertion_mismatch_thresh_to_adjust_fitness EXERTION_MISMATCH_THRESH_TO_ADJUST_FITNESS]

rank an exercise activity -1,0,1

optional arguments:
  -h, --help            show this help message and exit
  -user USER
  -activity_hash ACTIVITY_HASH
  -activity_category {lifestyle,training,videos,skip}
  -rating {-1,0,1}
  -exertion {6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}
  -attempted {True,False}
  --exertion_mismatch_thresh_to_adjust_fitness EXERTION_MISMATCH_THRESH_TO_ADJUST_FITNESS
                        if user's reported exertion differs from the expected
                        exertion for the ativity by this much (or greater),
                        adjust the user's fitness score

```
Execute `rate.sh` as an example.

