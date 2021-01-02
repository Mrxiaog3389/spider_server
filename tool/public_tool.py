# -*- coding: utf-8 -*-
# @Time    : 2020/8/10 10:40
# @Author  : Xiaoyunlong
from tool import db_con
import json

from main_spider import main_init

config = main_init.Init_Config().init_log()
db = db_con.Db_Connection()


def df_columns_upper(df):
    """
    :return: 将一个DF的列名变成大写
    """
    return df.rename(columns=lambda x: x.upper(), inplace=True)


def get_fjmlid(fjmlid):
    """
    :param fjmlid: 父级目录ID
    :return: 获取上级父级目录ID
    """
    fj_sql = f"select XM_ID,XM_FJ_ID from CJ_XM where XM_ID = '{fjmlid}'"
    fj_df = db.obtain_mysql_df(fj_sql)
    if len(fj_df) != 0:
        return (str(list(fj_df['XM_FJ_ID'])[0]) + ',' + str(list(fj_df['XM_ID'])[0])).replace('0,', '')


def obtain_post_data(data):
    if len(dict(data)) == 0:
        return {'status':'0'}
    try:
        data_info = dict(data)
        data = {}
        for k,v in data_info.items():
            if v[0] == '' or v[0] == 'undefined':
                continue
            else:
                data[k] = v[0]
        return {'status':'2','nr':data}
    except:
        config.error("POST请求错误", data)
        return {'status':'1'}


def obtain_get_data(data):
    if len(data) == 0:
        return True
    try:
        data = json.loads(list(data.keys())[0])
        return data
    except:
        config.error("GET请求错误", data)
        return False


def handle_limit_sql(parames:dict):
    """
    处理分页的规则
    """
    limit_dict = {}
    parames_key_list = list(parames.keys())
    if 'page' in parames_key_list:
        if parames['page']== 0:
            limit_dict['page'] = 1
        else:
            limit_dict['page'] = parames['page']
        del parames['page']
    else:
        limit_dict['page'] = 1
    if 'rows' in parames_key_list:
        if parames['rows']== 0:
            limit_dict['rows'] = 20
        else:
            limit_dict['rows'] = parames['rows']
        del parames['rows']
    else:
        limit_dict['rows'] = 20
    sql = f" limit {limit_dict['rows'] * (limit_dict['page']-1)},{limit_dict['rows']}"
    return sql,parames


def handle_order_sql(parame:dict,order_name_string:str):
    """
    处理分页的规则
    """
    order_dict = {}
    order_key_list = list(parame.keys())
    if 'order_name'  in order_key_list:
        order_dict['order_name'] = parame['order_name']
        del parame['order_name']
    else:
        order_dict['order_name'] = order_name_string
    if 'order_desc' in order_key_list:
        order_dict['order_desc'] = parame['order_desc']
        del order_dict['order_desc']
    else:
        order_dict['order_desc'] = '_'
    order_sql = f" order by {order_dict['order_name']},{order_dict['order_desc']}".replace(',_','')
    return order_sql, parame


def request_get_none_data(cx_zd,table_name,table_id,parames={}):
    """
    当GET请求是直接请求的时候   直接返回数据
    """
    try:
        limit_sql, parames = handle_limit_sql(parames)
        order_sql, parames = handle_order_sql(parames, table_id)
        all_sql = f"select {cx_zd} from {table_name} " + (order_sql + limit_sql)
        all_count_sql = f"select COUNT(*) from {table_name} " + (order_sql)
        df = db.obtain_mysql_df(all_sql)
        df_count = db.obtain_mysql_count(all_count_sql)
        return True, df, df_count
    except Exception as msg:
        config.error(f"{table_name} :", msg)
        return False, msg, 0


def update_table(parames: dict,table_name:str,zy_zd:str):
    all_update_sql = []
    xm_id = parames[zy_zd]
    del parames[zy_zd]
    for k, v in parames.items():
        update_sql = f"UPDATE {table_name} SET {k} = '{v}' WHERE {zy_zd}='{xm_id}'"
        all_update_sql.append(update_sql)
    all_status_result = []
    for update_sql in all_update_sql:
        status_result = db.commit_sql(update_sql)
        all_status_result.append(status_result)
    return all_status_result

def delete_table(parames: dict,table_name:str,zy_zd:str):
    try:
        xm_id = parames[zy_zd]
        delete_sql = f"DELETE FROM {table_name} WHERE {zy_zd}={xm_id} "
        status_result = db.commit_sql(delete_sql)
        return True,status_result
    except Exception as eromsg:
        config.error(f"{table_name} :", eromsg)
        return False,eromsg