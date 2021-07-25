# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 10:51:15 2021

@author: 孔令百
"""

from flask import Flask,request
import MySQLdb
import json
import hashlib
import time
import random
import string
from user import *
mysql_host='localhost'
app = Flask(__name__)
@app.route('/test')
def test():
    return '后端flask框架测试成功'
#获取K线数据
@app.route('/API/KLine2',methods=["POST"])
def get_Kline_history_data():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_list = data['data']
    request_data = request_list['Data']
    assert 'symbol' in request_data, 'there should be symbol inside this json data'
    assert 'count' in request_data, 'there should be count inside this json data'
    assert 'field' in request_data, 'there should be field inside this json data'
    symbol=request_data['symbol'].upper()
    count=request_data['count']
    field=request_data['field']
    
    sql = f"""SELECT Kdate,Kpre,Kopen,Khigh,Klow,Kclose,Kvol,Kamount
             FROM kline
             WHERE K_Sid='{symbol}'
             ORDER BY Kdate
             LIMIT 0,{count};"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    
    all_data=cursor.fetchall()
    response={}
    response['data']=all_data
    
    sql = f"""SELECT Sname
             FROM stock
             WHERE Sid='{symbol}';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    name=cursor.fetchone()[0]
    response['symbol']=request_data['symbol']
    response['name']=name
    db.close()
    return json.dumps(response,ensure_ascii=False)
#获取股票信息
@app.route('/API/message',methods=["POST"])
def get_stock_message():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'sid' in request_data, 'there should be sid inside this json data'
    sql=f"""SELECT Sname,Smsg,Skind,Sindustry,Sarea
            FROM stock
            WHERE Sid='{request_data['sid']}';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    one_data=cursor.fetchone() 
    response={}
    response['data']=one_data
    db.close()
    return json.dumps(response,ensure_ascii=False)
#获取沪深行情列表
@app.route('/API/HS_list',methods=["POST"])
def get_HS_list():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'Skind' in request_data, 'there should be Skind inside this json data'
    assert 'DataPos' in request_data, 'there should be DataPos inside this json data'
    assert 'RequestKind' in request_data, 'there should be RequestKind inside this json data'
    Skind=request_data['Skind']
    DataPos=request_data['DataPos']
    RequestKind=request_data['RequestKind']
    #print(DataPos)
    if RequestKind=='ADD':
        sql = f"""SELECT Sid,Sname,Kclose,100*(Kclose-Kpre)/Kpre as rate
                FROM (SELECT Sid,Sname
                	FROM stock
                	WHERE Skind='{Skind}'
                	) as a,
                	(SELECT K_Sid,Kclose,Kpre
                	FROM kline
                	WHERE Kdate=(SELECT max(Kdate)
                				FROM kline)
                	) as b
                WHERE a.Sid=b.K_Sid
                ORDER BY (Kclose-Kpre)/Kpre DESC
                LIMIT {DataPos},100;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    response={}
    response['data']=all_data
    db.close()
    return json.dumps(response,ensure_ascii=False)
#获取行业行情列表
@app.route('/API/HY_list',methods=["POST"])
def get_HY_list():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    sql = """SELECT Sindustry,100*(SUM(Kclose)-SUM(Kpre))/SUM(Kpre) as rate
            FROM (SELECT Sid,Sindustry
            	FROM stock
            	) as a,
            	(SELECT K_Sid,Kclose,Kpre
            	FROM kline
            	WHERE Kdate=(SELECT max(Kdate)
            				FROM kline)
            	) as b
            WHERE a.Sid=b.K_Sid
            GROUP BY Sindustry
            ORDER BY Sindustry DESC;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    response={}
    response['data']=all_data
    db.close
    return json.dumps(response,ensure_ascii=False)
