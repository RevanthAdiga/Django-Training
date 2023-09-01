from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bikeLists.models import BikeList
from bikeLists.serializers import BikeListSerializer


class BikeListAV(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        API to return all the bike lists

        """
        bikes = BikeList.objects.all()
        serializer = BikeListSerializer(bikes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        API to create a bike to the list

        """
        serializer = BikeListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BikeDetailAV(APIView):
    permission_classes = (IsAuthenticated,)

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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        API to delete a bike from the list

        """
        try:
            bike = BikeList.objects.get(pk=pk)
        except BikeList.DoesNotExist:
            return Response(
                {"error": "bike not found"}, status=status.HTTP_400_BAD_REQUEST
            )
        bike.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
