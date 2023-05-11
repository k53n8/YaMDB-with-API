from rest_framework import serializers


def UsernameMinSymbolLimit(value):
    if len(value) < 4:
        raise serializers.ValidationError('Минимум четыре символа!')
