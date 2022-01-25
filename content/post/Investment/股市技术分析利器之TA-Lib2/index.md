---
title: "股市技术分析利器之TA-Lib（二）"
date: 2021-12-22T10:36:04+08:00
description: ""
image: ""
categories: [Investment]
tags: [python,量化]
---

> 不进行研究的投资，就像打扑克从来不看牌一样，必然失败——彼得·林奇

**引言**

**TA-Lib**，全称“Technical Analysis Library”, 即技术分析库，是Python金融量化的高级库，涵盖了150多种股票、期货交易软件中常用的技术分析指标，如MACD、RSI、KDJ、动量指标、布林带等等。TA-Lib可分为10个子板块：Overlap Studies(重叠指标)，Momentum Indicators(动量指标)，Volume Indicators(交易量指标)，Cycle Indicators(周期指标)，Price Transform(价格变换)，Volatility Indicators(波动率指标)，Pattern Recognition(模式识别)，Statistic Functions(统计函数)，Math Transform(数学变换)和Math Operators(数学运算)，见下图。[【手把手教你】股市技术分析利器之TA-Lib（一）](https://mp.weixin.qq.com/s/nLOCNim0XRjqs_2iLDMO8Q)，主要探讨了重叠指标的相关原理与Python实现，本文将着重介绍TA-Lib中强大的数学运算、数学变换、统计函数、价格变换、周期指标和波动率指标函数及其应用实例。

![](1640140226-a59efd9b4d4b6dcb2ccc4cc87c519550.jpg)

**安装与使用**

**安装**：在cmd上使用“pip install talib”命令一般会报错，正确安装方法是，进入[https://www.lfd.uci.edu/~gohlke/pythonlibs/](https://www.lfd.uci.edu/~gohlke/pythonlibs/)，下拉选择TA\_Lib-0.4.17-cp37-cp37m-win\_amd64.whl（win系统64位，python3.7版本，根据自己系统和python版本选择相应的安装包），将下载包放在当前工作路径中，然后在Anaconda Prompt（或windows的cmd）里面输入命令：pip install TA\_Lib-0.4.17-cp27-cp27m-win\_amd64.whl。

**使用**：import talib as ta

## 01 Price Transform 价格转换

TA-Lib模块中提供的价格转换函数有四个，主要用于计算开盘价、收盘价、最高价、最低价之间的均值，具体如下表所示。

![](1640140226-6f5ab91131d96a07774a7f879cbec4b3.jpg)

```python
#先引入后面可能用到的包（package）

import pandas as pd  
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline   

#正常显示画图时出现的中文和负号
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False

#引入TA-Lib库
import talib as ta

#获取交易数据用于示例分析
import tushare as ts
def get_data(code,start='2015-01-01'):
    df=ts.get_k_data(code,start)
    df.index=pd.to_datetime(df.date)
    df=df.sort_index()
    return df

#获取上证指数收盘价、最高、最低价格
df=get_data('sh')[['open','close','high','low']]

#开盘价，最高价，最低价，收盘价的均值
df['average']=ta.AVGPRICE(df.open,df.high,df.low,df.close)
#最高价，最低价的均值
df['median']=ta.MEDPRICE(df.high,df.low)
#最高价，最低价，收盘价的均值
df['typical']=ta.TYPPRICE(df.high,df.low,df.close)
#最高价，最低价，收盘价的加权
df['weight']=ta.WCLPRICE(df.high,df.low,df.close)
df.head()

df.loc['2019-01-08':,['close','average','median','typical','weight']].plot(figsize=(12,6))
ax = plt.gca()  
ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none')   
plt.title('上证指数及其价格转换',fontsize=15)
plt.xlabel('')
plt.show()
```

![](1640140226-e58cec635b814c1b6e215df67701a243.jpg)

## 02 Cycle Indicator Functions周期指标函数

**希尔伯特变换**(Hilbert Transform)是积分变换中的一种，在信号处理领域得到了广泛的应用，而在工程中常用于窄带数字信号的处理。金融市场的波动是非周期、不规律的，但只要存在波动，就可以通过希尔伯特变换寻找其“周期性”。对于股价走势，一般可将其分解为：长期趋势、中短期周期性波动和噪声。在去除长期趋势的情况下，可以利用希尔伯特变换对中短期的周期性波动进行分析。关于希尔伯特变换原理及其在短线择时中的应用可参考广发证券金融工程专题报告《希尔伯特变换下的短线择时策略》（公众号**Python金融量化**后台回复：“**希尔伯特**”，获取免费下载地址）

![](1640140226-14a85b10f327398b521f3d445db97c4a.jpg)

```python
df=get_data('sh')[['open','close','high','low']]
df['dcperiod']=ta.HT_DCPERIOD(df.close)
df['dcphase']=ta.HT_DCPHASE(df.close)
df['inhpase'],df['quadrature']=ta.HT_PHASOR(df.close)
df['sine'],df['leadsine']=sine, leadsine = ta.HT_SINE(df.close)
df['trendmode']=ta.HT_TRENDMODE(df.close)

#将上述函数计算得到的结果进行可视化
df[['close','dcperiod','dcphase','inhpase','quadrature','sine','leadsine','trendmode']].plot(figsize=(20,18),
       subplots = True,layout=(4, 2))
plt.subplots_adjust(wspace=0,hspace=0.2)
```

上证指数走势及其周期变换

![](1640140226-0e49cb3b01f8518fe4c5cf1120c6786d.jpg)

## 03 Volatility Indicator Functions 波动率指标函数

当前交易日最高价与最低价差值，前一交易日收盘价与当前交易日最高价间的差值，前一交易日收盘价与当前交易日最低价的差值，这三者中的最大值为真实波幅。即真实波动幅度 = max(最大值,昨日收盘价) − min(最小值,昨日收盘价)，平均真实波动幅度等于真实波动幅度的N日指数移动平均数。波动幅度可以显示出**交易者的期望和热情**。波动幅度的急剧增加表示交易者在当天可能准备持续买进或卖出股票，波动幅度的减少则表示交易者对股市没有太大的兴趣。波动率指标可用于衡量价格的波动情况，辅助判断趋势改变的可能性，市场的交易氛围，也可以利用波动性指标来帮助**止损止盈**。

![](1640140226-10ea8af5080f8c0a1c45301f89c87a7e.jpg)

```python
df=get_data('sh')[['open','close','high','low']]
df['atr']=ta.ATR(df.high, df.low, df.close, timeperiod=14)
df['natr']=ta.NATR(df.high, df.low, df.close, timeperiod=14)
df['trange']=ta.TRANGE(df.high, df.low, df.close)
df.tail()
```

上证指数走势及波动率指标

![](1640140226-2d123dc0741f39aabeb1189c535bf7ba.jpg)

## 04 Math Operator Functions数学运算

TA-Lib提供了向量（数组）的加减乘除、在某个周期内求和、最大最小值及其索引等计算函数，注意与Numpy和Pandas数学运算函数的联系与区别，TA-Lib的向量计算功能类似于pandas的moving window（移动窗口），得到的是一个新的序列（不是某个值），具体如下表所示。

![](1640140226-9ff1e85a45187b9930c096fdd40d5a85.jpg)

```python
df=get_data('sh')[['open','close','high','low']]
#最高价与最低价之和
df['add']=ta.ADD(df.high,df.low)
#最高价与最低价之差
df['sub']=ta.SUB(df.high,df.low)
#最高价与最低价之乘
df['mult']=ta.MULT(df.high,df.low)
#最高价与最低价之除
df['div']=ta.DIV(df.high,df.low)
#收盘价的每30日移动求和
df['sum']=ta.SUM(df.close, timeperiod=30)
#收盘价的每30日内的最大最小值
df['min'], df['max'] = ta.MINMAX(df.close, timeperiod=30)
#收盘价的每30日内的最大最小值对应的索引值（第N行）
df['minidx'], df['maxidx'] = ta.MINMAXINDEX(df.close, timeperiod=30)
df.tail()

#将上述函数计算得到的结果进行可视化
df[['close','add','sub','mult','div','sum','min','max']].plot(figsize=(20,18),
       subplots = True,
       layout=(4, 2))
plt.subplots_adjust(wspace=0,hspace=0.2)
```

上证指数走势及数学运算

![](1640140226-ce9df6bc4a3197eb8f5d9c671428bc48.jpg)

## 05 Statistic Functions 统计学函数

TA-Lib提供了常用的基础统计学函数，基于时间序列移动窗口进行计算。注意TA-Lib的beta，示例中是求某只股票的最高价与最低价序列的移动beta值，默认时间周期为5日，而资本资产定价中一般是分析某只股票相对于市场（大盘指数）的波动情况。具体指标如下表所示。

![](1640140226-c19a40b6ff6b675627bf6948968be8dd.jpg)

```python
df=get_data('sh')[['open','close','high','low']]
#收盘价对时间t的线性回归预测值
df['linearreg']=ta.LINEARREG(df.close, timeperiod=14)
#时间序列预测值
df['tsf']=ta.TSF(df.close, timeperiod=14)
#画图
df.loc['2018-08-01':,['close','linearreg','tsf']].plot(figsize=(12,6))
```

![](1640140226-e5c1d880bc1b1bd6133a4305c2c22a6d.jpg)

```python
df['beta']=ta.BETA(df.high,df.low,timeperiod=5)
df['correl']=ta.CORREL(df.high, df.low, timeperiod=30)
df['stdev']=ta.STDDEV(df.close, timeperiod=5, nbdev=1)
#将上述函数计算得到的结果进行可视化
df[['close','beta','correl','stdev']].plot(figsize=(18,8),
       subplots = True,layout=(2, 2))
plt.subplots_adjust(wspace=0,hspace=0.2)
```

![](1640140226-8ad38c733963dec20b875bc6fa02ed59.jpg)

## 06 Math Transform Functions数学转换函数

TA-Lib提供了三角函数（正余弦、正余切、双曲）、取整、对数、平方根等数学转换函数，均是基于时间序列的向量变换。三角函数的应用比较复杂，可结合傅里叶变换和小波分析进行学习，此处不再详细展开。具体指标如下表所示。

![](1640140226-d18ff3ff239472c996020e800478b619.jpg)

```python
df=get_data('sh')[['open','close','high','low']]
df['sin']=ta.SIN(df.close)
df['cos']=ta.COS(df.close)
df['ln']=ta.LN(df.close)
#将上述函数计算得到的结果进行可视化
df[['close','sin','cos','ln']].plot(figsize=(18,8),
       subplots = True,layout=(2, 2))
plt.subplots_adjust(wspace=0,hspace=0.2)
```

![](1640140226-6b24a2f3f41e537fa3a93497f74bff9f.jpg)
