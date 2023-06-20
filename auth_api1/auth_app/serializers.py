from rest_framework import serializers
from auth_app.models import User
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.utils.encoding import smart_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        # data["username"]=self.user.username
        # data["is_student"]=self.user.is_student
        data["email"]=self.user.email
        # data["phone"] = self.user.phone
        data["firstname"]=self.user.name
        # data["lastname"]=self.user.lastname


        return data
class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'}
    , write_only=True)
    class Meta:
        model = User
        fields='__all__'
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.pop('password2')
        print(password2)
        if password!=password2:
            raise serializers.ValidationError("Password and conformPassword doesn't match")
        return attrs
    def create(self,validate_data):
        return User.objects.create_user(**validate_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    # def validate(self,attrs )

class SendPasswordResetEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields=['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid) 
            token=PasswordResetTokenGenerator().make_token(user)
            print('password Reset Token ',token)
            link='http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link',link)
            return attrs
        else:
            raise ValidationError('You are not Registered User')

class UserPasswordResetSerializers(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Please Enter Same Password")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)   
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token Is Not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs        
        
        except Exception as ex:
            PasswordResetTokenGenerator

 