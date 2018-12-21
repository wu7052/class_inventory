from logger_package import myLogger

import urllib3
import requests
import chardet
import logging
import os
from urllib import parse


class ex_web_data(object):

    def __init__(self):
        log_dir = os.path.abspath('.')
        self.logger = myLogger(log_dir)
        # self.logger.wt.info("calling logger from Father Class ex_web_data")

    def url_encode(self, str):
        return parse.quote(str)

    def get_json_str(self, url):
        header = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer': r'https://www.jianshu.com/c/20f7f4031550?utm_medium=index-collections&utm_source=desktop',
            'Connection': 'keep-alive'
        }

        headers = {
            'Cookie': 'yfx_c_g_u_id_10000042=_ck18012900250116338392357618947; VISITED_MENU=%5B%228528%22%5D; yfx_f_l_v_t_10000042=f_t_1517156701630__r_t_1517314287296__v_t_1517320502571__r_c_2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
            'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
        }

        requests.packages.urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            raw_data = http.request('GET', url, headers=headers)
        except Exception as e:
            raise e
        finally:
            # logging.debug('[fetcher]{}'.format(raw_data.status)) # 200
            pass

        # 获得html源码,utf-8解码
        # logging.debug(chardet.detect(raw_data.data))
        # logging.debug(type(raw_data.data))
        # print(chardet.detect(unicode))
        # print(type(raw_data.data))
        unicode = raw_data.data.decode("utf-8")
        # print(type(unicode))

        return unicode