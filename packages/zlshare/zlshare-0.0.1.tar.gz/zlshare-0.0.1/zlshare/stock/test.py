# -*- coding:utf-8 -*-
import json
from unittest import TestCase

from zlshare.stock import trading
import datetime
#
# str = "{} {}".format(20190101, 710)
# dt = datetime.datetime.strptime(str, '%Y%m%d %H%M')
#
# a = trading.get_hist_data('600768.sh', start='2019-01-01', ktype="5")
# print(a.head())
#
#
# class TestGet_hist_data(TestCase):
#     def test_get_hist_data(self):
#         self.fail()


import requests

data = {
    "symbol": [ "600000.sh",  "000001.sz",  "000158.sz",  "000001.sh" ],
    "field": [  "symbol", "price","name","vol","increase","buy","sell","deal","minute"]
}
url="http://7dacb781.zealink.com/API/Stock"
resp = requests.post(url=url,json=data).json()
print resp

json.loads()