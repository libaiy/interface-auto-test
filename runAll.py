import os
import utils.htmlTestRunner as HTMLTestRunner
from utils import getPathInfo
import unittest
from utils import operateConfig
#from utils.configEmail import send_email
from utils import logger

#send_mail = send_email()
path = getPathInfo.get_Path()
report_path = os.path.join(path, 'result')
config_path = os.path.join(path, 'config')
on_off = operateConfig.OperateConfig().get_email('on_off')
log = logger.logger

class AllTest:
    def __init__(self):
        global resultPath
        # result/report.html
        resultPath = os.path.join(report_path, "report.html")
        # 配置执行哪些测试文件的配置文件路径
        self.caseListFile = os.path.join(config_path, "caselist.ini")
        # 真正的测试断言文件路径
        self.caseFile = os.path.join(path, "testCase")
        self.caseList = []
        # 将resultPath的值输入到日志，方便定位查看问题
        log.info('测试报告保存位置：%s'%resultPath)

    def set_case_list(self):
        """
        读取caselist.txt文件中的用例名称，并添加到caselist元素组
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):# 如果data非空且不以#开头
                self.caseList.append(data.replace("\n", ""))#读取每行数据会将换行转换为\n，去掉每行数据中的\n
        fb.close()

    def set_case_suite(self):
        """

        :return:
        """
        # 通过set_case_list()拿到caselist元素组
        self.set_case_list()
        test_suite = unittest.TestSuite()
        suite_module = []
        # 从caselist元素组中循环取出case
        print("caselist:")
        i = 0
        for case in self.caseList:
            i += 1
            case_name = case.split("/")[-1]  #通过split函数来将aaa/bbb分割字符串，-1取后面，0取前面
            print("\t%s.%s"%(i, case_name))  #打印出取出来的名称
            #批量加载用例，第一个参数为用例存放路径，第一个参数为路径文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            # 将discover存入suite_module元素组
            suite_module.append(discover)
            #print('suite_module:'+str(suite_module))
        if len(suite_module) > 0:#判断suite_module元素组是否存在元素
            for suite in suite_module:#如果存在，循环取出元素组内容，命名为suite
                for test_name in suite:#从discover中取出test_name，使用addTest添加到测试集
                    test_suite.addTest(test_name)
        else:
            print('else:')
            return None
        return test_suite#返回测试集

    def run(self):
        """
        run test
        :return:
        """
        try:
            log.info("******************************TEST START*****************************")
            print("********TEST START********")
            suit = self.set_case_suite()#调用set_case_suite获取test_suite
            print('run case')
            print(str(suit))
            if suit is not None:#判断test_suite是否为空
                fp = open(resultPath, 'wb')#打开result/20181108/report.html测试报告文件，如果不存在就创建
                #调用HTMLTestRunner
                runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                print("Have no case to test.")
        except Exception as ex:
            print(str(ex))
            log.info(str(ex))

        finally:
            log.info("******************************TEST END*****************************")
            print("*********TEST END*********")
            fp.close()
        #判断邮件发送的开关
        #if on_off == 'on':
        #    send_mail.outlook()
        #else:
        #    print("邮件发送开关配置关闭，请打开开关后可正常自动发送测试报告")

if __name__ == '__main__':
    AllTest().run()


