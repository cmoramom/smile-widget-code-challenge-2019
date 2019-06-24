from django.conf.urls import url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views as my_views

urlpatterns = [
    path('api/get-price/', my_views.ProductPriceGetPrice.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
