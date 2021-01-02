# -*- coding: utf-8 -*-
# @Time    : 2020/8/10 10:25
# @Author  : ChenZi

import time
import pandas as pd
from tool import public_tool as pt
from main_spider import main_init

log = main_init.Init_Config().init_log()
db = pt.db_con.Db_Connection()


def add_cj_xm(parames: dict, ) -> bool:
    """
    :param parames: 前端传入参数 过来的是一个json
    :return:
    """
    try:
        all_params_keys = list(parames.keys())
        if 'xm_xmlx' not in all_params_keys:
            parames['xm_xmlx'] = '1'
        if 'xm_fj_id' in all_params_keys:
            if parames['xm_fj_id'] != '0':
                parames['xm_fjmlqc'] = pt.get_fjmlid(parames['xm_fj_id'])
        parames['xm_cjsj'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        df = pd.DataFrame(parames, index=[1])
        df.rename(columns=lambda x: x.upper(), inplace=True)
        db.mysql_to_sql(df, 'CJ_XM')
        return True
    except Exception as errmsg:
        log.error("add_cj_xm :", errmsg)
        return False


def get_cj_xm(parame: dict):
    try:
        sql = ""
        limit_sql, parame = pt.handle_limit_sql(parame)
        order_sql, parame = pt.handle_order_sql(parame, 'XM_ID')
        if 'xm_fjmlqc' in list(parame.keys()):
            v_fjmlqc = parame['xm_fjmlqc'].split(',')
            for fjxm_id in v_fjmlqc:
                sql += f" and find_in_set(" + fjxm_id + "," + 'XM_FJMLQC' + ")"
            del parame['xm_fjmlqc']
        for k, v in parame.items():
            sql += f" and {k.upper()} = '{v}'"
        all_sql = "select * from CJ_XM WHERE " + (sql + order_sql + limit_sql)[4:]
        all_count_sql = "select COUNT(*) from CJ_XM WHERE " + (sql + order_sql)[4:]
        df = db.obtain_mysql_df(all_sql)
        df_count = db.obtain_mysql_count(all_count_sql)
        return True, df, df_count
    except Exception as msg:
        log.error("get_cj_xm :", msg)
        return False, msg, 0

def get_cj_xm_all(parame: dict):
    try:
        limit_sql, parame = pt.handle_limit_sql(parame)
        order_sql, parame = pt.handle_order_sql(parame, 'XM_ID')
        all_sql = "select * from CJ_XM  " + ( order_sql + limit_sql)
        all_count_sql = "select COUNT(*) from CJ_XM  " + (order_sql)
        df = db.obtain_mysql_df(all_sql)
        df_count = db.obtain_mysql_count(all_count_sql)
        return True, df, df_count
    except Exception as msg:
        log.error("get_cj_xm :", msg)
        return False, msg, 0


def update_cj_xm(parames: dict):
    all_update_sql = []
    xm_id = parames['xm_id']
    del parames["xm_id"]
    for k, v in parames.items():
        update_sql = f"UPDATE CJ_XM SET {k} = '{v}' WHERE XM_ID='{xm_id}'"
        all_update_sql.append(update_sql)
    all_status_result = []
    for update_sql in all_update_sql:
        status_result = db.commit_sql(update_sql)
        all_status_result.append(status_result)
    return all_status_result

def delete_cj_xm(parames: dict):
    xm_id = parames['xm_id']
    delete_sql = f"DELETE FROM CJ_XM WHERE XM_ID={xm_id} "
    status_result = db.commit_sql(delete_sql)
    return status_result