import requests
import datetime
import csv
import pymysql
import time

def pull_file(git_url,today,filename):
    response=requests.get(git_url)
    if response.status_code!=200:
        with open("logs.txt","a") as f1:
            f1.write(str(datetime.datetime.now())+":"+str(response.raise_for_status)+" File not found error" if response.status_code==404 else " unexpected error")
            f1.write("\n")
            return False
    with open(filename,"wb") as f:
        for data in response.iter_content(chunk_size=64):
            if data:
                f.write(data)

def update_sql_db(eid,ename,esal,ecity,mod):
    try:
        conn=pymysql.connect(host="localhost",database="jan",user="root",password="root")
        cursor=conn.cursor()
        cursor.execute("create table if not exists employee_records (eid int primary key, ename varchar(10),esal float, ecity varchar(10))")
        if mod=="A":
            if cursor.execute("select eid from employee_records where eid=%s",eid):
                print("entry alredy exist")
                return
            sql="insert into employee_records (eid,ename,esal,ecity) values (%s, %s, %s, %s)"
            cursor.execute(sql, (eid,ename,esal,ecity))
            conn.commit()
        elif mod=="D":
            sql="delete from employee_records where eid=%s"
            cursor.execute(sql,eid)
            conn.commit()
        elif mod=="C":
            sql="update employee_records set ename=%s, esal=%s, ecity=%s where eid=%s"
            cursor.execute(sql,(ename,esal,ecity,eid))
            conn.commit()
        else:
            print("The file is corrupt")
    except Exception as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def process_file(filename):
    flag=0
    with open (filename, "r",encoding="UTF-8") as f2:
        r=csv.reader(f2)
        next(r) # skipping header
        datas=list(r)
        for data in datas:
            for item in map(lambda x: x.split(","),data): #data will be in format ["101,adarsh,1000,bangalore"]
                mod=str(item[0]).strip()
                eid=int(item[1])
                ename=str(item[2]).strip()
                esal=float(item[3])
                ecity=str(item[4]).strip()
            if eid==None or (len(str(eid))<2 and len(str(eid))>6):
                flag=1
            elif ename==None or len(ename)>10:
                flag=1
            elif esal==None or esal<0:
                flag=1
            elif ecity==None or  len(ecity)>10:
                flag=1
            if flag==1:
                print("data in file is not correct:",eid,ename,esal,ecity)
            else:
                update_sql_db(eid,ename,esal,ecity,mod)


def main(last_processed_date,today,git_url,filename):
    while True:
        if last_processed_date==None:
            print("file processing for the first time")
            pull_status=pull_file(git_url,today,filename)
            if pull_status==False:
                print("Processing failed, check log for more details")
                return
            process_file(filename)
        elif last_processed_date==today:
            print("File already processed for today")
        else:
            pull_status=pull_file(git_url,today,filename)
            if pull_status==False:
                print("Processing failed, check log for more details")
                return
            process_file(filename)
         
        time.sleep(60)    
        last_processed_date=today

#get the name of the file to be processed
git_url="https://raw.githubusercontent.com/adhu53/Docker_ETL/refs/heads/main/employees_2026-01-09.csv"
today=datetime.datetime.now().strftime("%Y-%m-%d")
filename="employees_"+today+".csv"
print(filename)
last_processed_date=None

if __name__=="__main__":
    main(last_processed_date,today,git_url,filename)