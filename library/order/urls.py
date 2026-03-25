from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_orders_view, name='all_orders'),
    path('my/', views.my_orders_view, name='my_orders'),
    path('close/<int:order_id>/', views.order_close_view, name='order_close'),
    path('admin/edit/<int:pk>/', views.order_admin_update, name='order_update'),
    path('create/<int:book_id>/', views.order_create_view, name='order_create'),
]