#获取地区行情列表
@app.route('/API/DQ_list',methods=["POST"])
def get_DQ_list():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    sql = """SELECT Sarea,100*(SUM(Kclose)-SUM(Kpre))/SUM(Kpre) as rate
            FROM (SELECT Sid,Sarea
            	FROM stock
            	) as a,
            	(SELECT K_Sid,Kclose,Kpre
            	FROM kline
            	WHERE Kdate=(SELECT max(Kdate)
            				FROM kline)
            	) as b
            WHERE a.Sid=b.K_Sid
            GROUP BY Sarea
            ORDER BY Sarea DESC;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    response={}
    response['data']=all_data
    db.close
    return json.dumps(response,ensure_ascii=False)
#获取推荐行情列表
@app.route('/API/TJ_list',methods=["POST"])
def get_TJ_list():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    sql = """SELECT Sid,Kclose,Rpr,Sname
            FROM (SELECT Sid,Sname
            	FROM stock
                WHERE Sid IN(SELECT R_Sid 
                             FROM recommend)
            	) as a,
            	(SELECT K_Sid,Kclose
            	FROM kline
            	WHERE Kdate=(SELECT max(Kdate)
            				FROM kline)
                and K_Sid IN(SELECT R_Sid 
                             FROM recommend)
            	) as b,
                recommend as c
            WHERE a.Sid=c.R_Sid and b.K_Sid=c.R_Sid
            ORDER BY Rpr/Kclose DESC;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    response={}
    response['data']=all_data
    db.close
    return json.dumps(response,ensure_ascii=False)
#验证邮箱是否已经注册
@app.route('/user/ckemail/<email>',methods=['GET'])
def check_email(email):
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    sql=f"""SELECT Uid
            FROM user
            WHERE Uemail='{email}' and Ustatus='正常';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall()
    db.close()
    if len(all_data)==0:
        return 'SUCCESS'
    else:
        return 'FAIL'
#注册准用户发送验证码
@app.route('/user/auth',methods=['POST'])
def send_auth():
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'email' in request_data, 'there should be email inside this json data'
    assert 'pw' in request_data, 'there should be pw inside this json data'
    assert 'name' in request_data, 'there should be name inside this json data'
    assert 'pid' in request_data, 'there should be pid inside this json data'
    
    if check_email(request_data['email'])=='FAIL':
        return
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    new_uid=''
    while True:
        new_uid=generate_uid()
        sql=f"""SELECT Uid
            FROM user
            WHERE Uid='{new_uid}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        all_data=cursor.fetchall()
        if len(all_data)==0:
            break
    new_auth=generate_auth()
    
    sql=f"""DELETE FROM user
            WHERE Uemail='{request_data['email']}' and Ustatus='未注册';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    
    sql=f"""INSERT INTO user (Uid,Ukey,Ustatus,Upname,Upid,Uemail,Uauth)
            VALUES ('{new_uid}',MD5('{request_data['pw']}'),'未注册','{request_data['name']}','{request_data['pid']}','{request_data['email']}','{new_auth}');"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    auth_send(new_auth,request_data['email'])
    db.close()
    return 'OK'
#向已有用户发送验证码
@app.route('/user/reauth',methods=['POST'])
def send_reauth():
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'email' in request_data, 'there should be email inside this json data'
    if check_email(request_data['email'])=='SUCCESS':
        return
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    new_auth=generate_auth()
    
    sql=f"""UPDATE user
            SET Uauth='{new_auth}'
            WHERE Uemail='{request_data['email']}';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    auth_send(new_auth,request_data['email'])
    db.close()
    return 'OK'
#修改密码
@app.route('/user/changepw',methods=['POST'])
def change_pw():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'email' in request_data, 'there should be email inside this json data'
    assert 'pw' in request_data, 'there should be pw inside this json data'
    assert 'auth' in request_data, 'there should be auth inside this json data'
    sql=f"""SELECT Uid,Uauth
            FROM user
            WHERE Uemail='{request_data['email']}' and Ustatus='正常';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    one_data=cursor.fetchone() 
    
    uid=one_data[0]
    auth=one_data[1]
    
    msg=''
    if request_data['auth']==auth:
        sql=f"""UPDATE user
                SET Ukey=MD5('{request_data['pw']}')
                WHERE Uid='{uid}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='验证码不正确'
    db.close()
    return msg
#注册用户
@app.route('/user/register',methods=['POST'])
def register():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'email' in request_data, 'there should be email inside this json data'
    assert 'auth' in request_data, 'there should be auth inside this json data'
    
    sql=f"""SELECT Uid,Uauth
            FROM user
            WHERE Uemail='{request_data['email']}' and Ustatus='未注册';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    one_data=cursor.fetchone()
    
    uid=one_data[0]
    auth=one_data[1]
    msg=''
    if request_data['auth']==auth:
        sql=f"""UPDATE user
                SET Ustatus='正常'
                WHERE Uid='{uid}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
           
        sql=f"""INSERT INTO assert (A_Uid,Atotast,Astotast)
                VALUE ('{uid}',100000,100000);"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='验证码不正确'
    db.close()
    return msg
