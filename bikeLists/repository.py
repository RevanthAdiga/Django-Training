from bikeLists.models import Bike, CompanyDetails, Review
from core.generics.repository import ORMModelRepository


class ReviewRepository(ORMModelRepository):
    def __init__(self):
        super(ReviewRepository, self).__init__(Review)


class BikeRepository(ORMModelRepository):
    def __init__(self):
        super(BikeRepository, self).__init__(Bike)


class CompanyDetailsRepository(ORMModelRepository):
    def __init__(self):
        super(CompanyDetailsRepository, self).__init__(CompanyDetails)
