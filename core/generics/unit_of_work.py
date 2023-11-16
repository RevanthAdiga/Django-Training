from __future__ import annotations

import abc


class AbstractUnitOfWork(abc.ABC):
    def __init__(self, conn, trans) -> AbstractUnitOfWork:
        self.connection = conn
        self.transaction = trans

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class ORMModelUnitOfWork(AbstractUnitOfWork):
    def __init__(self, transaction, repository_object):
        self.repoObj = repository_object()
        self.transaction = transaction

    def __enter__(self):
        self.auto_commit_orig = self.transaction.get_autocommit()
        self.transaction.set_autocommit(False)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.transaction.set_autocommit(self.auto_commit_orig)

    def commit(self):
        self.transaction.commit()

    def rollback(self):
        self.transaction.rollback()

    def filter_by_id(self, id=None):
        return self.repoObj.get(id)
