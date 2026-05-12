from django.urls import path
from . import views
from .views import heatmap_page, HeatmapDataAPIView

urlpatterns = [
    # صفحة إرسال الشكوى (HTML)
    path('', views.add_complaint_view, name='add-complaint-page'),
    path('complaints/track/', views.track_complaints_view, name='track-complaints'),
    path('api/complaints/my/', views.MyComplaintsAPIView.as_view(), name='my-complaints'),
    
    #الخريطة
    path('heatmap/', heatmap_page, name='heatmap-page'),
    path('api/heatmap/', HeatmapDataAPIView.as_view(),name='heatmap-api'),

    #لوحة متابعة المشرف
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('api/dashboard/stats/', views.DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    
    
    # API لإرسال الشكاوى
    path('api/create/', views.ComplaintCreateAPIView.as_view(), name='create-complaint'),

   

]