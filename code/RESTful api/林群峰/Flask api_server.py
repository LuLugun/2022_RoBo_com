import numpy as np
import pymysql
import os
import pathlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from robo_function import *
from flight_function import *
import datetime
import time
import json

SRC_PATH = pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,'jpg_save','original')

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)
driver = webdriver.Chrome(chrome_options = chromeoptions)


def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getday():
    the_date = datetime.date.today()
    result_date = the_date + datetime.timedelta(days=-1)
    d = result_date.strftime('%Y/%m/%d')
    return d
    
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

def sql_insert(value,remark):
    sql = '''INSERT INTO `api_test`(`value`, `remark`) VALUES ('%s','%s')'''%(value,remark)
    cursor.execute(sql)
    db.commit()
    

def sql_insert_detect(value,remark):
    sql = '''INSERT INTO `api_test`(`value`, `remark`) VALUES ('%.2f','%s')'''%(value,remark)
    cursor.execute(sql)
    db.commit()


def sql_insert_ip(value):
    sql = '''INSERT INTO `get_ip`(`ip`) VALUES ('%s')'''%(value)
    cursor.execute(sql)
    db.commit()

def sql_select_get():
    sql = '''SELECT * FROM `api_test` ORDER BY `input time` DESC LIMIT 1'''
    cursor.execute(sql)
    result=cursor.fetchall()
    return result[0]

def sql_select_get_robo_state():
    sql = '''SELECT * FROM `robo_state`'''
    cursor.execute(sql)
    result=cursor.fetchall()
    return result[0]

def sql_select_get_number(country):
    sql = '''SELECT DISTINCT `COL 3`,`COL 5` FROM `fidspassenger` WHERE `COL 12` LIKE '%'''+str(country)+'''%';'''
    #print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    if str(result) == '()':
        return 'None'
    else:
        return json.dumps(result)

def sql_chin_country_select(country):
    the_date = datetime.date.today()
    the_date = the_date.strftime('%Y/%m/%d')
    now_time = time.localtime()
    now_time = time.strftime('%H:%M:%S',now_time)
    sql = '''SELECT `COL 1` ,`COL 3` ,`COL 5` ,`COL 20` FROM `fidspassenger` WHERE `COL 13` LIKE '%%%s%%' and `COL 20` != '' AND `COL 7` > '%s' AND `COL 8` > '%s' or (`COL 13` LIKE '%%%s%%' and `COL 20` != '' AND `COL 7` > '%s');'''%(country,getday(),now_time,country,the_date)
    print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    if str(result) == '()':
        return 'None'
    else:
        return result

def sql_english_country_select(country):
    the_date = datetime.date.today()
    the_date = the_date.strftime('%Y/%m/%d')
    now_time = time.localtime()
    now_time = time.strftime('%H:%M:%S',now_time)
    sql = '''SELECT `COL 1` ,`COL 3` ,`COL 5` ,`COL 20` FROM `fidspassenger` WHERE `COL 12` LIKE '%%%s%%' and `COL 20` != '' AND `COL 7` > '%s' AND `COL 8` > '%s' or (`COL 12` LIKE '%%%s%%' and `COL 20` != '' AND `COL 7` > '%s');'''%(country,getday(),now_time,country,the_date)
    
    #print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    if str(result) == '()':
        return 'None'
    else:
        return result

def sql_select_get_number(country):
    sql = '''SELECT DISTINCT `COL 3`,`COL 5` FROM `fidspassenger` WHERE `COL 12` LIKE '%'''+str(country)+'''%';'''
    #print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    if str(result) == '()':
        return 'None'
    else:
        return json.dumps(result)

def sql_select_get_flight(number):
    airline = number[:2]
    shift = number[2:]
    the_date = datetime.date.today()
    the_date = the_date.strftime('%Y/%m/%d')
    now_time = time.localtime()
    now_time = time.strftime('%H:%M:%S',now_time)
    sql = '''SELECT * FROM `fidspassenger` WHERE `COL 3` = '%s' AND `COL 5` = %s and `COL 20` != '' AND `COL 7` > '%s' AND `COL 8` > '%s' or (`COL 3` = '%s' AND `COL 5` = '%s' and `COL 20` != '' AND `COL 7` > '%s');'''%(airline,shift,getday(),now_time,airline,shift,the_date)
    #print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    if str(result) == '()':
        return 'None'
    else:
        return json.dumps(result[0])

