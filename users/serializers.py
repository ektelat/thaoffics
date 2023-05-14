from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    id_number = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False)
    profile_pic = serializers.ImageField(required=False)  # Add profile_pic field

    class Meta:
        model = User
        fields = ["id", "name", "email", "id_number", "address", "country_code", "phone_number", "password", "bio",
                  "profile_pic"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_id_number(self, value):
        if User.objects.filter(id_number=value).exists():
            raise serializers.ValidationError("This Identity number is already in use.")
        return value

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be a 10-digit number.")
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = True
        instance.is_phone_verified = False
        instance.is_email_verified = False
        instance.save()
        return instance
    def update(self, instance, validated_data):
        # Update the profile_pic field if it exists in the validated_data
        if 'profile_pic' in validated_data:
            instance.profile_pic = validated_data['profile_pic']

        # Update other fields if they exist in the validated_data
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.id_number = validated_data.get('id_number', instance.id_number)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.bio = validated_data.get('bio', instance.bio)

        # Save the updated instance
        instance.save()

        return instance

class ForgotPasswordSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    email = serializers.CharField()
    class Meta:
        model=User
        fields = ["name",'country_code','phone_number', 'email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields = ('id', 'name', 'permissions')
class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields = ('name', 'codename')