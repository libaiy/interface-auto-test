# coding:utf-8
import requests
import json
from utils.logger import logger

logger = logger
class RunMain():


    # 定义一个方法，传入需要的参数url和data
    def send_post(self, url, header, data):
        # 参数必须按照url、 header、data顺序传入
        res = requests.post(url, headers=header, data=data, verify=False)
        return res

    def send_get(self, url, header, data):
        result = requests.get(url=url, headers=header, data=data)
        res = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2)
        return res

    # 定义一个run_main函数，通过传过来的method来进行不同的get或post请求
    def run_main(self, method, url=None, header=None, data=None):
        result = None
        if method == 'post':
            result = self.send_post(url, header, data)
            logger.info("\t\t请求返回码：" + str(result))
        elif method == 'get':
            result = self.send_get(url, header, data)
            logger.info("\t\t请求返回码：" + str(result))
        else:
            print("method值错误！！！")
            logger.info("\t\tmethod值错误！！！")
        return result


# 验证我们写的请求是否正确
if __name__ == '__main__':
    result = RunMain().run_main('post', 'http://127.0.0.1:8888/login', 'name=xiaoming&pwd=')
    print(result)