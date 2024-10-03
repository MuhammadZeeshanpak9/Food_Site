from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from .serializers import ChangePasswordSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .serializers import RequestPasswordResetSerializer
from rest_framework import status
from rest_framework import serializers





##Creating manually TOKEN
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Create your views here.
class UserReg(APIView):
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg': 'User registered successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('Email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials.')

        # Check if the user is admin
        if not user.is_admin:
            return Response({'error': 'Only admins can log in.'}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT token for admin user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Get the user profile
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        # Update the user profile
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   


class ChangePasswordView(APIView):
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Calls the save method defined in the serializer
            return Response({'msg': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
############3 Reset Password Using Email ############
from .serializers import RequestPasswordResetSerializer,SetNewPasswordSerializer

class RequestPasswordResetView(APIView):
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'success': 'Password reset link sent to your email'}, status=status.HTTP_200_OK)
    
class SetNewPasswordView(APIView):
    def post(self, request, uidb64, token):
        serializer = SetNewPasswordSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Passing the UID and token to the serializer to handle validation
                serializer.save(uidb64=uidb64, token=token)
                return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
            except serializers.ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



