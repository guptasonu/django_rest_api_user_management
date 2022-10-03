from rest_framework import serializers


def parameter_exists(request, key):
    if key not in request.data:
        raise serializers.ValidationError({key: {"message": f"{key} is required"}})
