from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from auth_app.serializers import MyTokenObtainPairSerializer  ,UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializers,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializers
from auth_app.renderers import UserRenderer
# from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import ListCreateAPIView
from auth_app.models import User
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
     refresh=RefreshToken.for_user(user)

     return {
          'refresh':str(refresh),
          'access':str(refresh.access_token),
     }

class UserRegistrationView(ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserRegistrationSerializer
    
    # permission_classes=[IsAuthenticated]

class LoginViewSet(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# class UserLoginView(APIView):
#     def post(self,request,format=None):
#         serializer=UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email=serializer.data.get('email')
#             password=serializer.data.get('password')
#             user=authenticate(email=email,password=password)
#             if user is not None:
#                 token=get_tokens_for_user(user)
#                 return Response({'token':token, 'msg':'Login Successful'},status=status.HTTP_200_OK)
#             else:
#                 return Response({'errors':{'non_field_errors':["Email and Password is not valid"]}},status=status.HTTP_200_OK)

class UserProfileView(APIView):
    #  renderer_classes=[UserRenderer]
     permission_classes=[IsAuthenticated]
     def get(self,request,format=None):
        print(request.user)
        serializer=UserProfileSerializers(request.user)
        # if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_200_OK)
# class ShowdataViews(APIView):

#     def get(self, request):
#             print()
#             if "id" in request.data:
#                 try:
#                     user = User.objects.get(id=request.data['id'])
#                     serializer = UserRegistrationSerializer(instance=user)
#                     return Response(serializer.data)
#                 except User.DoesNotExist:
#                         return Response("User not found.", 400)
#             else:
#                 try:
#                     user = User.objects.all()
#                     serializer = UserRegistrationSerializer(instance=user,many=True)
#                     return Response(serializer.data)
#                 except User.DoesNotExist:
#                     return Response("User not found.", 400)

class UserChangePasswordView(APIView):
    renderer_classes=[UserRenderer]
    
    def post(self,request,format=None):
        serializer=UserChangePasswordSerializer(data=request.data,context={'user'.request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)  
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class SendPasswordResetEmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,format=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset link sended Please Cheak Your Email' },status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserPasswordResetView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request,uid,token,format=None):
        serializer=UserPasswordResetSerializers(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Successfully'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response()












