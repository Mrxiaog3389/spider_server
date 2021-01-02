# -*- coding: utf-8 -*-
# @Time    : 2020/8/14 14:17
# @Author  : Xiaoyunlong

import time
import pandas as pd
from tool import public_tool as pt
from main_spider import main_init
import json
log = main_init.Init_Config().init_log()
db = pt.db_con.Db_Connection()


def add_cj_rw(parame:dict):
    try:
        all_params_keys = list(parame.keys())
        if 'rw_khdbh' not in all_params_keys:
            return False,'客户端编号未添加'
        if 'rw_xm_id' not in all_params_keys:
            return False,'关联项目ID未添加'
        if 'rw_gxsj' not in all_params_keys:
            parame['rw_gxsj'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        df = pd.DataFrame(parame, index=[1])
        df.rename(columns=lambda x: x.upper(), inplace=True)
        db.mysql_to_sql(df, 'CJ_RW')
        return True, '200'
    except Exception as eromsg:
        log.error("add_cj_rw :", eromsg)
        return False, eromsg


def get_cj_gz(parames:dict,gz_zd:str):
    try:
        sql = ""
        limit_sql, parame = pt.handle_limit_sql(parames)
        order_sql, parame = pt.handle_order_sql(parames, 'RW_ID')
        for k,v in parames.items():
            sql += f" and {k.upper()} = '{v}'"
        all_sql = f"select {gz_zd} from CJ_RW WHERE " + (sql + order_sql + limit_sql)[4:]
        all_count_sql = "select COUNT(*) from CJ_RW WHERE " + (sql + order_sql)[4:]
        print(all_sql)
        df = db.obtain_mysql_df(all_sql)
        df_count = db.obtain_mysql_count(all_count_sql)
        return True, df, df_count
    except Exception as msg:
        log.error("get_cj_rw :", msg)
        return False, msg