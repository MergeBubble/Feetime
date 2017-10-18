#-*- coding:utf-8 -*-
import random
import Send_email
from bottle import *
from gevent import monkey;monkey.patch_all()
import gevent
code_db={}
database={}
information={}
message_total={}
comment={}
num = 0
now =0
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
        return template('main.html')
        #redirect('/main')
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
    return template('main.html')



@route('/',method ="post")
def ajax():
    data={}
    global now
    global num
    type=request.POST.get('type')
    print type
    if type=="first_open":
        max_=max(message_total)
        now = max_
        for x in range(max_,max_-5,-1):
            print x
            if(message_total.has_key(x)):
                data[x]=message_total[x]
                now-=1
        return data
    if type == "more":
        temp = now
        for x in range(temp,temp-2,-1):
            print x
            if(message_total.has_key(x)):
                data[x]=message_total[x]
                now-=1
        return data
    if type=="send_message":
        message=request.POST.get('message')
        num +=1
        message_total[num]=message
        message_id =num
        print message_id
        data={"message_id":message_id,"message":message}
        return data
    if type =="comment":
        message_id=request.POST.get('message_id')
        print message_id

        print message_id
        comment.setdefault(int(message_id),["暂无评论"])
        data={"comment":comment[int(message_id)]}
        return data
    if type == "add_comment":
        message_id=request.POST.get('message_id')
        message=request.POST.get('message')
        if comment[int(message_id)][0]=="暂无评论":
            comment[int(message_id)][0] =message
        else:
            comment[int(message_id)].append(message)
        data={"add_comment":message}
        return data
run(host='localhost',port=80,server='gevent')