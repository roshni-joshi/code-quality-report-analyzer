"""
URL configuration for code_quality_analyzer_analysis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import SmellAnalysisView, TrendAnalysisView, HotspotAnalysisView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('smell_analysis/', SmellAnalysisView.as_view(), name='smell_analysis'),
    path('trend_analysis/', TrendAnalysisView.as_view(), name='trend_analysis'),
    path('hotspot_analysis/', HotspotAnalysisView.as_view(), name='hotspot_analysis')
]
