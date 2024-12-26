"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from etf_rank import views as etf_rank_views
from portfolio_recommend import views as portfolio_recommend_views
from myapp import views as my_app_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',etf_rank_views.index),
    path('portfolio_recommend/',portfolio_recommend_views.index),
    path('portfolio_recommend/submit_questionnaire/', portfolio_recommend_views.submit_questionnaire),
    path('filter_index/',my_app_views.index)
]

