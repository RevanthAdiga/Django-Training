from rest_framework import serializers

from bikeLists.models import BikeList


class BikeListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    company = serializers.CharField()

    def create(self, validated_data):
        return BikeList.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.company = validated_data.get("company", instance.company)
        instance.save()
        return instance
