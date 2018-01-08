from django.db import models
from rest_framework import serializers

from cstasker.models import Person


class PersonSerializer(serializers.Serializer):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Person.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
