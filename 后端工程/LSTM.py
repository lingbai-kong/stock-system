import MySQLdb
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import pickle
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Flatten, Conv1D, AveragePooling1D
from math import sqrt

def getStockList(db):
    cursor=db.cursor()
    sql="""SELECT Sid
            FROM stock;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    return all_data

def getStockPrice(db,sid):
    cursor=db.cursor()
    sql=f"""SELECT K_Sid,Kdate,Kopen,Khigh,Klow,Kclose,Kvol
            FROM kline
            WHERE K_Sid='{sid}'
            ORDER BY Kdate;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    return all_data

#使用talib库函数构造行情指标
def taAnalysis(input_arrays):
    #Overlap Studies
    upper,middle,lower=ta.BBANDS(input_arrays['close'],matype=ta.MA_Type.T3)
    ma=ta.MA(input_arrays['close'],matype=0)
    ht=ta.HT_TRENDLINE(input_arrays['close'])
    midpoint=ta.MIDPOINT(input_arrays['close'],timeperiod=14)
    midpirce=ta.MIDPRICE(input_arrays['high'],input_arrays['low'],timeperiod=14)
    sar=ta.SAR(input_arrays['high'],input_arrays['low'],acceleration=0.1,maximum=0.1)
    OSlist={
        'upper':upper,
        'middle':middle,
        'lower':lower,
        'ma':ma,
        'ht':ht,
        'midpoint':midpoint,
        'midpirce':midpirce,
        'sar':sar
    }
    #Momentum Indicator
    macd,macdsignal,macdhist=ta.MACD(input_arrays['close'],fastperiod=12,slowperiod=26,signalperiod=9)
    slowk,slowd=ta.STOCH(input_arrays['high'],input_arrays['low'],input_arrays['close'],fastk_period=5,slowk_period=3,slowk_matype=0,slowd_period=3,slowd_matype=0)
    MIlist={
        'macd':macd,
        'macdsignal':macdsignal,
        'macdhist':macdhist,
        'slowk':slowk,
        'slowd':slowd
    }
    #Pattern Recognition
    cdl2crows=ta.CDL2CROWS(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdl3crows=ta.CDL3BLACKCROWS(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdl3inside=ta.CDL3INSIDE(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdl3linestrike=ta.CDL3LINESTRIKE(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdl3outside=ta.CDL3OUTSIDE(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdl3starsinsouth=ta.CDL3STARSINSOUTH(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdl3whitesoldiers=ta.CDL3WHITESOLDIERS(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdlabandonedbaby=ta.CDLABANDONEDBABY(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdladvanceblock=ta.CDLADVANCEBLOCK(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdlbelthold=ta.CDLBELTHOLD(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    cdlbreakaway=ta.CDLBREAKAWAY(input_arrays['open'],input_arrays['high'],input_arrays['low'],input_arrays['close'])
    PRlist={
        'cdl2crows':cdl2crows,
        'cdl3crows':cdl3crows,
        'cdl3inside':cdl3inside,
        'cdl3linestrike':cdl3linestrike,
        'cdl3outside':cdl3outside,
        'cdl3starsinsouth':cdl3starsinsouth,
        'cdl3whitesoldiers':cdl3whitesoldiers,
        'cdlabandonedbaby':cdlabandonedbaby,
        'cdladvanceblock':cdladvanceblock,
        'cdlbelthold':cdlbelthold,
        'cdlbreakaway':cdlbreakaway
    }
    return OSlist,MIlist,PRlist

#数据清洗
def featureEngineering(data,OSlist,MIlist,PRlist,timesteps=3):
    timesteps=timesteps+1
    length=len(data['close'])
    original=[]       
    #将各项特征序列拼接为一整块二维向量
    for i in range(length):
        original.append([])
        for key,value in data.items():
            if key!='trade_date' and key!='open':          
                original[-1].append(value[i])
        for key,value in OSlist.items():
            original[-1].append(value[i])
        for key,value in MIlist.items():
            original[-1].append(value[i])
        for key,value in PRlist.items():
            original[-1].append(value[i])
    #数据规范化，构造数据集
    dataX,dataY=[],[]
    for i in range(length-timesteps+1):
        adata=original[i:(i+timesteps)]
        if np.any(np.isnan(np.array(adata))):
            continue
        bdata=MinMaxScaler(feature_range=(0, 1)).fit_transform(adata)
        dataX.append(bdata[0:len(bdata)-1])
        dataY.append(bdata[-1][0])
        #date.append(data['trade_date'][i+timesteps-1])
    return dataX,dataY

def genDataSet(timesteps):
    db=MySQLdb.connect('localhost','root','','stock',charset='utf8')
    sids=getStockList(db)
    dataset=[]
    labelset=[]
    for sid in sids:
        stock_data=getStockPrice(db,sid[0])
        data_dict={
            'trade_date':np.array([x[1] for x in stock_data]),
            'close':np.array([x[5] for x in stock_data]),
            'open':np.array([x[2] for x in stock_data]),
            'high':np.array([x[3] for x in stock_data]),
            'low':np.array([x[4] for x in stock_data]),
            'vol':np.array([x[6] for x in stock_data])
        }
        if len(data_dict['close'])==0:
            continue
        OSlist,MIlist,PRlist=taAnalysis(data_dict)
        dataX,dataY=featureEngineering(data_dict, OSlist, MIlist, PRlist, timesteps)
        dataset.extend(dataX)
        labelset.extend(dataY)
    db.close()
    return dataset,labelset

def getRecommendList(db):
    cursor=db.cursor()
    sql="""SELECT R_Sid
            FROM recommend;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    all_data=cursor.fetchall() 
    return all_data

#数据清洗
def APP_featureEngineering(data,OSlist,MIlist,PRlist,timesteps=3):
    length=len(data['close'])
    original=[]       
    #将各项特征序列拼接为一整块二维向量
    for i in range(length):
        original.append([])
        for key,value in data.items():
            if key!='trade_date' and key!='open':          
                original[-1].append(value[i])
        for key,value in OSlist.items():
            original[-1].append(value[i])
        for key,value in MIlist.items():
            original[-1].append(value[i])
        for key,value in PRlist.items():
            original[-1].append(value[i])
    #数据规范化，构造数据集
    adata=original[length-timesteps:length]
    maxclose=np.amax(adata, axis=0)[0]
    minclose=np.amin(adata, axis=0)[0]
    rate=[maxclose,minclose]
    if np.any(np.isnan(np.array(adata))):
        return
    bdata=MinMaxScaler(feature_range=(0, 1)).fit_transform(adata)
    return bdata,rate

def APP_getDataSet(timesteps):
    db=MySQLdb.connect('localhost','root','','stock',charset='utf8')
    sids=getRecommendList(db)
    dataset=[]
    rateset=[]
    for sid in sids:
        stock_data=getStockPrice(db,sid[0])
        data_dict={
            'trade_date':np.array([x[1] for x in stock_data]),
            'close':np.array([x[5] for x in stock_data]),
            'open':np.array([x[2] for x in stock_data]),
            'high':np.array([x[3] for x in stock_data]),
            'low':np.array([x[4] for x in stock_data]),
            'vol':np.array([x[6] for x in stock_data])
        }
        if len(data_dict['close'])==0:
            continue
        OSlist,MIlist,PRlist=taAnalysis(data_dict)
        data,rate=APP_featureEngineering(data_dict, OSlist, MIlist, PRlist, timesteps)
        dataset.append(data)
        rateset.append(rate)
    db.close()
    return dataset,rateset
#模型训练
def train(dataX,dataY):
    train_X=np.array(dataX)
    train_Y=np.array(dataY)
    
    model=Sequential()
    '''
    首先构建三层LSTM神经网络，主要的可调参数为神经元个数，
    神经元个数偏少将无法提取完整的数据特征，个数过多则容易
    出现过拟合。经过反复测试我选择200作为隐层的神经元个数。
    为了进一步防止过拟合，在每一层LSTM之间加入了Dropout
    层，随机断开神经元的连接，抛弃阈值设定为0.2。
    '''
    model.add(LSTM(units=200,return_sequences=True,input_shape=(train_X.shape[1],train_X.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=200,return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=200,return_sequences=True))
    model.add(Dropout(0.2))
    '''
    之后构建两层一维卷积层，卷积核大小各为256个，卷积核大
    小为3，因为训练过程中涉及到较多的参数，所以选取Relu激
    活函数，对过拟合进行控制，在每一次卷积后还加入了池化层，
    对卷积结果下采样，对特征进行压缩，去除冗余信息。
    '''
    model.add(Conv1D(filters=256, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(AveragePooling1D(pool_size=2, strides=1))
    model.add(Dropout(0.2))
    
    model.add(Conv1D(filters=256, kernel_size=3, activation='relu', strides=1, padding='same'))
    model.add(AveragePooling1D(pool_size=2, strides=1))
    model.add(Dropout(0.2))  
    
    '''
    最后加入了4层全连接层，综合各组特征，输出预测结果。
    '''
    model.add(Flatten())
    model.add(Dense(units=256,activation='relu'))
    model.add(Dropout(0.2))
    
    model.add(Dense(units=256,activation='relu'))
    model.add(Dropout(0.2))  
    
    model.add(Dense(units=128,activation='relu'))
    model.add(Dropout(0.2))  
    
    model.add(Dense(units=1,activation='relu')) 
    '''
    损失函数为mae均方误差，优化器采用Adam。Adam算法是
    一种自适应学习率的方法，它利用梯度的一阶矩阵估计和
    二阶矩阵估计动态调整每个参数的学习率。学习率参数设
    定为0.001。
    '''
    model.compile(loss='mae', optimizer=tf.keras.optimizers.Adam(0.001))
    
    checkpoint_save_path = "./checkpoint/lstmconv_stock.ckpt"
    if os.path.exists(checkpoint_save_path):
        model.load_weights(checkpoint_save_path)
        # 若成功加载前面保存的参数，输出下列信息
        print("checkpoint_loaded")
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                     save_weights_only=True,
                                                     save_best_only=True,
                                                     monitor='val_loss')
    '''
    模型的epochs为100次，batch_size设定为32，shuffle
    置为True在训练过程中随机打乱输入样本的顺序，使用回调
    函数ModelCheckpoint，将在每个epoch后保存性能最好的
    模型到指定文件中。模型训练时的评价指标为mae均方误差
    '''
    history = model.fit(train_X, 
                        train_Y, 
                        epochs=40, 
                        batch_size=32, 
                        validation_split=0.2, 
                        verbose=1, 
                        shuffle=True,
                        callbacks=[cp_callback])
    model.summary()
    
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend()
    plt.show()   
    return model
#模型使用与预测
def apply(model,timesteps):
    testX,rate=APP_getDataSet(timesteps)
    testY = model.predict(np.array(testX))
    for i in range(len(testY)):
        testY[i]=testY[i]*(rate[i][0]-rate[i][1])+rate[i][1]
    return testY
def update():
    timesteps=9
    model=load_model('LSTM模型')
    predict=apply(model,timesteps)
    db=MySQLdb.connect('localhost','root','','stock',charset='utf8')
    sids=getRecommendList(db)
    for i in range(len(sids)):
        sql=f"""UPDATE recommend
                SET Rpr={predict[i][0]}
                WHERE R_Sid='{sids[i][0]}'"""
        cursor=db.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
    db.close()
    
#完成整个实验过程
def function():
    #可调参数：
    ###################
    #时间序列长度
    timesteps=9
    #训练集占所有数据集的比例
    train_rate=0.98
    #是否制作新的数据集，如果选择否则使用保存的数据集，当更新数据集时间后要制作新的数据集
    newdataset=False
    #是否使用现有模型进行预测，如果要重新训练模型，该参数应该置为True
    usemodel=True
    ################### 
    if not usemodel:
        dataset=[]
        labelset=[]
        if newdataset:
            dataset,labelset=genDataSet(timesteps)
            try:
                f=open('dataset.dst','wb')
                tup=(dataset,labelset)
                pickle.dump(tup,f)
                f.close()
            except IOError as e:
                print("error:caculate.write(data,indexdata,flow)",e)
        else:
            try:
                f=open('dataset.dst','rb')
                tup=pickle.load(f)
                (dataset,labelset)=tup
            except IOError as e:
                print("error:caculate.read(dataset.dst)",e)
        
        train_size=int(train_rate*len(labelset))
        trainX=dataset[:train_size]
        trainY=labelset[:train_size]
        testX=dataset[train_size:]
        testY=labelset[train_size:]
        model=train(trainX,trainY)
        model.save('LSTM模型')
    else:
        model=load_model('LSTM模型')
    predict=apply(model,timesteps)
    print(predict[0][0])
if __name__ == '__main__':
    #function()
    update()
