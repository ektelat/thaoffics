from abc import ABC

from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","name", "email", "phone_number", "password", "bio"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

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


class ForgotPasswordSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    email = serializers.CharField()
    class Meta:
        model=User
        fields = ["name", 'phone_number', 'email']


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password']
