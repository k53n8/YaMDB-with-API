from rest_framework import serializers


def usernamevalidator(value):
    if value == 'me':
        raise serializers.ValidationError('Запрещенный никнейм!')
    return value
