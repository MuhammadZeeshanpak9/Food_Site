from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
 





class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('Email', 'Name', 'Gender', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        # Create the user using the manager method
        user = User.objects.create_user(
            Email=validated_data['Email'],
            Name=validated_data['Name'],
            Gender=validated_data['Gender'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    Email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('Email')
        password = data.get('password')

        user = authenticate(Email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        
        return {'user': user}
    
class UserProfileSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(read_only=True)  # Include admin status

    class Meta: 
        model = User
        fields = ['Email', 'Name', 'Gender', 'is_admin']    




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')
        
        user = self.context['request'].user
        
        # Check if old password is correct
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is incorrect."})
        
        # Check if new passwords match
        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "New passwords must match."})
        
        # Optionally: Add more validation here (e.g., password strength)
        
        return data

    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user        


########################  TO Reset Passwor Using Email   #######   All essetnial needed Things are below   ########


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings


##### For Password Reset ##########

class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        # Change 'email' to 'Email' because your model uses 'Email'
        if not User.objects.filter(Email=email).exists():
            raise serializers.ValidationError("No user is registered with this email")
        return attrs

    def save(self, **kwargs):
        user = User.objects.get(Email=self.validated_data['email'])  # Also change here
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"

        # Sending email
        send_mail(
            'Password Reset Request',
            f"Click the link to reset your password: {reset_link}",
            settings.EMAIL_HOST_USER,
            [user.Email],  # Change this to use 'Email' field
            fail_silently=False,
        )
        return reset_link


############## Confirming New Passwrod    #################

class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6, max_length=68)
    confirm_password = serializers.CharField(write_only=True, min_length=6, max_length=68)

    class Meta:
        fields = ['new_password', 'confirm_password']

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # Check if the passwords match
        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def save(self, uidb64, token):
        try:
            # Decode the user's ID
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # Validate the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('The reset link is invalid or has expired')

            # Set the new password
            user.set_password(self.validated_data['new_password'])
            user.save()

        except DjangoUnicodeDecodeError as e:
            raise serializers.ValidationError('The reset link is invalid or has expired')
        