from django.urls import path
from .views import IndexView, registerMonitForms, myStock, EditMonitForms, DeleteMonitForms, registerWithStockMonitForms, historyMonitoringView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add/', registerMonitForms.as_view(),
         name='add_stock'),
    path('add/?<str:stock>', registerWithStockMonitForms.as_view(),
         name='addWstock_stock'),
    path('update/<int:pk>/', EditMonitForms.as_view(),
         name='update_stock'),
    path('delete/<int:pk>/', DeleteMonitForms.as_view(),
         name='delete_stock'),
    path('meusativos', myStock.as_view(), name='myStock'),
    path('histativos', historyMonitoringView.as_view(), name='histStock')
]
