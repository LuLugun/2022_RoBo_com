import pymysql
import numpy as np
import datetime
import time
import requests
import pandas as pd

def sql_connect(host,port,user,passwd,database):
    global db,cursor
    try:
        db=pymysql.connect(host=host,user=user,passwd=passwd,database=database,port =port)
        #os.system('cls')
        cursor=db.cursor()
        return True
    except pymysql.Error as e:
        print("連線失敗:"+str(e))
        return False

def get_data():
    domain_url = 'https://www.taoyuan-airport.com/uploads/govdata/FidsPassenger.csv'
    response = requests.get(domain_url)
    response = response.text
    response = response.split('\r\n')
    return response

def auto_updata(response):
    sql = '''INSERT INTO `fidspassenger` (`COL 1`, `COL 2`, `COL 3`, `COL 4`, `COL 5`, `COL 6`, `COL 7`, `COL 8`, `COL 9`, `COL 10`, `COL 11`, `COL 12`, `COL 13`, `COL 14`, `COL 15`, `COL 16`, `COL 17`, `COL 18`, `COL 19`, `COL 20`, `COL 21`, `COL 22`) VALUES '''
    for i in range(1,len(response)-1):
        values = response[i].replace(',',"','")
        sql += "('"+values+"'),"
    with open('result.txt','w') as f:
        f.write(sql)
        f.close()
    cursor.execute(sql[:-1])
    db.commit()

def truncate_table():
    sql ='''TRUNCATE `robo_com`.`fidspassenger`;'''
    cursor.execute(sql)
    db.commit()

def getday(the_date):
    result_date = the_date + datetime.timedelta(days=1)
    return result_date

sql_connect('localhost',3306,'root','','robo_com')
truncate_table()
auto_updata(get_data())

while True:
    sql_connect('localhost',3306,'root','','robo_com')
    truncate_table()
    auto_updata(get_data())
    now_time = time.localtime()
    now_time = time.strftime('%Y-%m-%d %H:%M:%S',now_time)
    print(now_time)
    time.sleep(3600)
    

