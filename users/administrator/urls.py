from django.urls import path
from users.administrator.views import MyTokenObtainPairView, retrieve_profile, forgot_password, change_password, register, check_pin, reset_password
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register, name="register"),
    path('forgot-password/', forgot_password, name="forgot_password"),
    path('check-pin/', check_pin, name="check_pin"),
    path('reset-password/', reset_password, name="reset_password"),
    path('change-password/', change_password, name="change_password"),
    path('profile/', retrieve_profile, name="retrieve_profile"),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]