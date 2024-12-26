from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
def index(request):
    return render(request, 'portfolio_recommend/portfolio_optimization.html')

# 風險分類函式
def determine_risk_category(age, experience, tolerance, return_expectation):
    score = 0
    if age == "20-30 歲":
        score += 4
    elif age == "31-40 歲":
        score += 3
    elif age == "41-50 歲":
        score += 2
    elif age == "51 歲以上":
        score += 1
    if experience == "5+":
        score += 5
    elif experience == "3-5":
        score += 4
    elif experience == "1-3":
        score += 3
    elif experience == "1":
        score += 2
    elif experience == "none":
        score += 1
    if tolerance == "25+":
        score += 5
    elif tolerance == "20":
        score += 4
    elif tolerance == "15":
        score += 3
    elif tolerance == "10":
        score += 2
    elif tolerance == "5":
        score += 1
    try:
        if not return_expectation:
            return_expectation = 0
        return_expectation = float(return_expectation)
        if return_expectation >= 20:
            score += 5
        elif return_expectation >= 15:
            score += 4
        elif return_expectation >= 10:
            score += 3
        elif return_expectation >= 5:
            score += 2
        else:
            score += 1
    except ValueError:
        return "Invalid input for return expectation"
    if score >= 16:
        return "高風險"
    elif score >= 12:
        return "中高風險"
    elif score >= 8:
        return "中等風險"
    elif score >= 4:
        return "中低風險"
    else:
        return "低風險"

# 顯示結果的視圖
def submit_questionnaire(request):
    if request.method == "POST":
        age = request.POST.get("age")
        experience = request.POST.get("investmentExperience")
        tolerance = request.POST.get("riskTolerance")
        return_expectation = request.POST.get("expectedReturn")

        risk_category = determine_risk_category(age, experience, tolerance, return_expectation)

        file_path = 'portfolio_recommend/filtered_stock_data_10.csv'
        data = pd.read_csv(file_path)

        # 確保正確提取股票代碼
        if 'stock_code' not in data.columns:
            data.rename(columns={data.columns[0]: 'stock_code'}, inplace=True)  # 假設第一列為股票代碼
        # 按波動率 (deviation) 排序
        data = data.sort_values(by='deviation', ascending=False)

        # 根據風險屬性篩選符合的兩支股票
        if risk_category == "高風險":
            selected_stocks = data.head(2)
        elif risk_category == "中高風險":
            selected_stocks = data.iloc[2:4]
        elif risk_category == "中等風險":
            selected_stocks = data.iloc[4:6]
        elif risk_category == "中低風險":
            selected_stocks = data.iloc[6:8]
        elif risk_category == "低風險":
            selected_stocks = data.tail(2)
        else:
            return HttpResponse("風險屬性計算錯誤，請重試。")

        # 標記符合風險屬性的股票
        data['is_recommended'] = data['stock_code'].isin(selected_stocks['stock_code'])

        context = {
            'risk_category': risk_category,
            'classified_data': data.to_dict(orient='records'),
        }
        return render(request, 'portfolio_recommend/result.html', context)

    return HttpResponse("僅接受 POST 請求")