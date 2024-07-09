from abc import ABC
from typing import Self
from src.storage.sql.storage import AbstractSQLAlchemyStorage
from sqlalchemy.ext.asyncio import AsyncSession


class SqlBaseRepository(ABC):
    storage: AbstractSQLAlchemyStorage

    def update_storage(self, storage: AbstractSQLAlchemyStorage) -> Self:
        self.storage = storage
        return self

    def _create_session(self) -> AsyncSession:
        return self.storage.create_session()
