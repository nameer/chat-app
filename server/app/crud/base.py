from enum import Enum
from functools import cached_property
from types import EllipsisType
from typing import Any, Self

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import ColumnElement, func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.base import ExecutableOption

from app.db.base_class import Base


class NotFoundError(Exception):
    pass


class SaveAction(Enum):
    # NOTE: the order is important
    NONE = "NONE"
    FLUSH = "FLUSH"
    COMMIT = "COMMIT"

    @cached_property
    def as_list(self) -> list[Self]:
        return list(self.__class__)

    def __gt__(self, other: Self) -> bool:
        _save_action_list = self.as_list
        return _save_action_list.index(self) > _save_action_list.index(other)


class CRUDBase[
    ModelType: Base,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
]():
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    @staticmethod
    def handle_session(session: Session, /, action: SaveAction) -> None:
        match action:
            case SaveAction.COMMIT:
                session.commit()
            case SaveAction.FLUSH:
                session.flush()
            case SaveAction.NONE:
                pass
            case _:  # pragma: no cover
                raise NotImplementedError

    def create(
        self,
        session: Session,
        /,
        obj_in: CreateSchemaType | dict[str, Any],
        *,
        action: SaveAction = SaveAction.COMMIT,
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        session_obj = self.model(**obj_in_data)
        session.add(session_obj)
        self.handle_session(session, action)
        if action > SaveAction.NONE:
            session.refresh(session_obj)
        return session_obj

    def create_multi(
        self,
        session: Session,
        /,
        objs_in: list[CreateSchemaType],
        *,
        action: SaveAction = SaveAction.COMMIT,
    ) -> list[ModelType]:
        objs_in_data = [jsonable_encoder(obj_in) for obj_in in objs_in]
        session_objs = [self.model(**obj_in_data) for obj_in_data in objs_in_data]
        session.add_all(session_objs)
        self.handle_session(session, action)
        return session_objs

    def get(
        self,
        session: Session,
        /,
        *,
        id: int | None = None,
        options: list[ExecutableOption] | None = None,
        filters: list[ColumnElement] | None = None,
    ) -> ModelType | None:
        filters = filters or []
        options = options or []
        if id is not None:
            filters.append(self.model.id == id)
        return session.scalars(
            select(self.model).where(*filters).options(*options)
        ).one_or_none()

    def get_multi(  # noqa: PLR0913
        self,
        session: Session,
        /,
        *,
        token: tuple[InstrumentedAttribute, Any] | None = None,
        limit: int | None = None,
        options: list[ExecutableOption] | None = None,
        ids: list[int] | None = None,
        filters: list[ColumnElement] | None = None,
        order_by: InstrumentedAttribute | None = None,
    ) -> tuple[list[ModelType], int]:
        options = options or []
        filters = filters or []
        if ids:
            filters.append(self.model.id.in_(ids))

        total_count = session.scalar(
            select(func.count()).select_from(self.model).where(*filters)
        )
        if limit == 0:
            # Avoid unnecessary database query.
            return [], total_count

        field, value = token
        if field and value:
            filters.append(field > value)

        stmt = select(self.model).where(*filters).options(*options)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        if limit:
            stmt = stmt.limit(limit)

        items = session.scalars(stmt).all()
        return items, total_count

    def get_count(
        self,
        session: Session,
        /,
        filters: list[ColumnElement] | None = None,
    ) -> int:
        _, count = self.get_multi(session, limit=0, filters=filters)
        return count

    def update(  # noqa: PLR0913
        self,
        session: Session,
        /,
        session_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        *,
        refresh_attributes: list[str] | EllipsisType | None = ...,
        action: SaveAction = SaveAction.COMMIT,
    ) -> ModelType:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_in.items():
            if hasattr(session_obj, field):
                setattr(session_obj, field, value)
        session.add(session_obj)
        self.handle_session(session, action)

        if refresh_attributes is None:
            refresh_attributes = []
        elif refresh_attributes is Ellipsis:
            refresh_attributes = None
        session.refresh(session_obj, attribute_names=refresh_attributes)

        return session_obj

    def remove(
        self,
        session: Session,
        id_or_obj: int | ModelType,
        /,
        *,
        action: SaveAction = SaveAction.COMMIT,
    ) -> None:
        obj = self.get(session, id_or_obj) if isinstance(id_or_obj, int) else id_or_obj
        if not obj:
            raise NotFoundError
        session.delete(obj)
        self.handle_session(session, action)

    def remove_multi(
        self,
        session: Session,
        /,
        objs: list[ModelType],
        *,
        action: SaveAction = SaveAction.COMMIT,
    ) -> None:
        for obj in objs:
            session.delete(obj)
        self.handle_session(session, action=action)
