from db_package import db_ops

import urllib3
import requests
import chardet
# import logging
import os
from urllib import parse
import new_logger as lg
from datetime import datetime, time, date
import pandas as pd
import json
from jsonpath import jsonpath
import re


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
        wx.info("ex_web_data :{}: __del__() called".format(self))

    def url_encode(self, str):
        return parse.quote(str)

    def daily_data_table_name(self):
        table_name = date.today().strftime('%Y%m')
        return table_name

    def db_fetch_stock_id(self, pre_id):
        if pre_id == '00%':
            sql = "select id from list_a where id like '" + pre_id + "' and id not like '002%'"
        else:
            sql = "select id from list_a where id like '" + pre_id + "'"
        id = self.db.cursor.execute(sql)
        id_array = self.db.cursor.fetchmany(id)
        return id_array

    def db_load_into_daily_data(self, dd_df=None, t_name=None):
        wx = lg.get_handle()
        if dd_df is None or t_name is None:
            wx.info("Err: Daily Data Frame or Table Name is Empty,")
            return -1
        dd_array = dd_df.values.tolist()
        i = 0
        while i < len(dd_array):
            dd_array[i] = tuple(dd_array[i])
            i += 1
        sql = "REPLACE INTO " + t_name + " SET id=%s, date=%s, open=%s, high=%s, low=%s, " \
                                         "close=%s, pre_close=%s, chg=%s,  pct_chg=%s,vol=%s, amount=%s"
        self.db.cursor.executemany(sql, dd_array)
        self.db.handle.commit()
        # wx.info(dd_array)

    def db_call_procedure(self, p_name, *args):
        wx = lg.get_handle()
        # wx.info("[{}] parameter ==> values {},{},{},{},{},{},{}".format(p_name, args[0], args[1], args[2],
        #                                                                 args[3], args[4],args[5], args[6]))
        self.db.cursor.callproc(p_name, (args[0], args[1], args[2], args[3], args[4], args[5], args[6]))
        self.db.cursor.execute(
            "select @_" + p_name + "_0, @_" + p_name + "_1, @_" + p_name + "_2, @_" + p_name + "_3, @_" + p_name + "_4, @_" + p_name + "_5, @_" + p_name + "_6")
        result = self.db.cursor.fetchall()
        wx.info(result)

    def db_load_into_list_a_2(self, basic_info_df):
        wx = lg.get_handle()
        if (basic_info_df is None):
            wx.info("Err: basic info dataframe is Empty,")
            return -1
        basic_info_array = basic_info_df.values.tolist()
        i = 0
        while i < len(basic_info_array):
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
                # self.logger.wt.info( "Insert id={0}, name={1}, t_shares={2}, f_shares={3}, date={4}, f_name={5},
                # industry={6}, industry_code={7}". format(basic_info[0], basic_info[1], basic_info[2], basic_info[
                # 3], basic_info[4], basic_info[5], basic_info[6], basic_info[7]))
                wx.info("Insert id={0}, name={1}".format(basic_info[0], basic_info[1]))
                self.db.cursor.execute(sql, (
                    basic_info[0], basic_info[1], float(basic_info[2]), float(basic_info[3]), basic_info[4],
                    basic_info[5], basic_info[6], basic_info[7]))
                self.db.handle.commit()
            elif iCount == 1:
                wx.info("Existed\t[{0}==>{1}]".format(basic_info[0], basic_info[1]))
            else:
                wx.info("iCount == %d , what happended ???" % iCount)

    def get_json_str(self, url, web_flag=None):
        wx = lg.get_handle()
        if web_flag == 'sz_basic':
            header = {
                'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
                'Connection': 'keep-alive'
            }
        elif web_flag == 'sh_basic':
            header = {
                'Cookie': 'yfx_c_g_u_id_10000042=_ck18012900250116338392357618947; VISITED_MENU=%5B%228528%22%5D; yfx_f_l_v_t_10000042=f_t_1517156701630__r_t_1517314287296__v_t_1517320502571__r_c_2',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
                'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/'
            }
        elif web_flag == 'eastmoney':
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'st_pvi=71738581877645; st_sp=2018-11-22%2011%3A40%3A40; qgqp_b_id=8db9365e6c143170016c773cee144103; em_hq_fls=js; HAList=a-sz-000333-%u7F8E%u7684%u96C6%u56E2%2Ca-sz-300059-%u4E1C%u65B9%u8D22%u5BCC; st_si=74062085443937; st_asi=delete; st_sn=27; st_psi=20190113183705692-113300301007-4079839165',
                'Host': 'dcfm.eastmoney.com',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
            }

        requests.packages.urllib3.disable_warnings()
        http = urllib3.PoolManager()
        try:
            raw_data = http.request('GET', url, headers=header)
        except Exception as e:
            raise e
        finally:
            if raw_data.status >= 300:
                wx.info("Web response failed : {}".format(url))
                return None

        # 获得html源码,utf-8解码
        str_type = chardet.detect(raw_data.data)
        # unicode = raw_data.data.decode(str_type['encoding'])
        unicode = lg.str_decode(raw_data.data, str_type['encoding'])
        return unicode

    def sina_daily_data_json_parse(self, json_str=None, date='20100101'):
        # self.logger.wt.info("start to parse BASIC INFO ...\n")
        if json_str is not None:
            json_obj = json.loads(json_str)

            company_code = jsonpath(json_obj, '$..code')  # 公司/A股代码
            open = jsonpath(json_obj, '$..open')
            high = jsonpath(json_obj, '$..high')
            low = jsonpath(json_obj, '$..low')
            close = jsonpath(json_obj, '$..trade')
            pre_close = jsonpath(json_obj, '$..settlement')
            chg = jsonpath(json_obj, '$..pricechange')
            pct_chg = jsonpath(json_obj, '$..changepercent')
            v = jsonpath(json_obj, '$..volume')  # 成交量，单位“股”，需要换算成“手”
            vol = [float(tmp) / 100 for tmp in v]  # 换算成 “手” 成交量
            am = jsonpath(json_obj, '$..amount')  # 成交金额， 单位“元”， 需要换算成 “千”
            amount = [float(tmp) / 1000 for tmp in am]  # 换算成 “千” 成交金额
            cur_date = list(date for _ in range(0, len(company_code)))
            daily_data = [company_code, cur_date, open, high, low, close, pre_close, chg, pct_chg, vol, amount]
            df = pd.DataFrame(daily_data)
            df1 = df.T
            df1.rename(
                columns={0: 'ID', 1: 'Date', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Close', 6: 'Pre_close', 7: 'Chg',
                         8: 'Pct_chg', 9: 'Vol', 10: 'Amount'}, inplace=True)
            # col_name = df1.columns.tolist()
            # col_name.insert(1, 'Date')
            # df1.reindex(columns=col_name)
            # df1['Date'] = date
            return df1
        else:
            # self.logger.wt.info("json string is Null , exit ...\n")
            return None

    def east_ws_json_parse(self, json_str=None):
        if json_str is not None:
            json_obj = json.loads(json_str)
        self.page_count = json_obj['pages']
        dt = jsonpath(json_obj, '$..TDATE')
        date = [re.sub(r'-','',tmp[0:10]) for tmp in dt]
        id = jsonpath(json_obj, '$..SECUCODE')
        disc = jsonpath(json_obj, '$..Zyl')
        price = jsonpath(json_obj, '$..PRICE')
        vol = jsonpath(json_obj, '$..TVOL')
        v_t = jsonpath(json_obj, '$..Cjeltszb')
        vol_tf = [float(tmp) * 100 for tmp in v_t]  # 换算成百分比，交易量占流动股的百分比
        amount = jsonpath(json_obj, '$..TVAL')
        b_code = jsonpath(json_obj, '$..BUYERCODE')
        s_code = jsonpath(json_obj, '$..SALESCODE')
        close_price = jsonpath(json_obj, '$..CPRICE')
        pct_chg = jsonpath(json_obj, '$..RCHANGE')
        ws_data = [date, id, disc, price, vol, vol_tf, amount, b_code, s_code, close_price, pct_chg]
        df = pd.DataFrame(ws_data)
        df1 = df.T
        df1.rename(columns={0: 'Date', 1: 'ID', 2: 'Disc', 3: 'Price', 4: 'Vol', 5: 'Vol_tf', 6: 'Amount', 7: 'B_code',
                            8: 'S_code', 9: 'Close_price', 10: 'Pct_chg'}, inplace=True)

        # irow = 0
        # while irow < len(df1['Date'].values.tolist()):
        #     date_str = df1['Date'][irow]
        #     date_str = date_str[:10]
        #     date_str = re.sub('-', '', date_str)
        #     df1['Date'][irow] = date_str
        #     irow += 1

        return df1

    def db_load_into_ws(self, ws_df=None, force_update=False):
        wx = lg.get_handle()
        if (ws_df is None):
            wx.info("Err: whole sales dataframe is Empty,")
            return -1
        ws_array = ws_df.values.tolist()
        i = 0
        while i < len(ws_array):
            ws_array[i] = tuple(ws_array[i])
            i += 1
        sql = "REPLACE INTO stock.ws_201901 SET date=%s, id=%s, disc=%s, price=%s, vol=%s, vol_tf=%s, " \
              "amount=%s, b_code=%s, s_code=%s, close_price=%s, pct_chg=%s"
        self.db.cursor.executemany(sql, ws_array)
        self.db.handle.commit()
