from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from media import views

urlpatterns = [
    path('pages/', views.PageList.as_view(),
        name='page_list'),
    path('pages/<int:pk>/', views.PageDetail.as_view(),
        name='page_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
