from django.contrib import admin
from django.urls import path
from auth_app.views import UserRegistrationView,LoginViewSet,UserProfileView,UserChangePasswordView,SendPasswordResetEmail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('login/',LoginViewSet.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('changepassword/',UserChangePasswordView.as_view(),name='changepassword'),
    path('resetpassword/',SendPasswordResetEmail.as_view(),name='send_reset-password-email'),
]
