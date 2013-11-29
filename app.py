# -*- coding: utf-8 -*-

from flask import Flask, render_template, jsonify, url_for
import os
import commands
import datetime

app = Flask(__name__)

def yukkuri_wav(word):
    wav_file = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.wav'
    wav_file_path = './static/' + wav_file
    os.system('./yukkuri/AquesTalkPi -v f2 -o %s %s' % (wav_file_path, word.encode('utf-8')))
    return wav_file

@app.route("/")
def hello():
    wav_files = commands.getoutput('ls ./static')
    wav_list = wav_files.split()
    return render_template('index.html', **locals())

@app.route("/yukkuri/<word>")
def echo_yukkuri(word):
    wav_file = yukkuri_wav(word)
    return render_template('yukkuri.html', **locals())

@app.route("/yukkuri/api/<word>")
def yukkuri_api(word):
    wav_file = yukkuri_wav(word)
    return jsonify(wav=url_for('static', filename=wav_file),
                    word=word.encode('utf-8'))

if __name__ == "__main__":
    app.debug = True
    app.run()
