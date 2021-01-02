# -*- coding: utf-8 -*-
# @Time    : 2020/8/10 11:38
# @Author  : Xiaoyunlong
from django.shortcuts import HttpResponse
from tool import public_tool as pt
from dao import CJ_XM
import json


def add_cj_xm(request):
    """
    添加采集项目
    """
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        result_add = CJ_XM.add_cj_xm(params['nr'])
        if result_add:
            return HttpResponse(json.dumps({'MSG': "200"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")
    else:

        return HttpResponse(json.dumps({'MSG': "500",'ERR':'请求参数解析错误'}), content_type="application/json")


def get_cj_xm(request):
    """
    查询采集项目
    """
    params = pt.obtain_post_data(request.GET)
    if params['status'] == '0':
        results_df,results_df, results_count = CJ_XM.get_cj_xm_all({})
        results_df['XM_CJSJ'] = results_df['XM_CJSJ'].astype(str)
        results_df.fillna('',inplace=True)
        result = results_df.to_dict(orient='records')
        return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                            content_type="application/json")
    elif params['status'] == '2':
        params = params['nr']
        results, results_df, results_count = CJ_XM.get_cj_xm(params)
        if results:
            results_df['XM_CJSJ'] = results_df['XM_CJSJ'].astype(str)
            result = results_df.to_dict(orient='records')
            return HttpResponse(json.dumps({'MSG': "200", "ROWS": result, "TOTAL": results_count}),
                                content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500", "ERR": results_df}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500", "ERR": '请求参数解析错误'}), content_type="application/json")


def update_cj_xm(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        params = params['nr']
        results = CJ_XM.update_cj_xm(params)
        for request in results:
            if request:
                return HttpResponse(json.dumps({'MSG': "200"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")


def delete_cj_xm(request):
    params = pt.obtain_post_data(request.POST)
    if params['status'] == '2':
        params = params['nr']
        results = CJ_XM.delete_cj_xm(params)
        if results:
            return HttpResponse(json.dumps({'MSG': "200"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({'MSG': "500"}), content_type="application/json")


