# -*- coding: utf-8 -*-
# @Time    : 2020/8/14 14:17
# @Author  : Xiaoyunlong


from tool import public_tool as pt
from django.shortcuts import HttpResponse
import json
from main_spider import main_init
from dao import CJ_RW

log = main_init.Init_Config().init_log()
db = pt.db_con.Db_Connection()


def add_cj_rw(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        params = params['nr']
        result,msg = CJ_RW.add_cj_rw(params)
        if result:
            return HttpResponse(json.dumps({'MSG': msg}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500", "ERR": msg}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", "ERR":'请求参数解析错误'}), content_type="application/json")


def get_cj_rw(request):
    params = pt.obtain_post_data(request.GET)
    cx_zd = 'RW_ID,RW_LX,RW_ZT,RW_KHDBH,RW_XM_ID,RW_QDSJ,RW_GXSJ'
    if params['status'] == '0':
        results_df,results_df, results_count = pt.request_get_none_data(cx_zd,"CJ_RW",'RW_ID')
        results_df['RW_GXSJ'] = results_df['RW_GXSJ'].astype(str)
        result = results_df.to_dict(orient='records')
        return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                            content_type="application/json")
    elif params['status'] == '2':
        params = params['nr']
        results_status, df, results_count = CJ_RW.get_cj_gz(params, cx_zd)
        if results_status == True:
            df['RW_GXSJ'] = df['RW_GXSJ'].astype(str)
            result = df.to_dict(orient='records')
            return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500", "ERR": df}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500",'ERR':'请求参数解析错误'}), content_type="application/json")


def update_cj_rw(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        params = params['nr']
        result_list = pt.update_table(params,'CJ_RW','rw_id')

        for request in result_list:
            if request:
                return HttpResponse(json.dumps({'MSG': "200"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")


def delete_cj_rw(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        try:
            params = params['nr']
            result_status,msg = pt.delete_table(params,'CJ_RW','rw_id')
            if result_status:
                return HttpResponse(json.dumps({'MSG': "200",}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'MSG': "500",'ERR':msg}),content_type="application/json")
        except Exception as eromsg:
            log.error(eromsg)
            return HttpResponse(json.dumps({'MSG': "500", 'ERR': eromsg}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", 'ERR': '请求参数解析错误'}), content_type="application/json")

