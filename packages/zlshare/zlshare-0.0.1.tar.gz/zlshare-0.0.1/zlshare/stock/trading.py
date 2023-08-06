# -*- coding:utf-8 -*-
"""
交易数据接口
Created on 2019/01/21
@author: luqy
@group : zealink
@contact: luqy@zealink.com
"""
from __future__ import division
from zlshare.stock import vars
import time, datetime, json
from zlshare.utils import netbase
from zlshare.utils import apiclient
import pandas as pd
import logbook

log = logbook.Logger("stock")


def get_hist_data(code=None, start=None, end=None,
                  ktype='D', retry_count=3,
                  pause=0.001):
    """
        获取个股历史交易记录
    Parameters
    ------
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取到API所提供的最早日期数据
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取到最近一个交易日数据
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          属性:日期 ，开盘价， 最高价， 收盘价， 最低价， 成交量， 价格变动 ，涨跌幅，5日均价，10日均价，20日均价，5日均量，10日均量，20日均量，换手率
    """
    dtstart = int('19700101') if start is None else int(start.replace('-', ''))
    dtend = int(datetime.datetime.now().strftime('%Y%m%d')) if end is None else int(end.replace('-', ''))
    if ktype in vars.K_LABELS:
        period = vars.K_LABELS[ktype]
        postdata = {
            "symbol": code,
            "count": 10000,
            "period": period
        }
        for _ in range(retry_count):
            try:
                res = netbase.Client(vars.K_URL, postdata)
                js = json.loads(res.gvalue())
                if js['code'] != 0:
                    raise "api[{}] error.code={}".format(vars.K_URL, js['code'])
            except Exception as e:
                log.warning(str(e))
                time.sleep(pause)
            else:
                df = pd.DataFrame(data=js['data'],
                                  columns=['date', 'preclose', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
                df['price_change'] = df.close - df.preclose
                df['p_change'] = (df.close - df.preclose) * 100.0 / df.preclose
                # 均价，均量
                for ma in [5, 10, 20]:
                    df['ma' + str(ma)] = df['close'].rolling(ma).mean()
                    df['v_ma' + str(ma)] = df['volume'].rolling(ma).mean()
                df = df.drop(columns=['preclose', 'turnover'])
                df = df[(df['date'] >= dtstart) & (df['date'] <= dtend)]
                df.date = df.date.apply(lambda x: datetime.datetime.strptime(str(x), '%Y%m%d'))
                df = df.set_index('date').sort_index(ascending=False)
                return df
        raise "net work error"
    elif ktype in vars.K_MIN_LABELS:
        period = vars.K_MIN_LABELS[ktype]
        postdata = {
            "symbol": code,
            "count": 10000,
            "period": period
        }
        for _ in range(retry_count):
            try:
                res = netbase.Client(vars.K_MIN_URL, postdata)
                js = json.loads(res.gvalue())
                if js['code'] != 0:
                    raise "api[{}] error.code={}".format(vars.K_URL, js['code'])
            except Exception as e:
                log.warning(str(e))
                time.sleep(pause)
            else:
                df = pd.DataFrame(data=js['data'],
                                  columns=['date', 'preclose', 'open', 'high', 'low', 'close', 'volume', 'turnover',
                                           'time'])
                df['price_change'] = df.close - df.preclose
                df['p_change'] = (df.close - df.preclose) * 100.0 / df.preclose
                # 均价，均量
                for ma in [5, 10, 20]:
                    df['ma' + str(ma)] = df['close'].rolling(ma).mean()
                    df['v_ma' + str(ma)] = df['volume'].rolling(ma).mean()
                df = df[(df['date'] >= dtstart) & (df['date'] <= dtend)]
                df.date = df.apply(
                    lambda row: datetime.datetime.strptime("{} {}".format(int(row['date']), int(row['time'])),
                                                           '%Y%m%d %H%M'), axis=1)
                df = df.drop(columns=['preclose', 'turnover', 'time'])
                df = df.set_index('date').sort_index(ascending=False)
                return df
        raise "net work error"
    else:
        raise "unknow ktype = {}".format(ktype)

def get_stock_basics(type='EQA'):
    """
    获取股票列表
    :param retry_count:
    :param type: EQA,IDX
    :return:
    """
    apiClient = apiclient.ApiClient()
    data = apiClient.crawl(url=vars.STK_CODE_LIST_URL).json
    data_list = data.get("symbollist")
    code_list = []
    for item in data_list:
        if type is None or item[2]==type:
            code_list.append(item)
    df = pd.DataFrame(data=code_list,
                      columns=['code', 'name', 'type'])
    return df.set_index('code')

def get_today_all(retry_count=3):
    """
    一次性获取当前交易所有股票的行情数据（如果是节假日，即为上一交易日，结果显示速度取决于网速）
    :return:
        DataFrame:
            属性:code: 代码,
                name: 名称,
                price:现价，
                open:开盘价，
                high:最高价，
                low:最低价
                preclose:昨日收盘价
                volume:成交量
                amount:成交金额
                changepercent:涨跌幅，
                turnover:换手率
                pe:市盈率
                pb:市净率
                marketvalue:总市值
                flowmarketvalue:流通市值
    """
    pause = 0.01

    post_data = {
        "plate":["CNA.ci"],
        "start": 0,
        "end":5000,
        "filterstop":1,
        "field":["symbol","name","increase","price","open","high","low","yclose","vol","amount","exchangerate","pe","pb","marketvalue","flowmarketvalue"]
    }
    for _ in range(retry_count):
        try:
            res = netbase.Client(vars.STK_SNAPSHOT_URL, post_data)
            js = json.loads(res.gvalue())
            if js['code'] != 0:
                raise Exception("api[{api}] error.code={code},msg={message}".format(api=vars.STK_SNAPSHOT_URL, code=str(js['code']),message=js['message'].encode("utf8")))
            data_list = js["stock"]
            df = pd.DataFrame(data=data_list,columns=["symbol","name","increase","price","open","high","low","yclose","vol","amount","exchangerate","pe","pb","marketvalue","flowmarketvalue"])
            df = df.loc[(df['price'] >0)]
            df.rename(columns={"symbol":"code","yclose":"preclose","vol":"volume","exchangerate":"trunover","increase":"changepercent"},inplace=True)
            return df
        except Exception as e:
            print str(e)
            log.warning(str(e))
            time.sleep(pause)
    return None


def get_tick_data(code=None, date=None, retry_count=3, pause=0.001):
    """
    历史分笔,获取个股以往交易历史的分笔数据明细
    :param code: string
                    股票代码 eg.600153
    :param date:string
                    日期,格式 YYYY-MM-DD eg.2018-12-12
    :param retry_count:int
                    重试次数，默认为3，如遇网络问题重复执行的次数
    :param pause:float
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    :return:DataFrame
            属性:time：时间
                price：成交价格
                change：价格变动
                volume：成交手
                amount：成交金额(元)
                type：买卖类型【买盘、卖盘、中性盘】
    """
    pass


def get_realtime_quotes(code=None, retry_count=3, pause=0.001):
    """
        获取实时交易数据 getting real time quotes data
       用于跟踪交易情况（本次执行的结果-上一次执行的数据）
    Parameters
    ------
        symbols : string, array-like object (list, tuple, Series).

    return
    -------
        DataFrame 实时交易数据
              属性:0：name，股票名字
            1：open，今日开盘价
            2：pre_close，昨日收盘价
            3：price，当前价格
            4：high，今日最高价
            5：low，今日最低价
            6：bid，竞买价，即“买一”报价
            7：ask，竞卖价，即“卖一”报价
            8：volumn，成交量 maybe you need do volumn/100
            9：amount，成交金额（元 CNY）
            10：b1_v，委买一（笔数 bid volume）
            11：b1_p，委买一（价格 bid price）
            12：b2_v，“买二”
            13：b2_p，“买二”
            14：b3_v，“买三”
            15：b3_p，“买三”
            16：b4_v，“买四”
            17：b4_p，“买四”
            18：b5_v，“买五”
            19：b5_p，“买五”
            20：a1_v，委卖一（笔数 ask volume）
            21：a1_p，委卖一（价格 ask price）
            ...
            30：date，日期；
            31：time，时间；
    """
    pause = 0.001
    post_data = {
        "symbol":[code],
        "field": ["symbol","name", "open", "yclose", "price", "high", "low", "vol", "amount", "buy", "sell", "date", "time"]
    }

    for _ in range(retry_count):
        try:
            res = netbase.Client(vars.STK_SNAPSHOT_URL, post_data)
            js = json.loads(res.gvalue())
            if js['code'] != 0:
                raise Exception("api[{api}] error.code={code},msg={message}".format(api=vars.STK_SNAPSHOT_URL, code=str(js['code']),message=js['message'].encode("utf8")))
            data_list = js["stock"]
            buy = data_list[0].get("buy",None)
            sell = data_list[0].get("sell",None)
            ret_data_dict = data_list[0]
            for index, item in enumerate(buy):
                if index == 0:
                    bid = item.get("price")
                    ret_data_dict.setdefault("bid", bid)
                ret_data_dict.setdefault("b{num}_p".format(num=index + 1), item.get("price"))
                ret_data_dict.setdefault("b{num}_v".format(num=index + 1), item.get("vol"))

            for index, item in enumerate(sell):
                if index == 0:
                    ask = item.get("price")
                    ret_data_dict.setdefault("ask", ask)
                ret_data_dict.setdefault("a{num}_v".format(num=index + 1), item.get("price"))
                ret_data_dict.setdefault("a{num}_p".format(num=index + 1), item.get("vol"))

            ret_data_dict.pop("buy")
            ret_data_dict.pop("sell")
            ret_data_dict.pop("symbol")

            data_list = [ret_data_dict]
            df = pd.DataFrame(data=data_list,columns=["name","open","yclose","price","high","low","vol",
                                                      "amount","bid", "ask", "b1_v", "b1_p",
                                                      "b2_v", "b2_p","b3_v", "b3_p","b4_v", "b4_p",
                                                      "b5_v", "b5_p", "a1_v", "a1_p", "a2_v", "a2_p",
                                                      "a3_v", "a3_p", "a4_v", "a4_p",
                                                      "a5_v", "a5_p", "date", "time",])
            df.rename(columns={"yclose":"pre_close","vol":"volume"},inplace=True)
            return df
        except Exception as e:
            print str(e)
            log.warning(str(e))
            time.sleep(pause)
    return None


def get_today_ticks(code=None, retry_count=3, pause=0.001):
    """
    实时分笔，获取实时分笔数据，可以实时取得股票当前报价和成交信息
    :param code: string
                    股票代码 eg.600153
    :param retry_count:int
                    重试次数，默认为3，如遇网络问题重复执行的次数
    :param pause:float
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    :return:DataFrame
            属性:time：时间
                price：当前价格
                pchange:涨跌幅
                change：价格变动
                volume：成交手
                amount：成交金额(元)
                type：买卖类型【买盘、卖盘、中性盘】
    """
    if code is None:
        return  None

    post_data = {
        "symbol": [code],
        "field": ["symbol", "deal"]
    }
    for _ in range(retry_count):
        try:
            res = netbase.Client(vars.STK_SNAPSHOT_URL, post_data)
            js = json.loads(res.gvalue())
            if js['code'] != 0:
                raise Exception("api[{api}] error.code={code},msg={message}".format(api=vars.STK_SNAPSHOT_URL, code=str(js['code']),message=js['message'].encode("utf8")))
            data_list = js["stock"]
            if len(data_list)!=1 and (data_list[0].get('deal',None) is not None):
                return None
            deal = data_list[0].get('deal')
            df = pd.DataFrame(data=deal,columns=["vol", "price", "time", "amount"])
            return df
        except Exception as e:
            print str(e)
            log.warning(str(e))
            time.sleep(pause)
    pass


def get_index():
    """
    大盘指数行情列表，获取大盘指数实时行情列表
    :return:DataFrame
            属性:code:指数代码
                name:指数名称
                change:涨跌幅
                open:开盘点位
                preclose:昨日收盘点位
                close:收盘点位
                high:最高点位
                low:最低点位
                volume:成交量(手)
                amount:成交金额（亿元）
    """
    retry_count = 3
    pause = 0.01
    index_list = get_stock_basics(type="IDX")
    if not index_list:
        return None

    post_data = {
        "symbol":index_list,
        "field":["symbol","name","increase","price","open","high","low","yclose","vol","amount"]
    }
    for _ in range(retry_count):
        try:
            res = netbase.Client(vars.STK_SNAPSHOT_URL, post_data)
            js = json.loads(res.gvalue())
            if js['code'] != 0:
                raise Exception("api[{api}] error.code={code},msg={message}".format(api=vars.STK_SNAPSHOT_URL, code=str(js['code']),message=js['message'].encode("utf8")))
            data_list = js["stock"]
            df = pd.DataFrame(data=data_list,columns=["symbol","name","increase","price","open","high","low","yclose","vol","amount"])
            df.rename(columns={"symbol":"code","increase":'change',"yclose":"preclose","vol":"volume"},inplace=True)
            return df
        except Exception as e:
            print str(e)
            log.warning(str(e))
            time.sleep(pause)
    return None


def get_stk_dd(code=None, date=None, vol=400, retry_count=3, pause=0.001):
    """
    大单交易数据,获取大单交易数据，默认为大于等于400手
    :param code: string
                    股票代码 eg.600153
    :param date:string
                    交易日期,格式YYYY-MM-DD eg.2018-12-12
    :param retry_count:int
                    重试次数，默认为3，如遇网络问题重复执行的次数
    :param pause:float
                    重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    :return:DataFrame
            属性:code：代码
                name：名称
                time：时间
                price：当前价格
                volume：成交手
                preprice ：上一笔价格
                type：买卖类型【买盘、卖盘、中性盘】
    :return:
    """

def get_k_data(code=None, start='', end='',
                  ktype='D', autype='qfq',
                  index=False,
                  retry_count=3,
                  pause=0.001):
    """
    获取k线数据
    ---------
    Parameters:
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取上市首日
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
      autype:string
                  复权类型，qfq-前复权 hfq-后复权 None-不复权，默认为qfq
      ktype：string
                  数据类型，D=日k线 W=周 M=月 5=5分钟 15=15分钟 30=30分钟 60=60分钟，默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volume 成交量
          amount 成交额
          turnoverratio 换手率
          code 股票代码
    """
    dtstart = int('19700101') if start is None else int(start.replace('-', ''))
    dtend = int(datetime.datetime.now().strftime('%Y%m%d')) if end is None else int(end.replace('-', ''))
    if ktype in vars.K_LABELS:
        period = vars.K_LABELS[ktype]
        postdata = {
            "symbol": code,
            "count": 1000,
            "period": period
        }
        for _ in range(retry_count):
            try:
                res = netbase.Client(vars.K_URL, postdata)
                js = json.loads(res.gvalue())
                if js['code'] != 0:
                    raise "api[{}] error.code={}".format(vars.K_URL, js['code'])
            except Exception as e:
                log.warning(str(e))
                time.sleep(pause)
            else:
                df = pd.DataFrame(data=js['data'],
                                  columns=['date', 'preclose', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
                df = df.drop(columns=['preclose', 'turnover'])
                df = df[(df['date'] >= dtstart) & (df['date'] <= dtend)]
                df.date = df.date.apply(lambda x: str(x))
                #df = df.set_index('date').sort_index(ascending=False)
                return df
        raise SystemError("code={} net work error".format(code))
    elif ktype in vars.K_MIN_LABELS:
        period = vars.K_MIN_LABELS[ktype]
        postdata = {
            "symbol": code,
            "count": 10000,
            "period": period
        }
        for _ in range(retry_count):
            try:
                res = netbase.Client(vars.K_MIN_URL, postdata)
                js = json.loads(res.gvalue())
                if js['code'] != 0:
                    raise "api[{}] error.code={}".format(vars.K_URL, js['code'])
            except Exception as e:
                log.warning(str(e))
                time.sleep(pause)
            else:
                df = pd.DataFrame(data=js['data'],
                                  columns=['date', 'preclose', 'open', 'high', 'low', 'close', 'volume', 'turnover',
                                           'time'])
                df = df[(df['date'] >= dtstart) & (df['date'] <= dtend)]
                df.date = df.apply(
                    lambda row: datetime.datetime.strptime("{} {}".format(int(row['date']), int(row['time'])),
                                                           '%Y-%m-%d %H:%M'), axis=1)
                df = df.drop(columns=['preclose', 'turnover', 'time'])
                #df = df.set_index('date').sort_index(ascending=False)
                return df
        raise SystemError("code={} net work error".format(code))
    else:
        raise SystemError("code={} unknow ktype = {}".format(code,ktype))


if __name__ == '__main__':
    # import tushare as ts
    # pro = ts.pro_api(token="b71cbc849e0ba4b48a7f09fb1bfc762d2a39c3a9edf59a74294358b3")
    # data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # print data
    df = get_today_ticks(code="000001.sz")
    print df