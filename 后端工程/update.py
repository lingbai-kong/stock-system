# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 16:58:04 2021

@author: 孔令百
"""

from initialize import updateKlineTable as KLupdate
from Kshape_W import Kshape as KSupdate
from LSTM import update as LSTMupdate

def job():
    print("开始更新数据库")
    KLupdate()
    KSupdate()
    LSTMupdate()
    print("数据库更新完成")

if __name__ == '__main__':
    job()
    # from apscheduler.schedulers.blocking import BlockingScheduler
    # # BlockingScheduler
    # scheduler = BlockingScheduler()
    # scheduler.add_job(job, 'cron', day_of_week='1-5', hour=0, minute=30)
    # scheduler.start()