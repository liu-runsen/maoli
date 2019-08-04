# -*- coding：utf-8 -*-
# time ：2019/8/4 11:58
# author: 毛利

import flask

app = flask.Flask(__name__)

@app.route('/')
def helo():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)