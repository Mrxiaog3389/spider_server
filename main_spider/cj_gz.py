# -*- coding: utf-8 -*-
# @Time    : 2020/8/13 9:15
# @Author  : Xiaoyunlong

from tool import public_tool as pt
from django.shortcuts import HttpResponse
import json
from main_spider import main_init
from dao import CJ_GZ

log = main_init.Init_Config().init_log()
db = pt.db_con.Db_Connection()


def add_cj_gz(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        result, msg = CJ_GZ.add_cj_gz(params['nr'])
        if result:
            return HttpResponse(json.dumps({'MSG': msg}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500", "ERR": msg}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", "ERR": '请求参数解析错误'}), content_type="application/json")


def get_cj_gz(request):
    params = pt.obtain_post_data(request.GET)
    cx_zd = 'GZ_ID,GZ_NRLB,GZ_PAGE,GZ_HEADERS,GZ_CJSJ,GZ_MC'

    if params['status'] == '0':
        results_status,df, results_count = pt.request_get_none_data(cx_zd,"CJ_GZ",'GZ_ID')
        df['GZ_CJSJ'] = df['GZ_CJSJ'].astype(str)
        df.fillna('', inplace=True)

        result = df.to_dict(orient='records')
        return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                            content_type="application/json")
    elif params['status'] == '2':
        results_status, df, results_count = CJ_GZ.get_cj_gz(params['nr'],cx_zd)
        if results_status == True:
            df['GZ_CJSJ'] = df['GZ_CJSJ'].astype(str)
            df.fillna('', inplace=True)
            result = df.to_dict(orient='records')
            return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500", "ERR": df}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", "ERR": '请求参数解析错误'}), content_type="application/json")


def get_cj_gz_id(request):
    params = pt.obtain_post_data(request.GET)
    if params['status'] == '2':
        params = params['nr']
        cx_zd = '*'
        results, results_df, results_count = CJ_GZ.get_cj_gz(params,cx_zd)
        if results:
            results_df['GZ_CJSJ'] = results_df['GZ_CJSJ'].astype(str)
            results_df.fillna('', inplace=True)

            result = results_df.to_dict(orient='records')
            return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500", "ERR": results_df}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", "ERR": '请求参数解析错误'}), content_type="application/json")


def update_cj_gz(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        params = params['nr']
        result_list = pt.update_table(params,'CJ_GZ','gz_id')

        for request in result_list:
            if request:
                return HttpResponse(json.dumps({'MSG': "200"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")


def delete_cj_gz(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        try:
            params = params['nr']
            result_status,msg = pt.delete_table(params,'CJ_GZ','gz_id')
            if result_status:
                return HttpResponse(json.dumps({'MSG': "200",}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'MSG': "500",'ERR':msg}),content_type="application/json")
        except Exception as eromsg:
            log.error(eromsg)
            return HttpResponse(json.dumps({'MSG': "500", 'ERR': eromsg}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", 'ERR': '请求参数解析错误'}), content_type="application/json")

