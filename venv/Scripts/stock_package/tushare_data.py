import tushare as ts
from datetime import datetime, date, timedelta
import time
import new_logger as lg

class ts_data:
    __counter = 1
    __timer = 0
    def __init__(self):
        self.ts= ts.pro_api('9e78306f8bbe893520528008f70653779cc98c5ec88c07340a3b8f18')

    def basic_info(self):
        data = self.ts.stock_basic(exchange='', list_status='L', fields='symbol,name,area,industry,list_date')
        # data = self.ts.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        return data

    def trans_day(self):
        wx = lg.get_handle()
        today = date.today().strftime('%Y%m%d')
        yesterday = (date.today() + timedelta(days=-1)).strftime('%Y%m%d')
        wx.info("Yesterday:{} ---- Today date: {}".format(yesterday,today))
        return self.ts.trade_cal(exchange='', start_date=yesterday, end_date=today)

    def acquire_daily_data(self, code, period):
        wx = lg.get_handle()
        if (ts_data.__counter == 1):  # 第一次调用，会重置 计时器
            ts_data.__timer = time.time()
        if (ts_data.__counter == 200): # 达到 200 次调用，需要判断与第一次调用的时间间隔
            ts_data.__counter = 0      # 重置计数器=0，下面立即调用一次 计数器+1
            wait_sec = 60 - (int)(time.time() - ts_data.__timer) # 计算时间差
            # ts_data.__timer = time.time() # 重置计时器
            if (wait_sec > 0):
                wx.info("REACH THE LIMIT, MUST WAIT ({}) SECONDS".format(wait_sec))
                time.sleep(wait_sec)
                # ts_data.__timer = time.time() # 重置计时器

        end_date = date.today().strftime('%Y%m%d')
        start_date = (date.today() + timedelta(days = period)).strftime('%Y%m%d')
        df = self.ts.query('daily', ts_code=code, start_date=start_date, end_date=end_date)
        ts_data.__counter += 1
        wx.info("tushare call {} times，id: {}".format(ts_data.__counter, code))
        return df