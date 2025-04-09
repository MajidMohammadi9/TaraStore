from django.urls import path

from .views import faq_list_view, faq_list_view_Trans,faq_search_api

urlpatterns = [
    path('', faq_list_view, name='faq_list'),
    path('trans/', faq_list_view_Trans, name='faq_list_trans'),
    path('search/', faq_search_api, name='faq_search_api'),
]

