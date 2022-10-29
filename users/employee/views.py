# Rest Framework
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status, permissions


# Django 
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

# Library Python
import random 
import string

# Customize
from users.employee.serializers import ProfileSerializer, ResetCodeSerializer, ForgotPasswordSerializer, MyTokenObtainPairSerializer, RegisterSerializer
from users.models import ResetCode 
from bases import errors, views as base_views
from roles.models import Role
from userpermissions.models import UserPermission


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(["POST"])
@permission_classes([])
def create_admin(request):
    data = request.data
    # Check email exists
    try:
        user = get_user_model().objects.get(email=request.data["email"])
    except:
        user = None
    finally:
        if user:
            raise ValidationError(errors.get_error(errors.EMAIL_EXSITS))
    # Check password and confirm 
    if data["password"] != data["password_confirm"]:
        raise ValidationError(errors.get_error(errors.PASSWORD_CONFIRM))
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = get_user_model().objects.create_user(**serializer.validated_data)
    user.set_password(data["password"])
    user.profile_code = base_views.base64_encoding(user.email)
    # Create permissions for new user
    user.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def register(request):
    data = request.data
    role = data.get("role", None)
    # Can't create user with administrator role
    if role == 1 or role == None:
        raise ValidationError(errors.get_error(errors.INVALID_ROLE))
    # Check creater 's role
    creater = request.user
    if creater.role.id == 1: # Administrator
        if role not in [2,3,4,5]:
            raise ValidationError(errors.get_error(errors.NOT_CREATE_USER_ROLE))
    elif creater.role.id == 2: # Owner
        if role not in [3,4,5]:
            raise ValidationError(errors.get_error(errors.NOT_CREATE_USER_ROLE))
    elif creater.role.id == 3: # Branch Manager
        if role not in [4,5]:
            raise ValidationError(errors.get_error(errors.NOT_CREATE_USER_ROLE))
    elif creater.role.id == 4: # Storage Manager
        if role not in [5]:
            raise ValidationError(errors.get_error(errors.NOT_CREATE_USER_ROLE))
    else:   # Supervisor
        raise ValidationError(errors.get_error(errors.NOT_CREATE_USER_ROLE))
    # Check email exists
    try:
        user = get_user_model().objects.get(email=request.data["email"])
    except:
        user = None
    finally:
        if user:
            raise ValidationError(errors.get_error(errors.EMAIL_EXSITS))
    # Check password and confirm 
    if data["password"] != data["password_confirm"]:
        raise ValidationError(errors.get_error(errors.PASSWORD_CONFIRM))
    serializer = RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    user = get_user_model().objects.create_user(**serializer.validated_data)
    user.set_password(data["password"])
    user.profile_code = base_views.base64_encoding(user.email)
    # Creater ID
    user.employer = creater.id
    # Supervisor of
    if creater.role.id < 5 and role == 5:
        if data.get('supervisor_of', None) == None:
            raise ValidationError(errors.get_error(errors.HAVE_STORAGE_ID_SUPERVISOR_OF))
        else:
            user.supervisor_of = data["supervisor_of"]
    # Create permissions for new user
    permissions = user.role.role_permissions.all()
    for permission in permissions:
        UserPermission.objects.create(person=user, permission=permission)
    user.save()
    return Response(status=status.HTTP_201_CREATED)

@api_view(["POST"])
def forgot_password(request):
    email = request.data["email"]
    try:
        user = get_user_model().objects.get(email=email)
        serializer = ForgotPasswordSerializer(user)
    except get_user_model().DoesNotExists:
        raise ValidationError(errors.get_error(errors.EMAIL_NOT_EXISTS))
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
        raise ValidationError(errors.get_error(errors.EMAIL_NOT_SENT))
    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def check_pin(request):
    if request.data["code"]:
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
        raise ValidationError(errors.get_error(errors.PASSWORD_CONFIRM))
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
    # Must be check have all of fields you need 
    if user.check_password(request.data["password_old"]) == False:
        raise ValidationError(errors.get_error(errors.OLD_PASSWORD_INCORRECT))
    if request.data["password"] != request.data["password_confirm"]:
        raise ValidationError(errors.get_error(errors.PASSWORD_CONFIRM))
    user.set_password(request.data["password"])
    user.save()
    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def retrieve_profile(request):
    serializer = ProfileSerializer(instance=request.user)
    return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def increase_permission(request):
    user = request.user
    user.is_superuser = True
    user.role = Role.objects.get(pk=1)
    user.is_staff = True
    user.save()
    return Response(status=status.HTTP_200_OK)
