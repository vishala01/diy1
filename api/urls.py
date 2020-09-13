from django.urls import include, path
from . import views

urlpatterns = [
    path('welcome', views.welcome),
    path('store/<int:store_id>/products', views.get_products, name='get_all_products'),
    path('store/<int:store_id>', views.add_products, name='add_products')
]
