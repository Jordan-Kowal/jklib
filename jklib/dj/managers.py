from typing import Iterable, List, Optional

from django.db.models import Manager, Model, QuerySet


class ImprovedManager(Manager):
    def __init__(
        self,
        allow_bulk: bool = True,
        select_related: Optional[Iterable[str]] = None,
        prefetch_related: Optional[Iterable[str]] = None,
    ):
        super().__init__()
        self.allow_bulk = allow_bulk
        self.select_related = select_related or []  # type: ignore
        self.prefetch_related = prefetch_related or []  # type: ignore

    def bulk_create(  # type: ignore
        self,
        objs: Iterable,
        batch_size: Optional[int] = None,
        ignore_conflicts: bool = False,
    ) -> List:
        if not self.allow_bulk:
            raise NotImplementedError
        return super().bulk_create(objs, batch_size, ignore_conflicts)

    def bulk_update(
        self, objs: Iterable, fields: Iterable[str], batch_size: Optional[int] = None
    ) -> int:
        if not self.allow_bulk:
            raise NotImplementedError
        return super().bulk_update(objs, fields, batch_size)

    def get_queryset(self) -> QuerySet["Model"]:
        queryset = super().get_queryset()
        if self.select_related:
            queryset = queryset.select_related(*self.select_related)  # type: ignore
        if self.prefetch_related:
            queryset = queryset.prefetch_related(*self.prefetch_related)  # type: ignore
        return queryset
