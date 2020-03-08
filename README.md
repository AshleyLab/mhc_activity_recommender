# mhc_activity_recommender
recommender system of activities for users in MHC 3.0 coaching studies 

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
