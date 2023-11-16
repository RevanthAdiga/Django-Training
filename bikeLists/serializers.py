from rest_framework import serializers

from bikeLists.models import Bike, CompanyDetails, Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        exclude = ("bikelist",)


class BikeListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    company = serializers.CharField(read_only=True, source="company_details.company")

    class Meta:
        model = Bike
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    bikelist = BikeListSerializer(many=True, read_only=True)

    class Meta:
        model = CompanyDetails
        fields = "__all__"
