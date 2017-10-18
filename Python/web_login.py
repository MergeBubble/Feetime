#-*- coding:utf-8 -*-
import random
import Send_email
from bottle import *
from gevent import monkey;monkey.patch_all()
import gevent
code_db={}
database={}
information={}
global old
@route('/')#登陆主页面
def login():
    return template('login.html')
@route('/<subpath:path>')  #文件的获取
def server_static(subpath):
    print subpath
    return static_file(subpath,root='view')
@route('/checklogin',method='post')  #验证是否正确
def do_login():
    print 1
   # return template('login')
    password=request.POST.get('password')
    User_ = request.POST.get('email')
    print User_ ,password
    if database.get(User_) == password :
        print 'success'
        #return template('info',**information[User_])
        return template('personal.html')
    else:
        redirect('/?error')
@route('/userRegister',method='post')   #注册事件
def do_register():
    print 1
    Email = request.POST.get('email')
    Username = request.POST.get('username')
    password = request.POST.get('password')
    repassword = request.POST.get('repassword')
    print Email,Username,password,repassword
    if Email.split("@")[1]!= "zju.edu.cn":
        redirect('/register1.html?error')
    else:

        if database.has_key(Username):
            redirect('/register1.html?error')
        else:
            if password == repassword:
                database[Username]=password
                print 'Create success'
                global old
                old = Username
                #发送邮件 以检验
                xrange=random.randrange(9999)
                print "%04d"%xrange
                y = Send_email.Send_code()
                y.Send(Email,"%04d"%xrange)
                code_db[Email]="%04d"%xrange
                print code_db[Email]
                redirect(redirect('/register1.html?next'))
                #return template('xxxx.html')
            else:
                redirect('/register1.html?error1')


@route('/check_code',method='post')
def check_code():
    global old
    Email = request.POST.get('email')
    code  = request.POST.get('code')
    if code_db[Email] == code:
        return template('xxxx.html')
    else:
        del database[old]




@route('/yan',method='post')
def get():
    global old
    Mail = request.POST.get('Email')
    major =  request.POST.get('Major')
    Add = 'ZJU campus'
    Intro = 'Hello,I\'m '+ request.POST.get('Name')
    QQ =  request.POST.get('QQ')
    data ={
        'imge':'lx.jpg',
        'Intro':Intro,
        'Add':Add,
        'major':major,
        'QQ':QQ,
        'Mail':Mail
    }
    information[old] = data
    print data
    #return template('info',**data)
    return template("personal.html")
run(host='localhost',port=80,server='gevent')