#用户登录
@app.route('/user/login',methods=['POST'])
def login():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'email' in request_data, 'there should be email inside this json data'
    assert 'pw' in request_data, 'there should be pw inside this json data'
    
    sql=f"""SELECT Uid,Ukey
            FROM user
            WHERE Uemail='{request_data['email']}' and Ustatus='正常';"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    one_data=cursor.fetchone()
    
    msg=''
    response={}
    if one_data==None:
        sql=f"""SELECT Mid,Mkey,Mgrade
            FROM manager
            WHERE Mid='{request_data['email']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        manager_data=cursor.fetchone()
        if manager_data==None:
            msg='该邮箱未注册账户'
        else:
            uid=manager_data[0]
            pw=manager_data[1]
            mgrade=manager_data[2]
            
            m=hashlib.md5()
            m.update(request_data['pw'].encode("utf8"))
            md5=m.hexdigest()
            if pw!=md5:
                msg='密码错误'
            else:
                if mgrade=='预备管理员':
                    msg='管理员权限尚未开通'
                elif mgrade=='正式管理员':
                    msg='OK'
                    response['kind']='normal'
                    response['uid']=uid
                    response['jwt']=generate_jwt(uid)
                elif mgrade=='超级管理员':
                    msg='OK'
                    response['kind']='super'
                    response['uid']=uid
                    response['jwt']=generate_jwt(uid)
                else:
                    msg='非法身份'
            
    else:
        uid=one_data[0]
        pw=one_data[1]
    
        m=hashlib.md5()
        m.update(request_data['pw'].encode("utf8"))
        md5=m.hexdigest()
        if pw!=md5:
            msg='密码错误'
        else:
            msg='OK'
            response['kind']='user'
            response['uid']=uid
            response['jwt']=generate_jwt(uid)
    response['msg']=msg
    db.close()
    return json.dumps(response,ensure_ascii=False)
#获取用户信息
@app.route('/user/message',methods=['POST'])
def get_user_message():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f"""SELECT Uid,Ustatus,Upname,Upid,Uemail
                FROM user
                WHERE Uid='{request_data['uid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        one_data=cursor.fetchone()
        response['msg']='OK'
        response['data']=one_data
    else:
        response['msg']='登录已过期，请重新登录'
    db.close()
    return json.dumps(response,ensure_ascii=False)
#添加自选股
@app.route('/user/select',methods=['POST'])
def select():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'sid' in request_data, 'there should be sid inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f"""INSERT INTO optional(O_Uid,O_Sid,Odate,Oprice)
            VALUES ('{request_data['uid']}','{request_data['sid']}',{request_data['date']},{request_data['price']});"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录'
    db.close()
    return msg
