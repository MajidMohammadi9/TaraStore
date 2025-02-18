from django.urls import path

from .views import (
    ProductListView,ProductDetailView,    
    ProductCreateView, ProductUpdateView, ProductDeleteView,
    ProductWomenListView, ProductMenListView, ProductKidsListView,
    ProductSearchView,
    # product_search, 
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('womens/', ProductWomenListView.as_view(), name='product_women'),
    path('mens/', ProductMenListView.as_view(), name='product_men'),
    path('kids/', ProductKidsListView.as_view(), name='product_kids'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
    # path('search/', product_search, name='product_search'),
]
