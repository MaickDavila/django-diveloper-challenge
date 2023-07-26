from .models import *
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PetSerializer(ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"


class ToySerializer(Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    purchase_url = serializers.URLField()
    pets = serializers.ListField()

    def create(self, validated_data):
        return Toy.objects.create(**validated_data)
