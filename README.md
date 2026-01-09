# Docker_ETL
##Author: Adarsh M D 
##last modified: 09 Jan 2026
The github_to_mysql.py is a python script that pulls the file from Github every 24 hours and does the necessary transformation and loads to Mysql DB after Data validation.
The while loop mentioned is a optional case. this could be better done by setting up a cron or by cloud schedular.
*************************
the script will process the delta file present in github
modtype
A --> Addition of any record
D --> deletion of any record
C --> Change of any data for the record 


