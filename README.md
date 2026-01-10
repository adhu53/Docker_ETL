## Docker_ETL
## Author: Adarsh M D 
## last modified: 10 Jan 2026
### Long-running Dockerized ETL service that continuously polls a GitHub repository for new files. When a new file is detected, it is downloaded, validated, and processed into MySQL. The ETL container stays running, while state and idempotency are handled in the databaseCustom Docker image using Python slim. The image packages ETL logic and required libraries. The container runs as a long-lived service that continuously polls GitHub for new data files and loads them into MySQL.
##### Docker Compose is to orchestrate two containers: a MySQL container for persistent storage and a custom ETL container built from a Dockerfile. The ETL container runs as a long-lived service that continuously pulls data from GitHub and loads it into MySQL.
#### Logic file: etl.py
#### containerization: docker-compose.yml,dockerfile.yml
##### inputfile: <filename>_<date>.csv. The input to the file is a delta file where mod indicating the data change type.
# A- new recorded created
# D- a record was deleted
# C - one or more fiels in the record has been changed.
# logs:logs.txt
# frequency: runs once a day or can be even scheduled to run every hour. Once the file is processed for the day, next day it starts processing again when new feed is received.  
###################################################
## The continous monitoring of github repo using the while loop can be eliminated by using a cron job or by automating using cloud scheduler.
