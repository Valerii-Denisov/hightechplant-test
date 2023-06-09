from django.urls import path
from django.contrib.auth import views as a_views

from test_task.users import views

urlpatterns = [
    path('', views.UsersView.as_view(), name='users'),
    path('create/', views.UserRegister.as_view(), name='user_create'),
    path('<str:id>/update/', views.UserEdit.as_view(), name='user_edit'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.UserActivate.as_view(), name='activate'),
    path('<str:id>/', views.OneUserView.as_view(), name='user_see'),
]
