import numpy as np
import pymysql
import os
import pathlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

SRC_PATH = pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,'jpg_save')

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if sql_connect('localhost',3304,'root','','robo_com'):
        try:
            sql_insert(value,remark)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/get', methods=['GET'])
def get():
    if sql_connect('localhost',3304,'root','','robo_com'):
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
    if sql_connect('localhost',3304,'root','','robo_com'):
        try:
            sql_insert(value,remark)
            return 'return : insert success', 200
        except pymysql.Error as e:
            return  'return : '+str(e), 400
    else:
        return 'return : SQL connect FAIL', 500

@app.route('/put/x1/<int:id>', methods=['PUT'])
def putx1Input(id):
    if sql_connect('localhost',3304,'root','','robo_com'):
        try:
            sql_insert(value = id,remark = 'None')
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
            return jsonify({"Status": "Error 0000", "Msg": "没有上传图片，请重新上传!"})

        if not allow_file(f.filename):
            return jsonify({"Status": "Error 9999", "Msg": "文件格式不支持，仅支持如下图片格式:'png', 'jpg', 'bmp'。"})

        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return "Successful"

if __name__ == '__main__':
    app.run()