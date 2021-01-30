from django.contrib.auth.views import LogoutView
from django.urls import path

from authentication.views import LogInView
from authentication.views import SignupView


urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='sign_up'),
]
