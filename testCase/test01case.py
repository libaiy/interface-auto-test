# coding:utf-8
import json
import unittest
import paramunittest
from utils import getUrlParams
from utils import readExcel
from utils import operateConfig
from utils import configHttp
from utils import logger


url = getUrlParams.GetUrlParams().get_Url()# 调用我们的geturlParams获取我们拼接的URL
login_xls = readExcel.ReadExcel().get_xls('userCase.xlsx', 'login')
log = logger.logger

@paramunittest.parametrized(*login_xls)
class testUserLogin(unittest.TestCase):


    def setParameters(self, case_num, case_name, path, query, method, code, msg):
        """
        set params
        :param case_num
        :param case_name:
        :param path
        :param query
        :param method
        :param code
        :param msg
        :return:
        """
        self.case_num = str(case_num)
        self.case_name = str(case_name)
        self.path = str(path)
        self.query = str(query)
        self.method = str(method)
        self.code = int(code)
        self.msg = str(msg)

    def description(self):
        """
        test report description
        :return:
        """
        print("测试用户名密码登录相关用例")

    def setUp(self):
        log.info("********************测试用例：test01case_%s********************"%self.case_name)
        log.info("\t测试开始前准备...")
        print("\n测试test01case开始前准备。\n")

    def test01case(self):
        log.info("\t测试进行中...")
        self.checkResult()

    def tearDown(self):
        log.info("\t测试结束，输出log完结。")
        print("\n测试test01case结束，输出log完结。")

    def checkResult(self):# 断言
        """
        check test result
        :return:
        """
        log.info("\t\t测试接口：%s" % self.path)
        log.info("\t\t测试数据：%s" % self.query)
        web_url = url + self.path
        header = {'Content-Type': 'application/json', 'charset': 'UTF-8'}
        # 根据Excel中的method调用run_main来进行requests请求，并拿到响应
        info = configHttp.RunMain().run_main(self.method, web_url, header, self.query)
        rev_code = json.loads(info.text).get('code') # 获取自定义响应码
        rev_msg = json.loads(info.text).get('msg')
        log.info("\t\t响应码：")
        log.info("\t\t\t接收响应码：%s" % rev_code)
        log.info("\t\t\t期望响应码：%s" % self.code)
        log.info("\t\t响应信息：")
        log.info("\t\t\t接收响应信息：%s" % rev_msg)
        log.info("\t\t\t期望响应信息：%s" % self.msg)
        if self.case_name == u'成功登陆':# 如果case_name是login
            # 判断响应码
            self.assertEqual(rev_code, self.code)
            # 判断响应消息
            self.assertEqual(rev_msg, self.msg)
            # 登陆成功后，保存登陆信息至配置文件
            result = json.loads(info.text).get('result')
            phone_num = result.get('phone_num')
            user_token = result.get('token')
            uid = result.get('uid')
            user_dict = {
                "phone_num" : phone_num,
                "user_token" : user_token,
                "uid" : str(uid)
            }
            operateconfig = operateConfig.OperateConfig("user.ini")
            for k, v in user_dict.items():
                operateconfig.set_section("User", k, v)
        if self.case_name == u'密码错误':# 同上
            # 判断响应码
            self.assertEqual(rev_code, self.code)
            # 判断响应消息
            self.assertEqual(rev_msg, self.msg)
        if self.case_name == u'密码为空':# 同上
            # 判断响应码
            self.assertEqual(rev_code, self.code)
            # 判断响应消息
            self.assertEqual(rev_msg, self.msg)

