from django.urls import path
from users.administrator.views import MyTokenObtainPairView, register
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register, name="register"),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]