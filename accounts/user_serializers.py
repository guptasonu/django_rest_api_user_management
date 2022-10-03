from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers
from accounts import request_validators

from accounts import models as account_models


class BasicAuthenticationSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            try:
                validate_email(email)
            except ValidationError:
                msg = "Email is not valid"
                raise serializers.ValidationError(msg, code="authorization")
            user = authenticate(username=email, password=password)

            if user:
                user = account_models.User.objects.filter(username=email)
                if not user.exists():
                    msg = "Unable to log in with provided credentials."
                    raise serializers.ValidationError(msg, code="authorization")
            else:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop("exclude_fields", None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            # for multiple fields in a list
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = account_models.User
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "notes",
        )
        extra_kwargs = {
            "created": {"read_only": True},
            "id": {"read_only": True},
            "username": {"write_only": True},
            "password": {"write_only": True},
            "email": {"read_only": True},
        }

    def validate(self, attrs):
        request = self.context["request"]
        request_validators.parameter_exists(request, "first_name")
        request_validators.parameter_exists(request, "last_name")

        if (
            request.data.get("username")
            and request.data.get("password")
            and request.data.get("first_name")
            and request.data.get("last_name")
        ):
            try:
                validate_email(request.data.get("username"))
            except ValidationError:
                msg = "Username is not valid"
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "username" , "password","first_name" and "last_name".'
            raise serializers.ValidationError(msg, code="authorization")

        return attrs

    def create(self, validated_data):
        user = account_models.User.objects.create_user(
            email=validated_data.get("username"), **validated_data
        )

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop("exclude_fields", None)
        super(UpdateUserSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            # for multiple fields in a list
            for field_name in remove_fields:
                self.fields.pop(field_name)

    class Meta:
        model = account_models.User
        fields = ("id", "username", "first_name", "last_name", "email", "notes")
        extra_kwargs = {
            "id": {"read_only": True},
            "username": {"read_only": True},
            "password": {"read_only": True},
            "email": {"read_only": True},
        }

    def update(self, instance, validated_data):
        request = self.context["request"]

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if "email" in request.data:
            if account_models.User.objects.filter(
                username=request.data.get("email")
            ).exists():
                pass
            elif instance.email != request.data.get("email"):
                instance.username = request.data.get("email")
                instance.email = request.data.get("email")
        if "password" in request.data:
            instance.set_password(request.data.get("password"))
        instance.save()
        return instance
