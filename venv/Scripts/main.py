# -*- coding: utf-8 -*-
# __author__ = "WUX"

import new_logger as lg
lg._init_()
wx = lg.get_handle()
# wx.info("this is new logger")

from functions import *

# 从 eastmoney 获得大宗交易数据，开始时间可以指定，截止时间 到当日
update_whole_sales_data(period = -200)

# 从sina获得实时的交易数据
# update_daily_data_from_sina()

# 调用mysql 存储过程获得 A 股市值
#get_list_a_total_amount()

# 从上证、深证 网站更新 A 股基础信息
# update_sh_basic_info()
# update_sz_basic_info()

# 从tushare 获取前一天的 交易数据
# update_daily_data_from_ts(period = -1)
