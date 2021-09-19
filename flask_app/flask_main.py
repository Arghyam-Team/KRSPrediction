from typing import Text
from flask import Flask, send_file
from os.path import join
app = Flask(__name__)

@app.route('/files/<folder>/<sub_folder>/<file_name>')
def sendFile(folder: Text, sub_folder: Text, file_name: Text):
    try:
        return send_file(join("..","ChatbotWidget-main", folder, sub_folder, file_name))
    except:
        return ""


@app.route('/files/<folder>/<sub_folder>/<file_name>/<sub_file_name>')
def sendFile2(folder: Text, sub_folder: Text, file_name: Text, sub_file_name):
    try:
        return send_file(join("..","ChatbotWidget-main", folder, sub_folder, file_name, sub_file_name))
    except:
        return ""
if __name__ == '__main__':
    app.run(debug = False)