#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import netifaces
import requests
from requests_toolbelt import SourceAddressAdapter


class SourceAddressRequests(object):
    def __init__(self):
        self.session = requests.session()
        self.ips = []

    @staticmethod
    def get_local_ips():
        """获取本机所有ip"""
        local_ips = []
        info = psutil.net_if_addrs()
        for interface in netifaces.interfaces():
            for link in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                # 去掉本地回路，去掉docker的ip
                if link['addr'] != '127.0.0.1':
                    local_ips.append(item[1])
        # 去掉原始ip
        local_ips = local_ips[1:]
        print("本机ip数量：", len(local_ips))
        return local_ips

    def adapter_requests(self):
        """随机绑定一个本机ip"""
        bind_address = random.choice(self.ips)
        print("请求ip：", bind_address)
        new_source = SourceAddressAdapter(bind_address)
        self.session.mount('http://', new_source)
        self.session.mount('https://', new_source)

    def test_requests(self):
        """测试请求"""
        url = "http://httpbin.org/get"
        response = self.session.get(url=url)
        origin = response.json()["origin"]
        print("检测到ip：", origin)

    def main(self):
        self.ips = self.get_local_ips()
        for i in range(5):
            print("第{}次请求".format(i + 1))
            self.adapter_requests()
            self.test_requests()


if __name__ == '__main__':
    test = SourceAddressRequests()
    test.main()
