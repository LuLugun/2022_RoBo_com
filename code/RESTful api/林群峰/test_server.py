import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
x1 ,x2 ,x3 = 0 ,0 ,0
@app.route('/post', methods=['POST'])
def postInput():
    global x1 ,x2 ,x3
    insertValues = request.get_json()
    x1=insertValues['number_of_people']
    x2=insertValues['length']
    x3=insertValues['wait']

    return jsonify({'number_of_people': str(x1) , 'length' : str(x2) , 'wait' : str(x3)})

@app.route('/get_json', methods=['GET'])
def get_json():
    return jsonify({'number_of_people': str(x1) , 'length' : str(x2) , 'wait' : str(x3)})

@app.route('/get_number_of_people', methods=['GET'])
def get_number_of_people():
    return str(x1)

@app.route('/get_length', methods=['GET'])
def get_length():
    return str(x2)

@app.route('/get_wait', methods=['GET'])
def get_wait():
    return str(x3)

@app.route('/put', methods=['PUT'])
def putInput():
    global x1 ,x2 ,x3
    insertValues = request.get_json()
    x1=insertValues['number_of_people']
    x2=insertValues['length']
    x3=insertValues['wait']
    return 'PUT success'
@app.route('/put/x1/<int:id>', methods=['PUT'])
def putx1Input(id):
    global x1
    x1=id
    return 'x1 revise success'
@app.route('/put/x2/<int:id>', methods=['PUT'])
def putx2Input(id):
    global x2
    x2=id
    return 'x2 revise success'
@app.route('/put/x3/<int:id>', methods=['PUT'])
def putx3Input(id):
    global x3
    x3=id
    return 'x3 revise success'

@app.route('/post_jpg',methods = ['POST'])
def postjpg():
    get_jpg = request.files['file']
    file_name = get_jpg.filename
    if get_jpg:
        get_jpg.save(file_name)
        return 'save'
if __name__ == '__main__':
    app.run()
