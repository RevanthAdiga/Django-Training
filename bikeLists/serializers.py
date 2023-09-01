from rest_framework import serializers

from bikeLists.models import BikeList


class BikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BikeList
        fields = "__all__"
