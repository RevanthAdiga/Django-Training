from rest_framework import status
from rest_framework.response import Response

from bikeLists.serializers import BikeListSerializer
from core.generics.exceptions import MissingRequestParamsError, NoDataError
from core.generics.unit_of_work import AbstractUnitOfWork


def get_bikelist(uow: AbstractUnitOfWork, uid: int):
    with uow as unit_of_work:
        try:
            if uid == -1:
                bikelist = unit_of_work.repoObj.getAll()
                serializer = BikeListSerializer(bikelist, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                bike = unit_of_work.repoObj.get(uid)
                if not bike:
                    return Response(
                        {"error": str(NoDataError(uid))},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                serializer = BikeListSerializer(bike)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except MissingRequestParamsError("Bike id", uid) as error:
            return error


def add_bike(uow: AbstractUnitOfWork, data):
    with uow as unit_of_work:
        serializer = BikeListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            unit_of_work.commit()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_bikelist(uow: AbstractUnitOfWork, data, uid):
    with uow as unit_of_work:
        bike = unit_of_work.repoObj.get(uid)
        if not bike:
            return Response(
                {"data": " Bike Not Found"}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = BikeListSerializer(bike, data=data)
        if serializer.is_valid():
            serializer.save()
            unit_of_work.commit()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_bike(uow: AbstractUnitOfWork, uid):
    with uow as unit_of_work:
        bike = unit_of_work.repoObj.get(uid)
        if not bike:
            return Response(
                {"data": " bike Not Found"}, status=status.HTTP_400_BAD_REQUEST
            )
        unit_of_work.repoObj.delete(uid)
        unit_of_work.commit()
        return Response(
            {"data": " bike Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT
        )


def get_company_details(uow: AbstractUnitOfWork, uid: int):
    with uow as unit_of_work:
        try:
            if uid == -1:
                query_string = "SELECT * FROM 'bikeLists_companydetails'"
                company_details = unit_of_work.get_data_df(query_string, []).to_dict(
                    "records"
                )
                print(company_details)
                return Response(company_details, status=status.HTTP_200_OK)
            else:
                query_string = "SELECT * FROM 'bikeLists_companydetails' where id==%s"
                company_details = unit_of_work.get_data_df(query_string, [uid]).to_dict(
                    "records"
                )
                if len(company_details) == 0:
                    return Response(
                        {"error": str(NoDataError(uid))},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                return Response(company_details[0], status=status.HTTP_200_OK)
        except MissingRequestParamsError("company id", uid) as error:
            return error


def add_company_details(uow: AbstractUnitOfWork, data):
    with uow as unit_of_work:
        serializer = BikeListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            unit_of_work.commit()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def update_company_details(uow: AbstractUnitOfWork, data, uid):
    with uow as unit_of_work:
        company_details = unit_of_work.repoObj.get(uid)
        if not company_details:
            return Response(
                {"data": " company_details Not Found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = BikeListSerializer(company_details, data=data)
        if serializer.is_valid():
            serializer.save()
            unit_of_work.commit()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def delete_company_details(uow: AbstractUnitOfWork, uid):
    with uow as unit_of_work:
        company_details = unit_of_work.repoObj.get(uid)
        if not company_details:
            return Response(
                {"data": " company_details Not Found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        unit_of_work.repoObj.delete(uid)
        unit_of_work.commit()
        return Response(
            {"data": " company_details Deleted Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
