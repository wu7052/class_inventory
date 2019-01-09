# from logger_package import myLogger
from db_package import db_ops

import urllib3
import requests
# import chardet
import logging
import os
from urllib import parse
import new_logger as lg
from datetime import datetime, time, date


class ex_web_data(object):

    def __init__(self):
        wx = lg.get_handle()
        # log_dir = os.path.abspath('.')
        # self.logger = myLogger(log_dir)
        try:
            self.db = db_ops(host='127.0.0.1', db='stock', user='wx', pwd='5171013')
            wx.info("ex_web_data : __init__() called")
        except Exception as e:
            raise e

    def __del__(self):
        # self.logger.wt.info("{} __del__ called".format(self))
        wx = lg.get_handle()
        self.db.cursor.close()
        self.db.handle.close()
        wx.info("ex_web_data : __del__() called")

    def url_encode(self, str):
        return parse.quote(str)

    def daily_data_table_name(self):
        table_name = date.today().strftime('%Y%m')
        return table_name

    def db_fetch_stock_id(self, pre_id):
        sql = "select id from list_a where id like '" + pre_id + "'"
        id = self.db.cursor.execute(sql)
        id_array = self.db.cursor.fetchmany(id)
        return id_array

    def db_load_into_daily_data(self, dd_df=None, t_name = None):
        wx = lg.get_handle()
        if (dd_df is None or t_name is None):
            wx.info("Err: Daily Data Frame or Table Name is Empty,")
            return -1
        dd_array = dd_df.values.tolist()
        i = 0
        while (i < len(dd_array)):
            dd_array[i] = tuple(dd_array[i])
            i += 1
        sql = "REPLACE INTO "+t_name+" SET id=%s, date=%s, open=%s, high=%s, low=%s, " \
              "close=%s, pre_close=%s, chg=%s,  pct_chg=%s,vol=%s, amount=%s"
        self.db.cursor.executemany(sql, dd_array)
        self.db.handle.commit()
        # wx.info(dd_array)

    def db_load_into_list_a_2(self, basic_info_df):
        wx = lg.get_handle()
        if (basic_info_df is None):
            wx.info("Err: basic info dataframe is Empty,")
            return -1
        basic_info_array = basic_info_df.values.tolist()
        i = 0
        while (i < len(basic_info_array)):
            basic_info_array[i] = tuple(basic_info_array[i])
            i += 1
        # wx.info(basic_info_array)
        sql = "REPLACE INTO stock.list_a SET id=%s, name=%s, total_shares=%s, flow_shares=%s, list_date=%s, " \
                                         "full_name=%s, industry=%s, industry_code=%s"
        self.db.cursor.executemany(sql, basic_info_array)
        self.db.handle.commit()

    """
    db_load_into_list_a() 已经废弃，目前使用新函数 db_load_into_list_a_2() 代替
    """
    def db_load_into_list_a(self, basic_info_df):
        wx = lg.get_handle()
        for basic_info in basic_info_df.get_values():
            sql = "select * from list_a where id ='" + basic_info[0] + "'"
            # sql =  'select count(*) from list_a where id = \'%s\''%basic_info[0]
            iCount = self.db.cursor.execute(sql)  # 返回值，受影响的行数， 不需要 fetchall 来读取了
            if iCount == 0:
                sql = "insert into list_a (id, name, total_shares, flow_shares, list_date, full_name, industry, industry_code) " \
                      "values (%s, %s, %s ,%s, %s, %s, %s, %s)"
                # self.logger.wt.info(
                #     "Insert id={0}, name={1}, t_shares={2}, f_shares={3}, date={4}, f_name={5}, industry={6}, industry_code={7}".
                #     format(basic_info[0], basic_info[1], basic_info[2], basic_info[3], basic_info[4], basic_info[5], basic_info[6], basic_info[7]))
                wx.info("Insert id={0}, name={1}".format(basic_info[0], basic_info[1] ))
                self.db.cursor.execute(sql, (
                    basic_info[0], basic_info[1], float(basic_info[2]), float(basic_info[3]), basic_info[4],
                    basic_info[5], basic_info[6], basic_info[7]))
                self.db.handle.commit()
            elif iCount == 1:
                wx.info("Existed\t[{0}==>{1}]".format(basic_info[0], basic_info[1]))
            else:
                wx.info("iCount == %d , what happended ???" % iCount)

    def get_json_str(self, url, web_flag=None):
        if (web_flag == 'sz_basic'):
            header = {
                'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                'Connection': 'keep-alive'
            }
        elif (web_flag == 'sh_basic'):
            header = {
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
            pass

        # 获得html源码,utf-8解码
        # logging.debug(chardet.detect(raw_data.data))
        # logging.debug(type(raw_data.data))
        # print(chardet.detect(unicode))
        # print(type(raw_data.data))
        unicode = raw_data.data.decode("utf-8")
        # print(type(unicode))

        return unicode
