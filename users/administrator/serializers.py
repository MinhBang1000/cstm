from datetime import date
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import ResetCode

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = get_user_model().USERNAME_FIELD

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [ 'email', 'password' ]

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        required = True, 
        write_only = True
    )
    dob = serializers.DateField(input_formats=['%d-%m-%Y',])
    phone_no = serializers.CharField(max_length = 10)

    def validate(self, data):
        if data["dob"] >= date.today():
            raise serializers.ValidationError("The day of birth must be set before nowadays! Please check them again.")
        if str(data["phone_no"]).isdigit() == False:
            raise serializers.ValidationError("This phone number should be numbers!")
        return data

    class Meta:
        model = get_user_model()
        fields = [ "email", "password", "dob", "phone_no", "first_name", "last_name"]

class ForgotPasswordSerializer(serializers.ModelSerializer):
    code = serializers.StringRelatedField()
    
    class Meta:
        model = get_user_model()
        fields = [ "code" ]
    
class ResetCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetCode
        fields = ["code"]
        write_only_fields = ["code"]