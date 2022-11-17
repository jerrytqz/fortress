from django.urls import path
from spin import views

urlpatterns = [
    path('wake', views.wake, name='wake'),
    path('log-in/', views.log_in, name='log_in'),
    path('register/', views.register, name='register'),
    path('log-out/', views.log_out, name='log_out'),
    path('buy-spin/', views.buy_spin, name='buy_spin'),
    path('auto-log-in/', views.auto_log_in, name='auto_log_in'),
    path('fetch-inventory/', views.fetch_inventory, name='fetch_inventory'),
    path('fetch-profile/', views.fetch_profile, name='fetch_profile'),
    path('get-free-sp/', views.get_free_sp, name='get_free_sp'),
    path('list-item/', views.list_item, name='list_item'),
    path('fetch-market/', views.fetch_market, name='fetch_market'),
    path('buy-item/', views.buy_item, name='buy_item')
]
