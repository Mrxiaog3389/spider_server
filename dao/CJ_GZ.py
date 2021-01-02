# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 9:24
# @Author  : Xiaoyunlong

import time
import pandas as pd
from tool import public_tool as pt
from main_spider import main_init
import json
log = main_init.Init_Config().init_log()
db = pt.db_con.Db_Connection()


def add_cj_gz(parame: dict):
    """
    添加规则
    """
    all_params_keys = list(parame.keys())
    if "gz_mc" not in all_params_keys:
        return False, "规则名称未添加"
    else:
        try:
            if "gz_cjsj" not in all_params_keys:
                parame['gz_cjsj'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            if 'gz_headers' in all_params_keys:
                parame['gz_headers'] = json.dumps(parame['gz_headers'])
            if 'gz_nr' in all_params_keys:
                parame['gz_nr'] = json.dumps(parame['gz_nr'])
            df = pd.DataFrame(parame, index=[1])
            df.rename(columns=lambda x: x.upper(), inplace=True)
            db.mysql_to_sql(df, 'CJ_GZ')
            return True, '200'
        except Exception as eromsg:
            log.error("add_cj_xm :", eromsg)
            return False, eromsg

def get_cj_gz(parames:dict,gz_zd:str):
    try:
        sql = ""
        limit_sql, parame = pt.handle_limit_sql(parames)
        order_sql, parame = pt.handle_order_sql(parames, 'GZ_ID')
        for k,v in parames.items():
            sql += f" and {k.upper()} = '{v}'"
        all_sql = f"select {gz_zd} from CJ_GZ WHERE " + (sql + order_sql + limit_sql)[4:]
        all_count_sql = "select COUNT(*) from CJ_GZ WHERE " + (sql + order_sql)[4:]
        df = db.obtain_mysql_df(all_sql)
        df_count = db.obtain_mysql_count(all_count_sql)
        return True, df, df_count
    except Exception as msg:
        log.error("get_cj_gz :", msg)
        return False, msg


