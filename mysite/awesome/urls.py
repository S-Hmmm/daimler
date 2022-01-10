from django.urls import path
from . import views


app_name = 'awesome'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:case_id>/', views.detail, name='detail'),
    path('test_pt/', views.pt, name='pt'),
    path('node/', views.node, name='node'),
]
