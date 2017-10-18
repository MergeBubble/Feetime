#-*- coding=utf-8 -*-
from bottle import *
#定义上传路径
message_total={}
comment={}
num = 0
now =0
@route('/')
def upload():
    return template("main.html")
@route('/', method ="post")
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

@route('/<subpath:path>')
def server_static(subpath):
    print subpath
    return static_file(subpath,root='view')
run(host='localhost', port=8080)