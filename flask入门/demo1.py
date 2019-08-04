# -*- coding：utf-8 -*-
# time ：2019/8/4 11:37
# author: 毛利

import  flask
app = flask.Flask(__name__)

@app.route('/hello/<name>')
def hello(name):
    return '你好,{}'.format(name) + '!'

if __name__ == '__main__':
    app.run()