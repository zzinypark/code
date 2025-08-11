from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers

User = get_user_model()


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user = User(**data)
        errors = dict()
        try:
            validate_password(password=data["password"], user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super().validate(data)

    def create(self, validated_data):
        user = User(**validated_data)

        user.set_password(validated_data["password"])
        user.save()
        return user
