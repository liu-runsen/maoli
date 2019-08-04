# -*- coding：utf-8 -*-
# time ：2019/8/4 11:32
# author: 毛利


import flask

html_txt = """
<!DOCTYPE html>
<html>
    <body>
        <h2>收到GET请求</h2>
        <form method='post'>
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
        return '收到POST请求，我是Flask!'

if __name__ == '__main__':
    app.run()
