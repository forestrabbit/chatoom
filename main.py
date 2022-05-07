from bottle import *
from random import *
from datetime import datetime
from threading import *
import time

session = {}
application = {'msg': ''}

def clearSession():
    for k, v in session.items():
        if (datetime.now() - v['datetime']).hours > 1:
            session.pop(k)

def randomString(width = 50):
    astr = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    l = []
    for i in range(width):
        l.append(astr[int(random() * len(astr))])
    return ''.join(l)

@route('/', method = 'get')
def handler():
    return static_file('chatLogin.html', 'html')

@route('/', method = 'post')
def handler():
    userName = request.forms.get('userName')
    password = request.forms.get('password')
    if userName == 'xxx' and password == 'yyy':
        token = randomString()
        while token in session.keys():
            token = randomString()
        session[token] = {'userName': userName, 'password': password, 'datetime': datetime.now()}
        return token + ',/chat'
    else:
        return HTTPResponse('用户名或密码错误', 403)

@route('/chat')
def handler():
    if request.headers.get('Referer') == 'http://localhost:8080/':
        return static_file('chat.html', 'html')
    else:
        return '<h1>no permission to access here</h1>'

@route('/chat', method = 'post')
def handler():
    token = request.forms.get('token')
    if token in session.keys():
        session[token]['datetime'] = datetime.now()
        application['msg'] += session[token]['userName'] + '进入聊天室 ' + str(datetime.now()) + '<br />'
    else:
        return HTTPResponse('no permission to access here', 403)

@route('/msg', method = 'post')
def handler():
    token = request.forms.get('token')
    if token in session.keys():
        session[token]['datetime'] = datetime.now()
        return application['msg']
    else:
        return HTTPResponse('no permission to access here', 403)

@route('/send', method = 'post')
def handler():
    token = request.forms.get('token')
    if token in session.keys():
        session[token]['datetime'] = datetime.now()
        application['msg'] += session[token]['userName'] + '说：' + request.forms.get('msg') + ' at ' + str(datetime.now()) + '<br />'
    else:
        return HTTPResponse('no permission to access here', 403)

def main():
    run(host = 'localhost', port = 8080)

Thread(target = main).start()
while True:
    clearSession()
    time.sleep(3600)