# coding:utf-8
import os
import configparser
from utils import getPathInfo

path = getPathInfo.get_Path()


class OperateConfig():


    def __init__(self, file_name):
        config_path = os.path.join(path, 'config', file_name)
        self.config_path = config_path
        config = configparser.ConfigParser()
        config.read(config_path, encoding="utf-8")
        self.config = config


    def get_http(self, name):
        value = self.config.get('HTTP', name)
        return value

    def get_testintername(self, name):
        value = self.config.get('TestInterName', name)
        return value

    def get_user(self, name):
        value = self.config.get('User', name)
        return value

    def get_vm(self, name):
        value = self.config.get('VM', name)
        return value

    def set_section(self, section, option, value):
        modify_flag = True  # 标志是否修改配置文件
        # 判断section是否存在
        if not self.config.has_section(section):
            # 添加section
            self.config.add_section(section)
        if not self.config.has_option(section, option):
            self.config.set(section, option, value)
        else:
            read_value = self.config.get(section, option)
            if read_value != value:
                self.config.set(section, option, value)
            else:
                modify_flag = False
        if modify_flag:
            with open(self.config_path, 'w+',encoding='utf-8') as configfile:
                self.config.write(configfile)


if __name__ == '__main__':#测试一下，我们读取配置文件的方法是否可用
    print('HTTP中的server值为：', OperateConfig('config.ini').get_http('server'))
