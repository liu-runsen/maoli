# -*- coding：utf-8 -*-
# time ：2019/8/4 11:40
# author: 毛利

import flask

html_txt = """
<!DOCTYPE html>
<html>
    <body>
        <h2>收到GET请求</h2>
        <form method='post'>
        <input type='text' name='name' placeholder='请输入你的姓名' />
        <input type='submit' value='发送POST请求' />
        </form>
    </body>
</html>
"""

app = flask.Flask(__name__)

@app.route('/hello',methods=['GET','POST'])
def helo():
    if flask.request.method == 'GET':
        return html_txt
    else:
        name = 'name' in flask.request.form and flask.request.form['name']
        if name:
            return '你是：' + name + '!'
        else:
            return '你没有输入姓名！'

if __name__ == '__main__':
    app.run(debug=True)