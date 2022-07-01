from flask import request, Flask, jsonify
import os
import pathlib
from matplotlib import pyplot as plt
from werkzeug.utils import secure_filename

SRC_PATH = pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH)


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查文件后缀名是否是图片文件

def allow_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':


        # 使用request上传文件，其中‘file'表示前端表单的Key值；也可以使用request.files['file']

        f = request.files.get('files')


        # 判断是否上传成功

        if f is None:

            return jsonify({"Status": "Error 0000", "Msg": "没有上传图片，请重新上传!"})


        # 检查文件后缀名是否是图片文件

        if not allow_file(f.filename):

            return jsonify({"Status": "Error 9999", "Msg": "文件格式不支持，仅支持如下图片格式:'png', 'jpg', 'bmp'。"})


        # 使用plt将图片读入为数组

        np_img = plt.imread(f)
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 对图片进行处理

        # Your code


    return "Successful"







if __name__ == '__main__':

    app.run()