# -*- coding:utf-8 -*-
import sys
from zlshare.utils import vars as ct

K_LABELS = {'D': 0,'W': 1,'M': 2}
K_MIN_LABELS = {'1': 0,'5': 1,'15': 2,'60': 3}

K_URL = 'http://{}/API/KLine2'.format(ct.API_HTTP_URL)
K_MIN_URL = 'http://{}/API/KLine3'.format(ct.API_HTTP_URL)

#实时行情
STK_SNAPSHOT_URL = 'http://{domain}/API/Stock'.format(domain=ct.API_HTTP_URL)

#股票代码
STK_CODE_LIST_URL='http://{domain}/cache/symbollist/shsz.json'.format(domain=ct.CACHE_API_HTTP_URL)