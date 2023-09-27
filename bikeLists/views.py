import structlog
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, mixins, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bikeLists.models import BikeList, CompanyDetails, Review
from bikeLists.permissions import AdminOrReadOnly, ReviewUserOrReadOnly
from bikeLists.serializers import (
    BikeListSerializer,
    CompanySerializer,
    ReviewSerializer,
)

logger = structlog.get_logger(__name__)


@extend_schema_view(
    request=ReviewSerializer,
    responses={201: ReviewSerializer},
)
class ReviewList(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    logger.bind(
        app_name="bikelists",
        method_name="get_list_of_reviews",
        serializer=serializer_class,
    )

    def get_queryset(self):
        """API to return reviews respect to specific bike

        Parameter type- integer"""

        pk = self.kwargs["pk"]

        return Review.objects.filter(bikelist=pk)


@extend_schema_view(
    request=ReviewSerializer,
    responses={201: ReviewSerializer},
)
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    logger.bind(
        app_name="bikelists",
        method_name="create review",
        serializer=serializer_class,
    )

    def perform_create(self, serializer):
        """API to create the review based on the id of the provided.

        Raises:
            ValidationError: Same user cannot create multiple reviews
        """
        pk = self.kwargs["pk"]
        bikelist = BikeList.objects.get(pk=pk)
        reviewer = self.request.user
        review_queryset = Review.objects.filter(bikelist=bikelist, reviewer=reviewer)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this!!")

        if bikelist.number_of_rating == 0:
            bikelist.avg_rating = serializer.validated_data["rating"]

        else:
            bikelist.avg_rating = (
                (bikelist.avg_rating * bikelist.number_of_rating)
                + serializer.validated_data["rating"]
            ) / (1 + bikelist.number_of_rating)
        bikelist.number_of_rating += 1
        bikelist.save()
        serializer.save(bikelist=bikelist, reviewer=reviewer)


@extend_schema_view(
    description="List particular zone that a dish can be classified.",
    parameters=[
        OpenApiParameter(
            "pk",
            OpenApiTypes.INT,
            OpenApiParameter.PATH,
            examples=[
                OpenApiExample(
                    "Review Id",
                    summary="fetches, updates, deletes review based on primary id",
                    description="should be a integer value",
                    value=1,
                )
            ],
        )
    ],
)
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):

    """
    APIs to retrieve , update and destroy the review.

    Permissions: only the user who has reviewed or the admin user can edit the review.

    Parameter type- integer

    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    logger.bind(
        app_name="bikelists",
        method_name="retirieve update and delete review",
        serializer=serializer_class,
    )
    permission_classes = [ReviewUserOrReadOnly, AdminOrReadOnly]


class BikeListAV(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={201: BikeListSerializer},
    )
    def get(self, request):
        """
        API to return all the bike lists

        """
        bikes = BikeList.objects.all()
        serializer = BikeListSerializer(bikes, many=True)
        logger.bind(
            app_name="bikelists",
            method_name="get_list_of_bikes",
            serializer=serializer,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=BikeListSerializer,
        responses={201: BikeListSerializer},
    )
    def post(self, request):
        """
        API to create a bike to the list

        """
        serializer = BikeListSerializer(data=request.data)
        logger.bind(
            app_name="bikelists",
            method_name="upload bike object to list",
            serializer=serializer,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BikeDetailAV(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses=BikeListSerializer,
        description="List particular zone that a dish can be classified.",
        parameters=[
            OpenApiParameter(
                "pk",
                OpenApiTypes.INT,
                OpenApiParameter.PATH,
                examples=[
                    OpenApiExample(
                        "Bikelist Id",
                        summary="fetches, updates, deletes bikes based on primary id",
                        description="should be a integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request, pk):
        """
        API to get a bike from the list

        """
        try:
            bike = BikeList.objects.get(pk=pk)
        except BikeList.DoesNotExist:
            return Response(
                {"error": "bike not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BikeListSerializer(bike)
        logger.bind(
            app_name="bikelists",
            method_name="retrieve a bike from the list",
            serializer=serializer,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        API to update a bike into the list

        """
        try:
            bike = BikeList.objects.get(pk=pk)
        except BikeList.DoesNotExist:
            return Response(
                {"error": "bike not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BikeListSerializer(bike, data=request.data)
        logger.bind(
            app_name="bikelists",
            method_name="update a bike into the list",
            serializer=serializer,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        API to delete a bike from the list

        """
        logger.bind(
            app_name="bikelists",
            method_name="delete a bike from the list",
        )
        try:
            bike = BikeList.objects.get(pk=pk)
        except BikeList.DoesNotExist:
            return Response(
                {"error": "bike not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        bike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    request=CompanySerializer,
    responses=CompanySerializer,
    parameters=[
        OpenApiParameter(
            "pk",
            OpenApiTypes.INT,
            OpenApiParameter.PATH,
            examples=[
                OpenApiExample(
                    "Company id",
                    summary="fetches companies based on  primary id",
                    description="should be a integer value",
                    value=1,
                )
            ],
        )
    ],
)
class Company(viewsets.ModelViewSet):
    """API to GET, PUT, DELETE, POST and Retrieve company details"""

    queryset = CompanyDetails.objects.all()
    serializer_class = CompanySerializer
    logger.bind(
        app_name="bikelists",
        method_name="get_put_delete_post methods on company model",
        serializer=serializer_class,
    )
