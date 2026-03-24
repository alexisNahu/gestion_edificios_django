from abc import ABC, abstractmethod
from typing import List, Optional, Type, TypeVar, Generic
from django.db import models

T = TypeVar('T', bound=models.Model)

class IRepository(ABC, Generic[T]):
    _table: str = ""
    _model: Type[T] = None
    _objects: models.Manager = None

    @abstractmethod
    async def select(self, **kwargs) -> List[T]: pass

    @abstractmethod
    async def create(self, **kwargs) -> T: pass

    @abstractmethod
    async def update(self, id: int, **kwargs) -> Optional[T]: pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> bool: pass