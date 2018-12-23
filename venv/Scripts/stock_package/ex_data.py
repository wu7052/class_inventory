from logger_package import myLogger
from db_package import db_ops

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
        self.db = db_ops(host='127.0.0.1', db='stock', user='wx', pwd='5171013')

    def __del__(self):
        self.db.cursor.close()
        self.db.handle.close()
        self.logger.wt.info("{} Destoried".format(self))

    def url_encode(self, str):
        return parse.quote(str)

    def db_load_into_list_a(self, basic_info_df):
        for array in basic_info_df.get_values():
            sql = "select * from list_a where id ='" + array[0] + "'"
            # sql =  'select count(*) from list_a where id = \'%s\''%array[0]
            iCount = self.db.cursor.execute(sql)  # 返回值，受影响的行数， 不需要 fetchall 来读取了
            if iCount == 0:
                sql = "insert into list_a (id, name, total_shares, flow_shares, list_date, full_name, industry, industry_code) " \
                      "values (%s, %s, %s ,%s, %s, %s, %s, %s)"
                self.logger.wt.info(
                    "Insert id={0}, name={1}, t_shares={2}, f_shares={3}, date={4}, f_name={5}, industry={6}, industry_code={7}".
                    format(array[0], array[1], array[2], array[3], array[4], array[5], array[6], array[7]))
                self.db.cursor.execute(sql, (
                array[0], array[1], float(array[2]), float(array[3]), array[4], array[5], array[6], array[7]))
                self.db.handle.commit()
            elif iCount == 1:
                self.logger.wt.info("Existed\t[{0}==>{1}]".format(array[0], array[1]))
            else:
                self.logger.wt.info("iCount == %d , what happended ???" % iCount)


    def get_json_str(self, url):
        header = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
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
            raw_data = http.request('GET', url, headers=header)
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