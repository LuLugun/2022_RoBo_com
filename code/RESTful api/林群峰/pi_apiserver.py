import numpy as np
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def sql_connect(host,user,passwd,database):
    global db,cursor
    try:
        db=pymysql.connect(host=host,user=user,passwd=passwd,database=database)
        #os.system('cls')
        cursor=db.cursor()
        return True
    except pymysql.Error as e:
        print(str(e))
        return False

def sql_insert(value,remark):
    sql = '''INSERT INTO `api_test`(`value`, `remark`) VALUES ('%s','%s')'''%(value,remark)
    cursor.execute(sql)
    db.commit()
    
def sql_select_get():
    sql = '''SELECT * FROM `api_test` ORDER BY `input time` DESC LIMIT 1'''
    cursor.execute(sql)
    result=cursor.fetchall()
    return result[0]

@app.route('/post', methods=['POST'])
def postInput():
    insertValues = request.get_json()
    value=insertValues['value']
    remark=insertValues['remark']
    if sql_connect('localhost','pi','123456','pi'):
        try:
            sql_insert(value,remark)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/get', methods=['GET'])
def get():
    if sql_connect('localhost','pi','123456','pi'):
        get_result = sql_select_get()
        return {'input time': get_result[0],
                            'number': get_result[1],
                            'value': get_result[2],
                            'remark': get_result[3]}, 200
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put', methods=['PUT'])
def putInput():
    insertValues = request.get_json()
    value=insertValues['value']
    remark=insertValues['remark']
    if sql_connect('localhost','pi','123456','pi'):
        try:
            sql_insert(value,remark)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put/x1/<int:id>', methods=['PUT'])
def putx1Input(id):
    if sql_connect('localhost','pi','123456','pi'):
        try:
            sql_insert(value = id,remark = 'None')
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

if __name__ == '__main__':
    app.run()
