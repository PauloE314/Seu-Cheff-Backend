from django.urls import path
from users import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login/', obtain_auth_token),
    path('teste/', views.Test.as_view()),
    path('', views.Users.as_view()),
    path('active-account/', views.ActiveAccount.as_view())
]
