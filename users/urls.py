from django.urls import path, re_path, include, reverse_lazy
from rest_framework.routers import DefaultRouter
from users.views import Register, LoginView, UserView, LogoutView, TestView, PhoneVerificationView, VerifyPhoneView, \
    ForgotPasswordView, ResetPasswordView, RefreshTokenView

urlpatterns = [
    path("register", Register.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('test', TestView.as_view()),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('verify_phone/', PhoneVerificationView.as_view(), name='verify_phone'),
    path('verify_phone/check/', VerifyPhoneView.as_view(), name='verify_phone_check'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/', ResetPasswordView.as_view(), name='reset_password'),

]
