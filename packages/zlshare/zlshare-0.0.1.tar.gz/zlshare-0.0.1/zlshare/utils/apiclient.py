# -*- coding:utf-8 -*-
import json
import random
import requests
import six


class Response(object):
    def __init__(self, url, **kwargs):
        self.url = url
        self.ok = kwargs.get("ok")
        self.content = kwargs.get("content")
        self.save = kwargs.get("save")

    @property
    def text(self):
        if hasattr(self, '_text') and self._text:
            return self._text
        if not self.content:
            return u''
        if isinstance(self.content, six.text_type):
            return self.content
        content = self.content.decode('utf-8', 'replace')
        self._text = content
        return content

    @property
    def json(self):
        """Returns the json-encoded content of the response, if any."""
        if hasattr(self, '_json'):
            return self._json
        try:
            self._json = json.loads(self.text or self.content)
        except ValueError:
            self._json = None
        return self._json


class ApiClient(object):
    """
    调用http接口请求数据客户端
    """
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.182 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.183 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.184 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.185 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.186 Safari/537.36",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENTS)
    }

    def crawl(self, url, **kwargs):
        """
        请求Api方法
        :param url:
        :param kwargs:
        :return:Response对象
                属性:
        """
        method = kwargs.get("method", "GET")
        method = method.lower()
        if kwargs.has_key("method"):
            kwargs.pop("method")
        req_kwargs = {}
        if kwargs.has_key("data"):
            method = "post"
            req_kwargs["data"] = kwargs.get("data")
            kwargs.pop("data")
        elif kwargs.has_key("json"):
            method = "post"
            req_kwargs["json"] = kwargs.get("json")
            kwargs.pop("json")
        ret = requests.request(method=method, url=url, headers=self.headers, **req_kwargs)
        response = Response(url=url, ok=ret.status_code == 200, text=ret.text, content=ret.content, **kwargs)
        return response


if __name__ == '__main__':
    apiClient = ApiClient()
    url = "http://7dacb781.zealink.com/API/Stock"
    # print apiClient.crawl(url="http://7dacb781cache.zealink.com/cache/symbollist/shsz.json").url
    post_data = {
        "symbol": ["600869.sh"],
        "field": ["symbol", "name", "increase", "price", "open", "high", "low", "yclose", "vol", "amount",
                  "exchangerate", "pe", "pb", "marketvalue", "flowmarketvalue"]
    }
    print apiClient.crawl(url=url, json=post_data).json
