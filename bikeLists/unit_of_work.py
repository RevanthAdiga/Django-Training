import pandas as pd

from bikeLists.repository import (
    BikeRepository,
    CompanyDetailsRepository,
    ReviewRepository,
)
from core.generics.unit_of_work import ORMModelUnitOfWork


class CompanyDetailsUnitOfWork(ORMModelUnitOfWork):
    def __init__(self, trans):
        super(CompanyDetailsUnitOfWork, self).__init__(trans, CompanyDetailsRepository)

    def raw_queryset_as_values_list(self, raw_qs):
        columns = raw_qs.columns
        for row in raw_qs:
            yield tuple(getattr(row, col) for col in columns)

    def get_data_df(self, query_string, params):
        results = self.repoObj._model.raw(query_string, params)
        return pd.DataFrame(
            self.raw_queryset_as_values_list(results), columns=list(results.columns)
        )


class BikesUnitOfWork(ORMModelUnitOfWork):
    def __init__(self, trans):
        super(BikesUnitOfWork, self).__init__(trans, BikeRepository)


class ReviewUnitOfWork(ORMModelUnitOfWork):
    def __init__(self, trans):
        super(ReviewUnitOfWork, self).__init__(trans, ReviewRepository)
