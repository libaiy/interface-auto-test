# coding:utf-8
from utils import operateConfig

operateconfig = operateConfig.OperateConfig()

class GetUrlParams():
    def get_Url(self):
        protocol_name = operateconfig.get_http('protocol')
        server_domain = operateconfig.get_http('server')
        port = operateconfig.get_http('port')
        new_url = protocol_name + '://' + server_domain + ':' + port
        return new_url

if __name__ == '__main__':# 验证拼接后的正确性
    print(GetUrlParams().get_Url())
