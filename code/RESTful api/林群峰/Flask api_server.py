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

    return jsonify({'return': str(x1)+','+str(x2)+','+str(x3)})

@app.route('/get', methods=['GET'])
def get():
    return jsonify({'return': str(x1)+','+str(x2)+','+str(x3)})

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
if __name__ == '__main__':
    app.run()