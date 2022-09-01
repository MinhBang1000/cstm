from rest_framework_simplejwt.views import TokenObtainPairView
from users.administrator.serializers import ResetCodeSerializer, ForgotPasswordSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import random 
import string
from django.shortcuts import get_object_or_404

from users.models import ResetCode 

# Login and Refresh Token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Registering user
@api_view(["POST"])
def register(request):
    data = request.data
    if get_user_model().objects.get(email=request.data["email"]):
        raise ValidationError({"error" : "This email have already exists! Please choose another"})
    if data["password"] != data["password_confirm"]:
        raise ValidationError("Both password and confirm was not same! Please check it again")
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = get_user_model().objects.create_user(**serializer.validated_data)
    user.set_password(data["password"])
    user.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
def forgot_password(request):
    email = request.data["email"]
    try:
        user = get_user_model().objects.get(email=email)
        serializer = ForgotPasswordSerializer(user)
    except get_user_model().DoesNotExists:
        raise ValidationError("Haven't exists user follow this email! Please check them again")
    subject = "Cold Storage - Forgot Password Services"
    receivers = [ email, ]
    email_from = settings.EMAIL_HOST_USER
    if serializer.data["code"]:
        reset_code = serializer.data["code"]
    else:
        character = string.digits
        reset_code = ''.join(random.choice(character) for i in range(6))
        reset_serializer = ResetCodeSerializer(data={"code": reset_code})
        reset_serializer.is_valid(raise_exception=True)
        reset_serializer.save(user=user)
    message = reset_code
    try:
        send_mail(subject=subject, message=message, recipient_list=receivers, from_email=email_from)
    except Exception:
        raise ValidationError("Something went wrong! Can't send email")
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def check_pin(request):
    if request.data["code"]:
        # Forgot password to change
        user = get_object_or_404(get_user_model(),email=request.data["email"])
        serializer = ForgotPasswordSerializer(user)
        if serializer.data["code"] == request.data["code"]:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def reset_password(request):
    user = get_object_or_404(get_user_model(),email=request.data["email"])
    if request.data["password"] != request.data["password_confirm"]:
        raise ValidationError("Both password and confirm are not same!")
    serializer = ForgotPasswordSerializer(user)
    if serializer.data["code"] == request.data["code"]:
        code = ResetCode.objects.get(user=user)
        code.delete()
        user.set_password(request.data["password"])
        user.save()
        return Response(status=status.HTTP_200_OK)
    raise ValidationError("PIN was not correct!")

@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def change_password(request):
    user = request.user
    if request.data["password"] != request.data["password_confirm"]:
        raise ValidationError("Both password and confirm are not same!")
    user.set_password(request.data["password"])
    user.save()
    return Response(status=status.HTTP_200_OK)
