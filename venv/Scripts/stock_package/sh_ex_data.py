from logger_package import myLogger
from ex_data import ex_web_data

import pandas as pd
import json
from jsonpath import jsonpath

class sh_web_data(ex_web_data):

    def __init__(self):
        ex_web_data.__init__(self)
        # self.logger = ex_data.logger

    def json_parse(self, json_str=None):
        self.logger.wt.info("start to parse Page Data ...\n")
        if json_str is not None:
            json_obj = json.loads(json_str)
            company_code = jsonpath(json_obj, '$..pageHelp..COMPANY_CODE')  # 公司/A股代码
            company_abbr = jsonpath(json_obj, '$..pageHelp..COMPANY_ABBR')  # 公司/A股简称
            totalShares = jsonpath(json_obj, "$..pageHelp..totalShares")  # A股总资本
            totalFlowShares = jsonpath(json_obj, '$..pageHelp..totalFlowShares')  # A股流动资本
            list_date = jsonpath(json_obj, '$..pageHelp..LISTING_DATE')  # A股上市日期
            totalPage = jsonpath(json_obj, '$..pageHelp.pageCount')
            self.total_page = totalPage
            """
            df = pd.DataFrame(company_code,
                              index=range(1, len(company_code) + 1),
                              columns=['A股代码'])

            df['A股简称'] = pd.Series(company_abbr, index=df.index)
            df['A股总资本'] = pd.Series(totalShares, index=df.index)
            df['A股流动资本'] = pd.Series(totalFlowShares, index=df.index)
            """

            stock_matix = [company_code, company_abbr ,totalShares, totalFlowShares, list_date]
            df = pd.DataFrame(stock_matix)
            df1 = df.T
            df1.rename(columns={0: 'ID', 1: 'Name',2: 'Total Shares',3: 'Flow Shares', 4:'List_Date'}, inplace=True)
            #df1.sort_values(by=['Total Shares'], inplace=True)
            # print(df1.describe())
            #print(df1)
            return df1
        else:
            self.logger.wt.info("json string is Null , exit ...\n")
            return None