#获取自选股列表
@app.route('/user/ZX_list',methods=['POST'])
def get_ZX_list():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f"""SELECT Sid,Sname,Kclose,100*(Kclose-Kpre)/Kpre as rate,Odate,Oprice
                FROM (SELECT Sid,Sname,Odate,Oprice
                	FROM stock,optional
                	WHERE Sid=O_Sid and O_uid='{request_data['uid']}'
                	) as a,
                	(SELECT K_Sid,Kclose,Kpre
                	FROM kline
                	WHERE Kdate=(SELECT max(Kdate)
                				FROM kline)
                	) as b
                WHERE a.Sid=b.K_Sid
                ORDER BY (Kclose-Kpre)/Kpre DESC;"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        all_data=cursor.fetchall()
        response['msg']='OK'
        response['data']=all_data
    else:
        response['msg']='登录已过期，请重新登录'
    db.close()
    return json.dumps(response,ensure_ascii=False)
#删除自选股
@app.route('/user/ZX_remove',methods=['POST'])
def delete_ZX():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'sid' in request_data, 'there should be jwt inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f"""DELETE FROM optional
                WHERE O_Uid='{request_data['uid']}' AND O_Sid='{request_data['sid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录'
    db.close()
    return msg
#管理员申请
@app.route('/manager/apply',methods=['POST'])
def apply():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'name' in request_data, 'there should be name inside this json data'
    assert 'pw' in request_data, 'there should be pw inside this json data'
    assert 'telno' in request_data, 'there should be telno inside this json data'
    
    new_uid=''
    while True:
        new_uid=generate_uid()
        new_uid='#'+new_uid[1:]
        sql=f"""SELECT Mid
            FROM manager
            WHERE Mid='{new_uid}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        all_data=cursor.fetchall()
        if len(all_data)==0:
            break
    
    sql=f"""INSERT INTO manager (Mid,Mkey,Mname,Mgrade,Mtelno)
            VALUES ('{new_uid}',MD5('{request_data['pw']}'),'{request_data['name']}','预备管理员','{request_data['telno']}');"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    db.close()  
    return new_uid
#获取人员列表
@app.route('/manager/people',methods=['POST'])
def getPeopleList():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'kind' in request_data, 'there should be kind inside this json data'
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        if request_data['kind']=='super':
            sql="""SELECT Mid,Mname,Mgrade,Mtelno
                FROM manager
                WHERE Mgrade!='超级管理员';"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            all_data=cursor.fetchall() 
            response={}
            response['msg']='OK'
            response['data']=all_data
            return json.dumps(response,ensure_ascii=False)
        else:
            sql="""SELECT Uid,Upname,Ustatus,Uemail
                FROM user
                WHERE Ustatus!='未注册';"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            all_data=cursor.fetchall()
            response['msg']='OK'
            response['data']=all_data
    else:
        response['msg']='登录已过期，请重新登录'
    db.close()
    return json.dumps(response,ensure_ascii=False)
#更改管理员等级
@app.route('/manager/people/changeMGd',methods=['POST'])          
def changeMGd():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'opid' in request_data, 'there should be opid inside this json data'
    assert 'method' in request_data, 'there should be method inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=''
        if request_data['method']=='升级为正式管理员':
            sql=f"""UPDATE manager
                    SET Mgrade='正式管理员'
                    WHERE Mid='{request_data['opid']}';"""
        else:
            sql=f"""UPDATE manager
                    SET Mgrade='预备管理员'
                    WHERE Mid='{request_data['opid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录'  
    db.close()
    return msg
#删除管理员
@app.route('/manager/people/deleteM',methods=['POST'])  
def deleteM():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'opid' in request_data, 'there should be opid inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f'''DELETE FROM manager
                WHERE Mid='{request_data['opid']}';'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录'
    db.close()
    return msg
#管理员修改密码
@app.route('/manager/people/changePw',methods=['POST'])
def changePw():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'kind' in request_data, 'there should be kind inside this json data'
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'opid' in request_data, 'there should be opid inside this json data'
    assert 'newpw' in request_data, 'there should be newpw inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=''
        if request_data['kind']=='super':    
            sql=f'''UPDATE manager
                    SET Mkey=MD5('{request_data['newpw']}')
                    WHERE Mid='{request_data['opid']}';'''
        else:
            sql=f'''UPDATE user
                    SET Ukey=MD5('{request_data['newpw']}')
                    WHERE Uid='{request_data['opid']}';'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录'
    db.close()
    return msg
#更改用户状态
@app.route('/manager/people/changeUst',methods=['POST'])
def changeUst():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'opid' in request_data, 'there should be opid inside this json data'
    assert 'method' in request_data, 'there should be method inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=''
        if request_data['method']=='注销用户':
            sql=f"""UPDATE user
                    SET Ustatus='注销'
                    WHERE Uid='{request_data['opid']}';"""
        else:
            sql=f"""UPDATE user
                    SET Ustatus='正常'
                    WHERE Uid='{request_data['opid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录' 
    db.close()
    return msg
