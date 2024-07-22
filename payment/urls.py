from django.urls import path
from . import views

urlpatterns = [
    path('collect_money/', views.collect_money, name='collect_money'),
    path('deposit/', views.deposit, name='deposit'),
    path('status/', views.status, name='status'),
    path('transaction_id/', views.transaction_id, name='transaction_id'),

]