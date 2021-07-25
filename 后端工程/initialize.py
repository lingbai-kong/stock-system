# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 13:34:19 2021

@author: 孔令百
"""
import MySQLdb
import tushare as ts
import time
ts.set_token('1e2e19b9955c1e035264d840da4f4bdebb2842f0b4c9b10661646b2e')
pro=ts.pro_api()
stocklist=pro.stock_basic(list_status='L',fields='ts_code,symbol,name,market,industry,area')
def StockTable():
    introduction=pro.stock_company(fields='ts_code,introduction')
    Stock=[]
    for i in range(len(stocklist['ts_code'])):
        ts_code=stocklist['ts_code'][i]
        msg=''
        for msgindex in range(len(introduction['ts_code'])):
            if introduction['ts_code'][msgindex]==ts_code:
                msg=introduction['introduction'][msgindex]
                break
        single_stock=[stocklist['ts_code'][i],stocklist['name'][i],msg,stocklist['market'][i],stocklist['industry'][i],stocklist['area'][i]]
        Stock.append(single_stock)
    
    db=MySQLdb.connect('localhost','root','','stock',charset='utf8')
    cursor=db.cursor()
    
    for item in Stock:
        sql = f"""INSERT INTO stock(Sid,Sname,Smsg,Skind,Sindustry,Sarea)
             VALUES ('{item[0]}','{item[1]}','{item[2]}','{item[3]}','{item[4]}','{item[5]}')"""
        try:
           # 执行sql语句
           cursor.execute(sql)
           # 提交到数据库执行
           db.commit()
        except:
           # Rollback in case there is any error
           db.rollback()
    db.close()
def KlineTable():
    db=MySQLdb.connect('localhost','root','','stock',charset='utf8')
    cursor=db.cursor()
    
    Kline=[]
    for i in range(len(stocklist['ts_code'])):
        print(str(100*i/len(stocklist['ts_code']))+'%')
        ts_code=stocklist['ts_code'][i]
        data=pro.daily(ts_code=ts_code,start_date='20210101',fields='ts_code,trade_date,open,high,low,close,pre_close,vol,amount')
        for j in range(len(data['ts_code'])):
            single_Kline=[data['ts_code'][j],data['trade_date'][j],data['close'][j],data['high'][j],data['low'][j],data['open'][j],data['pre_close'][j],data['vol'][j],data['amount'][j]]
            Kline.append(single_Kline)
        for item in Kline:
            sql = f"""INSERT INTO kline(K_Sid,Kdate,Kclose,Khigh,Klow,Kopen,Kpre,Kvol,Kamount)
                 VALUES ('{item[0]}','{item[1]}','{item[2]}','{item[3]}','{item[4]}','{item[5]}','{item[6]}','{item[7]}','{item[8]}')"""
            try:
               # 执行sql语句
               cursor.execute(sql)
               # 提交到数据库执行
               db.commit()
            except:
               # Rollback in case there is any error
               db.rollback()
        Kline.clear()
    db.close()
def updateKlineTable():
    db=MySQLdb.connect('localhost','root','','stock',charset='utf8')
    cursor=db.cursor()
    
    sql="""SELECT max(Kdate)
            FROM kline;"""
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()
    newday=cursor.fetchone()[0]+1
    cal=pro.trade_cal(exchange='',start_date=str(newday))
    for i in range(len(cal)):
        if cal['is_open'][i]==1:
            newday=cal['cal_date'][i]
            break
    Kline=[]
    for i in range(len(stocklist['ts_code'])):
        time.sleep(0.1)
        print(str(100*i/len(stocklist['ts_code']))[0:4]+'%')
        ts_code=stocklist['ts_code'][i]
        data=pro.daily(ts_code=ts_code,start_date=str(newday),end_date=str(newday),fields='ts_code,trade_date,open,high,low,close,pre_close,vol,amount')
        for j in range(len(data['ts_code'])):
            single_Kline=[data['ts_code'][j],data['trade_date'][j],data['close'][j],data['high'][j],data['low'][j],data['open'][j],data['pre_close'][j],data['vol'][j],data['amount'][j]]
            Kline.append(single_Kline)
        for item in Kline:
            sql = f"""INSERT INTO kline(K_Sid,Kdate,Kclose,Khigh,Klow,Kopen,Kpre,Kvol,Kamount)
                  VALUES ('{item[0]}','{item[1]}','{item[2]}','{item[3]}','{item[4]}','{item[5]}','{item[6]}','{item[7]}','{item[8]}')"""
            try:
                # 执行sql语句
                cursor.execute(sql)
                # 提交到数据库执行
                db.commit()
            except:
                # Rollback in case there is any error
                db.rollback()
        Kline.clear()
    db.close()
if __name__ == '__main__':
    #StockTable()
    #KlineTable()
    updateKlineTable()