#获取管理员个人信息
@app.route('/manager/message',methods=['POST'])
def getManagerMsg():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f'''SELECT Mid,Mgrade,Mname,Mtelno
                FROM manager
                WHERE Mid='{request_data['uid']}';'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
           
        message=cursor.fetchone()
        response['msg']='OK'
        response['data']=message
    else:
        response['msg']='登录已过期，请重新登录'
    db.close()
    return json.dumps(response,ensure_ascii=False)
#更新管理员个人信息
@app.route('/manager/updateMsg',methods=['POST'])
def updateManagerMsg():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'name' in request_data, 'there should be name inside this json data'
    assert 'telno' in request_data, 'there should be telno inside this json data'
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f'''UPDATE manager
                SET Mname='{request_data['name']}',
                    Mtelno='{request_data['telno']}'
                WHERE Mid='{request_data['uid']}';'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        msg='OK'
    else:
        msg='登录已过期，请重新登录' 
    db.close()
    return msg
#获取资产信息
@app.route('/deal/assert_list',methods=['POST'])
def getAssert():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f'''SELECT Atotast,Astotast
            FROM assert
            WHERE A_Uid='{request_data['uid']}';'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
           
        message=cursor.fetchone()
        response['msg']='OK'
        response['data']=message
    else:
        response['msg']='登录已过期，请重新登录'
    db.close()
    return json.dumps(response,ensure_ascii=False)
#获取持仓信息
@app.route('/deal/position_list',methods=['POST'])
def getPosition():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f'''SELECT P_Sid,Pposition,Pcostprice,Sname,Kclose
            FROM position,stock,kline
            WHERE P_Uid='{request_data['uid']}' and
                Sid=P_Sid and
                Kdate=(SELECT max(Kdate) FROM kline) and
                K_Sid=P_Sid;'''
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
           
        message=cursor.fetchall()
        response['msg']='OK'
        response['data']=message
    else:
        response['msg']='登录已过期，请重新登录'
    db.close()
    return json.dumps(response,ensure_ascii=False)
#买入股票
@app.route('/deal/buy',methods=['POST'])
def buy():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'sid' in request_data, 'there should be sid inside this json data'
    assert 'vol' in request_data, 'there should be vol inside this json data'
    vol=request_data['vol']
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql = f"""SELECT Kclose
                FROM kline
                WHERE 
                    Kdate=(SELECT max(Kdate) FROM kline)
                    and
                    K_Sid='{request_data['sid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        price=cursor.fetchone()[0]
        
        sql = f"""SELECT Atotast
                FROM assert
                WHERE A_Uid='{request_data['uid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        totast=cursor.fetchone()[0]
        
        if float(vol)*price>totast:
            msg="账户可用资产不足！"
        else:
            sql = f"""UPDATE assert
                    SET Atotast={totast-float(vol)*price}
                    WHERE A_Uid='{request_data['uid']}'"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            sql = f"""SELECT Pposition,Pcostprice
                   FROM position
                   WHERE P_Uid='{request_data['uid']}' and
                       P_Sid='{request_data['sid']}';"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
            data=cursor.fetchone()
            new_position=[]
            if data==None:
                sql=f"""INSERT INTO position (P_Uid,P_Sid,Pposition,Pcostprice)
                        VALUES ('{request_data['uid']}','{request_data['sid']}',{vol},{price});"""
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
            else:
                old_position=data
                new_price=(float(old_position[0])*old_position[1]+float(vol)*price)/(float(old_position[0])+float(vol))
                new_position=[int(old_position[0])+int(vol),new_price]
                sql=f"""UPDATE position
                        SET Pposition={new_position[0]},
                            Pcostprice={new_position[1]}
                        WHERE P_Uid='{request_data['uid']}' and
                            P_Sid='{request_data['sid']}';"""
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
            str_list = [random.choice(string.digits+ string.ascii_letters) for i in range(14)]
            random_str = ''.join(str_list)
            Did=str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+random_str
            intdate=int(time.strftime("%Y%m%d", time.localtime()))
            sql=f"""INSERT INTO deal (Did,D_Uid,D_Sid,Ddate,Dprice,Damount,Dbusiness)
                    VALUES ('{Did}','{request_data['uid']}','{request_data['sid']}',{intdate},{price},{vol},'B');"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()        
            msg='OK'
    else:
        msg='登录已过期，请重新登录'
    db.close()
    return msg
#卖出股票
@app.route('/deal/sale',methods=['POST'])
def sale():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    assert 'sid' in request_data, 'there should be sid inside this json data'
    assert 'vol' in request_data, 'there should be vol inside this json data'
    vol=request_data['vol']
    msg=''
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql = f"""SELECT Kclose
                FROM kline
                WHERE 
                    Kdate=(SELECT max(Kdate) FROM kline)
                    and
                    K_Sid='{request_data['sid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        price=cursor.fetchone()[0]
        
        sql = f"""SELECT Atotast
                FROM assert
                WHERE A_Uid='{request_data['uid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        totast=cursor.fetchone()[0]
        
        sql = f"""SELECT Pposition,Pcostprice
                   FROM position
                   WHERE P_Uid='{request_data['uid']}' and
                       P_Sid='{request_data['sid']}';"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        data=cursor.fetchone()
        
        if data==None or int(vol)>int(data[0]):
            msg="股票持仓不足！"
        else:
            sql = f"""UPDATE assert
                    SET Atotast={totast+float(vol)*price}
                    WHERE A_Uid='{request_data['uid']}'"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
                
            new_position_num=int(data[0])-int(vol)
            if new_position_num==0:
                sql=f"""DELETE FROM position
                        WHERE P_Uid='{request_data['uid']}' and
                        P_Sid='{request_data['sid']}';"""
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
            else:
                sql=f"""UPDATE position
                        SET Pposition={new_position_num}
                        WHERE P_Uid='{request_data['uid']}' and
                            P_Sid='{request_data['sid']}';"""
                try:
                    # 执行sql语句
                    cursor.execute(sql)
                    # 提交到数据库执行
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
            str_list = [random.choice(string.digits+ string.ascii_letters) for i in range(14)]
            random_str = ''.join(str_list)
            Did=str(time.strftime("%Y%m%d%H%M%S", time.localtime()))+random_str
            intdate=int(time.strftime("%Y%m%d", time.localtime()))
            sql=f"""INSERT INTO deal (Did,D_Uid,D_Sid,Ddate,Dprice,Damount,Dbusiness)
                    VALUES ('{Did}','{request_data['uid']}','{request_data['sid']}',{intdate},{price},{vol},'S');"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()     
            msg='OK'
    else:
        msg='登录已过期，请重新登录'
    db.close()
    return msg
#获取交易明细
@app.route('/deal/detail',methods=['POST'])
def get_deal_detail():
    db=MySQLdb.connect(mysql_host,'root','','stock',charset='utf8')
    cursor=db.cursor()
    data = json.loads(request.get_data(as_text=True))
    request_data = data['data']
    assert 'uid' in request_data, 'there should be uid inside this json data'
    assert 'jwt' in request_data, 'there should be jwt inside this json data'
    response={}
    if request_data['uid']==check_jwt(request_data['jwt']):
        sql=f"""SELECT Did,D_Sid,Ddate,Dprice,Damount,Dbusiness
            FROM deal
            WHERE D_Uid='{request_data['uid']}'
            ORDER BY Did DESC;"""
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        data=cursor.fetchall()
        if data==None:
            response['data']=[]
        else:
            response['data']=data
        response['msg']='OK'
    else:
        response['msg']='登录已过期，请重新登录'
    return json.dumps(response,ensure_ascii=False)
if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8000) 
