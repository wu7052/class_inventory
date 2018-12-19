import tushare as ts

class ts_data:

    def __init__(self):
        self.ts= ts.pro_api('9e78306f8bbe893520528008f70653779cc98c5ec88c07340a3b8f18')


    def basic_info(self):
        data = self.ts.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        return data