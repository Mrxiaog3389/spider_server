# -*- coding: utf-8 -*-
# @Time    : 2020/9/24 10:40
# @Author  : ChenZi

import pandas as pd
import json
from sqlalchemy import create_engine
engine_hw = create_engine("mysql+pymysql://root:T1Wj_atyl_Vu5g_Kp2r_6nBq@10.100.10.7/CC")
def get_xzdz(x):
    x = json.loads(x)
    print(x)
sql = "select * from CJ_WZ where WZ_TAG='movgg' AND WZ_STATE='1'"
df = pd.read_sql(sql,engine_hw)
# df.columns
info_dict = {"WZ_URL":"CJZY_CJURL",'WZ_URL_MD5':'CJZY_CJID','WZ_TITLE':'CJZY_BT','WZ_SOURCE':'CJZY_TGDW','WZ_TIME':'CJZY_FBSJ','WZ_COLLECTTIME':'CJZY_CJSJ','WZ_CREATER':'CJZY_LYDWMC',"WZ_MD5":'CJZY_MD5'}
df.rename(columns=info_dict,inplace=True)
x = list(info_dict.values())
x.append('WZ_PARAMES')
zddf = df[x]
zddf['CJZY_XZURL'] = zddf['WZ_PARAMES'].apply(lambda x:json.loads(x.replace("'", '"'))['ljzd'])
zddf['CJZY_GS'] = 'HTML'
zddf['CJZY_CJZT'] = '1'
zddf['CJZY_WJZT'] = '1'
zddf['CJZY_MLPP'] = '0'
zddf['CJZY_RWJL_ID'] = '0'
zddf['CJZY_YZMLMC'] = zddf['WZ_PARAMES'].apply(lambda x:json.loads(x.replace("'", '"'))['yzmlmc'])
