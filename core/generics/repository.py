from abc import ABC, abstractmethod

from rest_framework.serializers import ValidationError


class AbstractRepository(ABC):
    """Abstracts the notion of an object/entity store."""

    def __init__(self, uow_man):
        self.uow = uow_man

    @abstractmethod
    def add(self, entity):
        """Insert a new entity into the data store."""
        raise NotImplementedError("add")

    @abstractmethod
    def delete(self, id):
        """Remove a persistent entity from the datastore."""
        raise NotImplementedError("delete")

    @abstractmethod
    def get(self, id):
        """Fetch an entity from the datastore by its identifier."""
        raise NotImplementedError("get")

    @abstractmethod
    def update(self, id):
        """Update an entity in the datastore by its identifier."""
        raise NotImplementedError("update")


class ORMModelRepository(AbstractRepository):
    def __init__(self, model_object):
        self._model = model_object.objects

    def add(self, entity):
        add_obj = self._model.create(**entity)
        return add_obj.pk

    def get(self, uid):
        return self._model.filter(id=uid).first()

    def getAll(self, **kwargs):
        return self._model.filter(**kwargs)

    def getRaw(self, query):
        return self._model.raw(query)

    def update(self, uid, entity):
        if self._model.filter(id=uid, active=True).first():
            self._model.filter(id=uid).update(**entity)
        else:
            raise ValidationError("cannot update inactive records")

    def delete(self, uid):
        if self._model.filter(id=uid).first():
            self._model.filter(id=uid).delete()
        else:
            raise ValidationError("cannot delete inactive records")