def sql_updata_robo_state(value):
    sql = '''UPDATE `robo_state` SET `robo_state`= '%s';'''%(value)
    cursor.execute(sql)
    db.commit()

def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

@app.route('/post/select/<string:country>', methods=['POST'])
def postflight_select(country):
    driver.get("https://www.taoyuan-airport.com/flight_depart?k=&time=all")
    Web_Driver_Wait(driver,'board')
    local_time = time.localtime()
    if local_time.tm_hour >= 18:
        change_time(driver)
        time.sleep(1)
    input_Keyword_search(driver,country)
    time.sleep(2)
    result_date = get_data(driver)
    return result_date



@app.route('/post', methods=['POST'])
def postInput():
    insertValues = request.get_json()
    value=insertValues['value']
    remark=insertValues['remark']
    if sql_connect('localhost',3306,'root','','robo_com'):
        try:
            sql_insert(value,remark)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/post/flight/<string:number>', methods=['POST'])
def postflight(number):
    if sql_connect('localhost',3306,'root','','robo_com'):
        try:
            result = sql_select_get_flight(number)
            return str(result)
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/post/country/<string:country>', methods=['POST'])
def postcountry(country):
    data_dict = {'label':[]}
    if sql_connect('localhost',3306,'root','','robo_com'):
        if is_all_chinese(country):
            result = sql_chin_country_select(country)
            if result != 'None':
                for i in result:
                    data_dict['label'].append(i[1]+i[2])
                    data_dict[i[1]+i[2]] = {'terminal':i[0],'counter':i[3]}
        else:
            result = sql_english_country_select(country)
            #print(result)
            if result != 'None':
                for i in result:
                    data_dict['label'].append(i[1]+i[2])
                    data_dict[i[1]+i[2]] = {'terminal':i[0],
                                                'counter':i[3]}
        return data_dict


    else:
        return 'return : SQL connect FAIL', 500

@app.route('/get', methods=['GET'])
def get():
    if sql_connect('localhost',3306,'root','','robo_com'):
        get_result = sql_select_get()
        return {'input time': get_result[0],
                            'number': get_result[1],
                            'value': get_result[2],
                            'remark': get_result[3]}, 200
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/get/robo_state', methods=['GET'])
def get_robo_state():
    if sql_connect('localhost',3306,'root','','robo_com'):
        get_result = sql_select_get_robo_state()
        return {'robo_state': get_result[0],}, 200
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put', methods=['PUT'])
def putInput():
    insertValues = request.get_json()
    value=insertValues['value']
    remark=insertValues['remark']
    if sql_connect('localhost',3306,'root','','robo_com'):
        try:
            sql_insert(value,remark)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put/x1/<int:id>', methods=['PUT'])
def putx1Input(id):
    if sql_connect('localhost',3306,'root','','robo_com'):
        try:
            sql_insert(value = id,remark = 'None')
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put/robo_state/<int:value>', methods=['PUT'])
def putrobo_state(value):
    if sql_connect('localhost',3306,'root','','robo_com'):
        try:
            sql_updata_robo_state(value)
            get_result = sql_select_get_robo_state()
            return {'robo_state': get_result[0],}, 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put/ip/<string:ip>', methods=['PUT'])
def putip(ip):
    if sql_connect('localhost',3306,'root','','robo_com'):
        try:
            sql_insert_ip(value = ip)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/jpg', methods=['POST'])
def upload_file():

    if request.method == 'POST':

        f = request.files.get('files')
        if f is None:
            return jsonify({"Status": "Error 0000", "Msg": "上傳失敗"})

        if not allow_file(f.filename):
            return jsonify({"Status": "Error 9999", "Msg": "檔案類型錯誤"})

        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        detect_value = model_detect(os.path.join(app.config['UPLOAD_FOLDER'])+'\\'+filename)
        if  detect_value != []:
            print(detect_value)
            if sql_connect('localhost',3306,'root','','robo_com'):
                try:
                    sql_insert_detect(detect_value[1],detect_value[0])
                    #return 'return : insert success', 200
                    return "Successful"
                except pymysql.Error as e:
                    return  'return : '+str(e), 400
            else:
                return 'return : SQL connect FAIL', 500
        else:
            return "Successful"

if __name__ == '__main__':
    app.run()
