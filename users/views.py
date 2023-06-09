import datetime
import random
import string
import jwt
from django.middleware.csrf import get_token
from django.core.cache import cache
from django.utils import timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, Permission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from twilio.rest import Client
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer, UserSerializer, GroupSerializer, \
    PermissionsSerializer
from users.models import User, PhoneVerification
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        group_name = request.data.get('group')
        if group_name == User.Groups.OWNER:
            group = Group.objects.get(name=User.Groups.OWNER)
            user.groups.add(group)
        elif group_name == User.Groups.STAFF:
            group = Group.objects.get(name=User.Groups.STAFF)
        elif group_name == User.Groups.CUSTOMER:
            group = Group.objects.get(name=User.Groups.CUSTOMER)
        else:
            return Response({'error': 'Invalid group name'}, status=400)
        user.groups.add(group)
        return Response({"status": 201}, status=status.HTTP_201_CREATED)


class PhoneVerificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        country_code = request.data.get('country_code')

        if not phone_number:
            return Response({'error': 'Please provide a phone number'}, status=400)
        # if request.user.is_phone_verified:
        #     return Response({'error': 'phone number is already Verified'}, status=400)
        if request.user.phone_number != phone_number:
            user2 = User.objects.filter(phone_number=phone_number).first()
            if user2 is not None:
                return Response({'error': 'phone number is already Used'}, status=400)
        verification = PhoneVerification.objects.filter(
            phone_number=phone_number
        ).order_by('-created_at').first()

        if (verification is None or verification.is_expired()):
            # Generate a random verification code
            verification_code = ''.join(random.choices(string.digits, k=6))
            # Send the verification code via SMS
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            # message = client.messages.create(
            #     messaging_service_sid='MG5dcdd5fa17649694daac41b499d3221d',
            #     body=f'Your verification code is: {verification_code}',
            #     to=f'whatsapp:{phone_number}'
            # )

            message = client.messages.create(
                from_='+972526936250',
                body=f'Your verification code is: {verification_code}',
                to=f'+{country_code}{phone_number}'

            )
            while message.status == 'queued':
                message = message.fetch()
            expires_in_minutes = getattr(settings, 'PHONE_VERIFICATION_EXPIRATION_MINUTES', 5)
            expires_at = timezone.now() + datetime.timedelta(minutes=expires_in_minutes)

            PhoneVerification.objects.create(
                phone_number=phone_number,
                verification_code=verification_code,
                expires_at=expires_at,
            )

            return Response({'success': 'Verification code sent successfully', "phone_number": phone_number}, status=200)
        else:
            remaining_time = verification.expires_at - datetime.datetime.now(timezone.utc)
            remaining_minutes = int(remaining_time.total_seconds() / 60)
            return Response(
                {
                    'msg': f'Sorry, we cannot resend the verification code yet. Please wait {remaining_minutes} minutes until the previous verification code expires and then try again. Thank you for your patience'},
                status=400)


class VerifyPhoneView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')
        user = request.user
        if not phone_number or not verification_code:
            return Response({'error': 'Please provide a phone number and a verification code'}, status=400)
        if user.is_phone_verified:
            return Response({'error': 'phone number is already Verified'}, status=400)
        verification = PhoneVerification.objects.filter(
            phone_number=phone_number
        ).order_by('-created_at').first()
        if verification and not verification.is_expired():
            verification.delete()
            if user.is_phone_verified:
                return Response({'error': 'phone number is already Verified'}, status=400)
            # Find the user with the matching phone number
            user.phone_number = phone_number
            # Set the user's is_active flag to True
            user.is_active = True
            user.is_phone_verified = True
            user.save()

            return Response({'success': 'Phone number verified successfully', "success": True}, status=200)
        else:
            return Response({'error': 'Invalid verification code', "success": False}, status=400)


class ResendVerificationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({'error': 'Please provide a phone number'}, status=400)

        if request.user.phone_number != phone_number:
            user2 = User.objects.filter(phone_number=phone_number).first()
            if user2 is not None:
                return Response({'error': 'phone number is already Used'}, status=400)

        verification = PhoneVerification.objects.filter(
            phone_number=phone_number
        ).order_by('-created_at').first()

        if (verification.is_expired()):
            verification_code = ''.join(random.choices(string.digits, k=6))
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            message = client.messages.create(
                from_='+972526936250',
                body=f'Your verification code is: {verification_code}',
                to=f'+{request.user.country_code}{phone_number}'

            )
            while message.status == 'queued':
                message = message.fetch()
            expires_in_minutes = getattr(settings, 'PHONE_VERIFICATION_EXPIRATION_MINUTES', 5)
            expires_at = timezone.now() + datetime.timedelta(minutes=expires_in_minutes)

            PhoneVerification.objects.create(
                phone_number=phone_number,
                verification_code=verification_code,
                expires_at=expires_at,
            )
            return Response(
                {'success': True, 'msg': 'Verification code Resent successfully', "phone_number": phone_number},
                status=200)
        else:
            remaining_time = verification.expires_at - datetime.datetime.now(timezone.utc)
            remaining_minutes = int(remaining_time.total_seconds() / 60)+1
            return Response(
                {'msg': f'Sorry, we cannot resend the verification code yet. Please wait {remaining_minutes} minutes until the previous verification code expires and then try again. Thank you for your patience'},
                status=400)


class LoginView(APIView):
    def post(self, request):
        token = get_token(request)
        phone_number = request.data['phone_number']
        password = request.data['password']
        user = User.objects.filter(phone_number=phone_number).first()
        group=Group.objects.filter(user=user).first()
        permissions=Permission.objects.filter(group=group);
        serializer = UserSerializer(user)
        if user is None:
            raise AuthenticationFailed("Sorry, we couldn't find that user. Please check the username and try again.")
        if not user.check_password(password):
            raise AuthenticationFailed(
                "Invalid login credentials. Please check your phone number and password and try again.")
        if not user.is_active:
            raise AuthenticationFailed(
                "Your account is currently disabled. Please contact customer support for assistance.")

        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        response = Response()
        groupSeriallezier=GroupSerializer(group)
        permissionsSeriallezier=PermissionsSerializer(instance=permissions, many=True)
        print(group,"======================?")
        response.data = {
            'access_token': str(access_token),
            'is_active': user.is_active,
            'refresh_token': str(refresh_token),
            'is_phone_verified': user.is_phone_verified,
            'user': serializer.data,
            'group':groupSeriallezier.data,
            'permissions':permissionsSeriallezier.data
        }
        return response


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed('Refresh token not found!')

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Refresh token has expired!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid refresh token!')

        user = User.objects.filter(id=payload['id']).first()
        if not user:
            raise AuthenticationFailed('User not found!')

        access_token_payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()

        response.data = {
            'access_token': access_token,
            'is_active': user.is_active,
            'is_phone_verified': user.is_phone_verified
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class TestView(APIView):
    def post(self, request, format=None):
        phone_number = request.data["phone_number"]
        user = User.objects.get(phone_number=phone_number)
        return Response(data={'message': 'Success!', "user": user.__str__()}, status=status.HTTP_200_OK)


password_reset_token = PasswordResetTokenGenerator()


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({'message': 'User with this phone number does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = password_reset_token.make_token(user)
            reset_password_url = settings.FRONTEND_URL + f'/auth/password/reset/confirm/{uidb64}/{token}/'
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                from_='+972526936250',
                body=f'Hello,You are receiving this message because you requested a password reset for your account.\nTo reset your password, please click on the link below:\n{reset_password_url}',
                to=f'+{serializer.validated_data.get("country_code")}{phone_number}'
            )
            while message.status == 'queued':
                message = message.fetch()

            return Response(
                {'message': 'sms  with instructions to reset your password has been sent.', "url": reset_password_url},
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer

    def get_user(self, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        print(user, uidb64, token)
        if user is not None and password_reset_token.check_token(user, token):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get('password')
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been successfully reset.'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Reset link is invalid.'}, status=status.HTTP_400_BAD_REQUEST)


