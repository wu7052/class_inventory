# -*- coding: utf-8 -*-
# __author__ = "WUX"

import new_logger as lg
lg._init_()
wx = lg.get_handle()
# wx.info("this is new logger")

from functions import *

update_sh_basic_info()
wx.info("<>"*40)
update_sz_basic_info()

# update_daily_data_from_ts(period = -1)

# update_sz_basic_info()
# wx.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
# update_sh_basic_info()
