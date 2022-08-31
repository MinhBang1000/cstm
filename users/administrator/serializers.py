from datetime import date
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = get_user_model().USERNAME_FIELD

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [ 'email', 'password' ]

class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(
        required = True, 
        write_only = True
    )
    password_confirm = serializers.CharField(
        required = True, 
        write_only = True
    )
    dob = serializers.DateField(input_formats=['%d-%m-%Y',])
    phone_no = serializers.CharField(max_length = 10)

    def validate(self, data):
        if data["dob"] >= date.today():
            raise serializers.ValidationError("The day of birth must be set before nowadays! Please check them again.")
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("This confirm was not like password! Please check it again")
        # if len(data["phone_no"]) == 10 and data["phone_no"].isdigit():
        #     raise serializers.ValidationError("This phone number will be only numbers!")
        return data

    class Meta:
        model = get_user_model()
        fields = [ "email", "password", "password_confirm", "dob", "phone_no"]