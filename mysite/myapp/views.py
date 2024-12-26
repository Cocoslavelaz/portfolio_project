from django.shortcuts import render, redirect
from .industry_df import conn_postgre
import pandas as pd
import json

def index(request):

    #get industry
    industry_last = getIndustry()
    industry_return = _return(industry_last)
    
    industry_list = [
        {"name": k, "detail": list(v.values())}
        for k, v in list(industry_return.items())
    ]
    
    industry_list_stock = industry_list[0]["detail"]
    industry_list_industry = industry_list[1]["detail"]
    
    industry_list_stockindustry = {}
    for i in range(len(industry_list_stock)):
        industry_list_stockindustry[str(int(industry_list_stock[i]))] = industry_list_industry[i]
    
    industry_list_stockindustry_reverse = {}
    for i,j in industry_list_stockindustry.items():
        if j not in industry_list_stockindustry_reverse:
            industry_list_stockindustry_reverse[j] = []
        industry_list_stockindustry_reverse[j].append(i)
    
    industry_list_industrylist = []
    for i in range(len(industry_list_industry)):
        if industry_list_industry[i] not in industry_list_industrylist :
            industry_list_industrylist.append(industry_list_industry[i])
    
    #get eps
    eps_last = getEps()
    eps_return = _return(eps_last)
    
    eps_list = [
        {"name": k, "detail": list(v.values())[-1]}
        for k, v in list(eps_return.items())
    ]
    sorted_eps_list = sorted(eps_list, key=lambda x: x['detail'], reverse=True)
    
    #get fcf
    fcf_last = getFcf()
    fcf_return = _return(fcf_last)
    
    fcf_list = [
        {"name": k, "detail": list(v.values())[-1]}
        for k, v in list(fcf_return.items())
    ]
    sorted_fcf_list = sorted(fcf_list, key=lambda x: x['detail'], reverse=True)
    
    #get roe
    roe_last = getRoe()
    roe_return = _return(roe_last)
    
    roe_list = [
        {"name": k, "detail": list(v.values())[-1]}
        for k, v in list(roe_return.items())
    ]
    sorted_roe_list = sorted(roe_list, key=lambda x: x['detail'], reverse=True)
    
    #get volume
    volume_last = getVolume()
    volume_return = _return(volume_last)
    
    volume_list = [
        {"name": k, "detail": list(v.values())[-1]}
        for k, v in list(volume_return.items())[:-1]
    ]
    sorted_volume_list = sorted(volume_list, key=lambda x: x['detail'], reverse=True)
    
    #get dbr
    dbr_last = getDbr()
    dbr_return = _return(dbr_last)
    
    dbr_list = [
        {"name": k, "detail": list(v.values())[-1]}
        for k, v in list(dbr_return.items())
    ]
    sorted_dbr_list = sorted(dbr_list, key=lambda x: x['detail'], reverse=False)

    #get roa
    roa_last = getRoa()
    roa_return = _return(roa_last)
    
    roa_list = [
        {"name": k, "detail": list(v.values())[-1]}
        for k, v in list(roa_return.items())
    ]
    sorted_roa_list = sorted(roa_list, key=lambda x: x['detail'], reverse=True)
    
    #把html回傳的資料作處理後給html
    display = []
    index_1 = '指標一'
    index_2 = '指標二'
    if request.method == 'POST':
        industry_post = request.POST.get('industry_post')
        index_1 = request.POST.get('index_1')
        index_2 = request.POST.get('index_2')
        n = 0
        m = 0
        
        if index_1 == 'eps':
            for i in sorted_eps_list:
                n += 1
                if i['name'] in industry_list_stockindustry_reverse[industry_post]:
                    string = [n, i['name'], i['detail']]
                    display.append(string)
                if len(display) == 10:
                    break
        if index_1 == 'fcf':
            for i in sorted_fcf_list:
                n += 1
                if i['name'] in industry_list_stockindustry_reverse[industry_post]:
                    string = [n, i['name'], i['detail']]
                    display.append(string)
                if len(display) == 10:
                    break
        if index_1 == 'roe':
            for i in sorted_roe_list:
                n += 1
                if i['name'] in industry_list_stockindustry_reverse[industry_post]:
                    string = [n, i['name'], i['detail']]
                    display.append(string)
                if len(display) == 10:
                    break
        if index_1 == 'volume':
            for i in sorted_volume_list:
                n += 1
                if i['name'] in industry_list_stockindustry_reverse[industry_post]:
                    string = [n, i['name'], i['detail']]
                    display.append(string)
                if len(display) == 10:
                    break
        if index_1 == 'dbr':
            for i in sorted_dbr_list:
                n += 1
                if i['name'] in industry_list_stockindustry_reverse[industry_post]:
                    string = [n, i['name'], i['detail']]
                    display.append(string)
                if len(display) == 10:
                    break
        if index_1 == 'roa':
            for i in sorted_roa_list:
                n += 1
                if i['name'] in industry_list_stockindustry_reverse[industry_post]:
                    string = [n, i['name'], i['detail']]
                    display.append(string)
                if len(display) == 10:
                    break
        if index_2 == 'eps':
            for j in sorted_eps_list:
                m += 1
                for i in display:
                    if j['name'] == i[1]:
                        i.append(j['detail'])
                        i[0] = i[0]+m
        if index_2 == 'fcf':
            for j in sorted_fcf_list:
                m += 1
                for i in display:
                    if j['name'] == i[1]:
                        i.append(j['detail'])
                        i[0] = i[0]+m
        if index_2 == 'roe':
            for j in sorted_roe_list:
                m += 1
                for i in display:
                    if j['name'] == i[1]:
                        i.append(j['detail'])
                        i[0] = i[0]+m
        if index_2 == 'volume':
            for j in sorted_volume_list:
                m += 1
                for i in display:
                    if j['name'] == i[1]:
                        i.append(j['detail'])
                        i[0] = i[0]+m
        if index_2 == 'dbr':
            for j in sorted_dbr_list:
                m += 1
                for i in display:
                    if j['name'] == i[1]:
                        i.append(j['detail'])
                        i[0] = i[0]+m
        if index_2 == 'roa':
            for j in sorted_roa_list:
                m += 1
                for i in display:
                    if j['name'] == i[1]:
                        i.append(j['detail'])
                        i[0] = i[0]+m
    
    sorted_display = sorted(display, key=lambda x: x[0])
    
    context = {
        'industrys': industry_list_stockindustry_reverse,
        'industryslist': industry_list_industrylist,
        'epss': sorted_eps_list,
        'display_index_1': index_1,
        'display_index_2': index_2,
        'display': sorted_display,
        'tests': sorted_dbr_list,
    }
    
    return render(request, './myapp/1202.html', context)


def getIndustry(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM industry; 
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def _return(df):
    df = df.dropna(axis=1, how="all")
    return df.to_dict()

def getEps(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM public.eps
    ORDER BY year ASC, quarter ASC ;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def getFcf(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM public.fcf
    ORDER BY year ASC, quarter ASC ;
    """
    pd.options.display.float_format = '{:.6f}'.format
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def getRoe(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM public.roe
    ORDER BY year ASC, quarter ASC ;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def getVolume(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM public.volume
    ORDER BY date ASC  ;
    """
    pd.options.display.float_format = '{:.6f}'.format
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def getDbr(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM public.dbr
    ORDER BY year ASC, quarter ASC ;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def getRoa(request=None):
    # 獲取資料庫連線
    cur, conn = conn_postgre()
    query = """
    SELECT * FROM public.roa
    ORDER BY year ASC, quarter ASC ;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
