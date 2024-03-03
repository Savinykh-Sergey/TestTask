from django.urls import path
from .views import ProductListAPIView, ProductLessonsAPIView

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/lessons/', ProductLessonsAPIView.as_view(), name='product-lessons'),
]