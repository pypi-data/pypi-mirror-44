#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import urllib
import urllib2
import json
import datetime
import hashlib
import base64

API_HOST = "http://web7.umydata.com"
PRI_KEY = "Zealink25GiYmhM3PkJU9JN5ghu0EeVq"

class vtradectl(object):

    def __init__(self,user='', passwd='', api_host=API_HOST):
        self.api_host = api_host
        self.token = None
        self.user = user
        self.passwd = passwd

    def _http_data(self,uri, postdata):
        requrl = self.api_host + uri
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = "Basic {}".format(self.token)
        postdata_js = json.dumps(postdata)
        req = urllib2.Request(url=requrl, data = postdata_js, headers=headers)
        response = urllib2.urlopen(req)
        return json.loads(response.read())

    def _get_sign(self, params):
        items = params.items()
        items.sort()
        sortedparams = ["{}={}".format(key,value) for key, value in items]
        sortedparams.append("Key={}".format(PRI_KEY))
        #param = urllib.urlencode(sortedparams).encode('utf-8')
        #param += "&Key={}".format(PRI_KEY)
        param = '&'.join(sortedparams)
        sign = hashlib.md5(param).hexdigest()
        return sign.upper()

    def logon(self, user=None, passwd=None):
        self.user = user if user else self.user
        self.passwd = passwd if passwd else self.passwd
        md5passwd = hashlib.md5(self.passwd.encode('utf-8')).hexdigest()
        postdata = {
            "UserId":self.user,
            "Password":md5passwd
        }
        postdata['Sign'] = self._get_sign(postdata)
        response = self._http_data("/api/VT_Logon", postdata=postdata)
        if response['code'] == 0:
            self.token = response['token']
        else:
            msg = u"code={},msg={}".format(response['code'], response['message'])
            raise ValueError(msg.encode('utf8'))

    def buy(self, **params):
        """
        :param Symbol:  股票代码
        :param Name:    股票代码
        :param Price:    买入价格
        :param Vol:      买入笔数
        :param MaxCount:
        :param Policy:
        :return:
        """
        postdata = {
            "Symbol":"",
            "Name":"",
            "Price":"",
            "Vol":"",
            "MaxCount":"",
            "Policy":""
        }
        for key, value in params.items():
            postdata[key] = value
        params['Sign'] = self._get_sign(postdata)
        postdata["Price"] = float(postdata["Price"])
        response = self._http_data("/api/VT_Buy",postdata=params)
        if response['code'] == 0:
            return response['bookid']
        else:
            msg = u"code={},msg={}".format(response['code'], response['message'])
            raise ValueError(msg.encode('utf8'))

    def sell(self, **params):
        """"
        :param Symbol:  股票代码
        :param Name:    股票代码
        :param Price:    卖出价格
        :param Vol:      卖出笔数
        :param MaxCount:
        :param Policy:
        :return:
        """
        postdata = {
            "Symbol": "",
            "Name": "",
            "Price": "",
            "Vol": "",
            "MaxCount": "",
            "Policy": ""
        }
        for key, value in params.items():
            postdata[key] = value
        params['Sign'] = self._get_sign(postdata)
        postdata["Price"] = float(postdata["Price"])
        response = self._http_data("/api/VT_Sell",postdata=params)
        if response['code'] == 0:
            return response['bookid']
        else:
            msg = u"code={},msg={}".format(response['code'], response['message'])
            raise ValueError(msg.encode('utf8'))

    def cancel(self, bookid):
        postdata = { "BookId":bookid }
        postdata['Sign'] = self._get_sign(postdata)
        response = self._http_data("/api/VT_Canel", postdata=postdata)
        if response['code'] == 0:
            return response['bookid']
        else:
            msg = u"code={},msg={}".format(response['code'], response['message'])
            raise ValueError(msg.encode('utf8'))

    def order(self, dtstart, dtend):
        """
        查询委托订单信息
        :param dtstart:
        :param dtend:
        :return:
        """
        postdata = {
            "QueryDate": {
                "StartDate":int(dtstart) if isinstance(dtstart,str) or isinstance(dtstart,int) else int(dtstart.strftime("%Y%m%d")),
                "EndDate": int(dtend) if isinstance(dtend,str) or isinstance(dtend,int) else int(dtend.strftime("%Y%m%d"))
            },
            "Type":0
        }
        postdata['Sign'] = self._get_sign(postdata)
        response = self._http_data("/api/VT_Query", postdata=postdata)
        if response['code'] == 0:
            return response['entrust']
        else:
            msg = u"code={},msg={}".format(response['code'], response['message'])
            raise ValueError(msg.encode('utf8'))

    def deal(self, dtstart, dtend):
        """
        查询成交信息
        :param dtstart:
        :param dtend:
        :return:
        """
        postdata = {
            "QueryDate": {
                "StartDate":int(dtstart) if isinstance(dtstart,str) or isinstance(dtstart,int) else int(dtstart.strftime("%Y%m%d")),
                "EndDate": int(dtend) if isinstance(dtend,str) or isinstance(dtend,int) else int(dtend.strftime("%Y%m%d"))
            },
            "Type": 1
        }
        postdata['Sign'] = self._get_sign(postdata)
        response = self._http_data("/api/VT_Query", postdata=postdata)
        if response['code'] == 0:
            return response['deal']
        else:
            msg = u"code={},msg={}".format(response['code'], response['message'])
            raise ValueError(msg.encode('utf8'))

    def info(self, stock=True):
        """
        查询持仓信息
        :param stock: 是否返回股票持仓信息
        :return:
        """
        postdata = {
            "Stock": stock
        }
        postdata['Sign'] = self._get_sign(postdata)
        return self._http_data("/api/VT_User", postdata=postdata)

