# coding:utf-8
import os
import configparser
from utils import getPathInfo

path = getPathInfo.get_Path()
config_path = os.path.join(path, 'config', 'config.ini')
config = configparser.ConfigParser()
config.read(config_path, encoding="utf-8")

class OperateConfig():


    def get_http(self, name):
        value = config.get('HTTP', name)
        return value

    def get_email(self, name):
        value = config.get('EMAIL', name)
        return value

    def get_testintername(self, name):
        value = config.get('TestInterName', name)
        return value

    def get_user(self, name):
        value = config.get('User', name)
        return value

    def set_section(self, section, option, value):
        modify_flag = True  # 标志是否修改配置文件
        # 判断section是否存在
        if not config.has_section(section):
            # 添加section
            config.add_section(section)
        if not config.has_option(section, option):
            config.set(section, option, value)
        else:
            read_value = config.get(section, option)
            if read_value != value:
                config.set(section, option, value)
            else:
                modify_flag = False
        if modify_flag:
            with open(config_path, 'w+',encoding='utf-8') as configfile:
                config.write(configfile)


if __name__ == '__main__':#测试一下，我们读取配置文件的方法是否可用
    print('HTTP中的server值为：', OperateConfig().get_http('server'))
