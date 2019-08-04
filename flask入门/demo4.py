# -*- coding：utf-8 -*-
# time ：2019/8/4 11:48
# author: 毛利

import flask

html_txt = """
<!DOCTYPE html>
<html>
    <body>
        <h2>收到GET请求</h2>
        <a href='/get_info'>获取会话信息</a>
    </body>
</html>
"""

app = flask.Flask(__name__)

@app.route('/set_info/<name>')
def set_cks(name):
    name = name if name else 'anonymous'
    flask.session['name'] = name
    return html_txt

@app.route('/get_info')
def get_cks():
    name = 'name' in flask.session and flask.session['name']
    if name:
        return '获取的会话信息是:' + name
    else:
        return '没有相应会话信息。'

if __name__ == '__main__':
    app.secret_key = 'dfadff#$#5dgfddgssgfgsfgr4$T^%^'
    app.run(debug=True)