import pymysql


class db_ops:
    def __init__(self, host='localhost', db='mysql', user='root', pwd=None):

        # self.host = host
        # self.db_name = db
        # self.user = user
        try:
            if pwd is None:
                print("[Err DB_OP]===> {0}:{1}:{2} need password ".format(host, db, user))
                raise Exception("Password is Null")
            else:
                # self.pwd = pwd
                self.config = {
                    'host': host,
                    'user': user,
                    'password': pwd,
                    'database': db,
                    'charset': 'utf8',
                    'port': 3306  # 注意端口为int 而不是str
                }
                # self.handle = pymysql.connect(self.host, self.user, self.pwd, self.db_name)
                self.handle = pymysql.connect(**self.config)
                self.cursor = self.handle.cursor()
        except Exception as e:
            print("Err occured in DB_OP __init__{}".format(e))
            exit(-1)
