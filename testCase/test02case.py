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
login_xls = readExcel.ReadExcel().get_xls('userCase.xlsx', 'vm')
log = logger.logger

@paramunittest.parametrized(*login_xls)
class testVMInfo(unittest.TestCase):
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
        print("测试获取虚拟机信息相关用例")

    def setUp(self):
        log.info("********************测试用例：test02case_%s********************" % self.case_name)
        log.info("\t测试开始前准备...")
        print("\n测试test02case开始前准备。\n")

    def test02case(self):
        log.info("\t测试进行中...")
        self.checkResult()

    def tearDown(self):
        log.info("\t测试结束，输出log完结。")
        print("\n测试test02case结束，输出log完结。")

    def checkResult(self):# 断言
        """
        check test result
        :return:
        """
        log.info("\t\t测试接口：%s" % self.path)
        log.info("\t\t测试数据：%s" % self.query)
        web_url = url + self.path
        operateconfig = operateConfig.OperateConfig("user.ini")
        uid = operateconfig.get_user("uid")
        token = operateconfig.get_user("user_token")
        header = {'Content-Type': 'application/json', 'X-CHAOS-TOKEN': token}
        data_dict = json.loads(self.query)
        data_dict["uid"] = uid
        data = json.dumps(data_dict)
        # 根据Excel中的method调用run_main来进行requests请求，并拿到响应
        info = configHttp.RunMain().run_main(self.method, web_url, header, data)
        rev_code = json.loads(info.text).get('code')  # 获取自定义响应码
        rev_msg = json.loads(info.text).get('msg')    # 获取自定义响应消息
        log.info("\t\t响应码：")
        log.info("\t\t\t接收响应码：%s" % rev_code)
        log.info("\t\t\t期望响应码：%s" % self.code)
        log.info("\t\t响应信息：")
        log.info("\t\t\t接收响应信息：%s" % rev_msg)
        log.info("\t\t\t期望响应信息：%s" % self.msg)
        # 断言
        if self.case_name == u'全部设备':
            # 判断响应码
            self.assertEqual(rev_code, self.code)
            # 判断响应信息
            self.assertEqual(rev_msg, self.msg)
            # 获取用户下虚拟机信息成功后，保存登陆信息至配置文件
            result = json.loads(info.text).get('result')
            # ws_token、vms
            ws_token = result.get('ws_token')
            vms_info = result.get('vms')
            new_vm_list = []
            need_vmoption = ["vm_id", "display_id", "is_owner"]
            for vm_dict in vms_info:
                new_vm_dict = {}
                for k, v in vm_dict.items():
                    if k in need_vmoption:
                        new_vm_dict[k] = v
                new_vm_list.append(new_vm_dict)
            vm_dict = {
                "ws_token" : ws_token,
                "vms" : str(new_vm_list)
            }
            for k, v in vm_dict.items():
                operateconfig.set_section("VM", k, v)
        if self.case_name == u'默认群组':# 同上
            # 判断响应码
            self.assertEqual(rev_code, self.code)
            # 判断响应信息
            self.assertEqual(rev_msg, self.msg)
        if self.case_name == u'自定义群组':# 同上
            # 判断响应码
            self.assertEqual(rev_code, self.code)
            # 判断响应信息
            self.assertEqual(rev_msg, self.msg)



