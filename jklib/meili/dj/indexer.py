# Built-in
from abc import ABC, abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    Unpack,
)

# Third-party
from meilisearch import Client

# Django
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet

# Application
from jklib.meili.search import build_search_filter
from jklib.meili.types import (
    MeilisearchFilters,
    MeilisearchSearchHits,
    MeilisearchSearchParameters,
    MeilisearchSearchResults,
    MeilisearchSettings,
)

if TYPE_CHECKING:
    # Django
    from django.db.models import Model


M = TypeVar("M", bound="Model")


class MeilisearchModelIndexer(ABC, Generic[M]):
    _meilisearch_client: Optional[Client] = None

    MODEL_CLASS: Type[M]
    PRIMARY_KEY = "id"
    SETTINGS: MeilisearchSettings

    @classmethod
    @abstractmethod
    def build_object(cls, instance: M) -> Dict[str, Any]:
        """Builds and returns the object to be indexed."""

    @classmethod
    @abstractmethod
    def index_name(cls) -> str:
        """Returns the index name."""

    # --------------------------------------------------
    # Index management
    # --------------------------------------------------
    @classmethod
    def index_exists(cls) -> bool:
        """Returns True if the index exists."""
        try:
            cls.meilisearch_client().get_index(cls.index_name())
            return True
        except Exception:  # noqa
            return False

    @classmethod
    def maybe_create_index(cls) -> None:
        """Creates the index if it doesn't exist."""
        client = cls.meilisearch_client()
        if not cls.index_exists():
            client.create_index(cls.index_name(), {"primaryKey": cls.PRIMARY_KEY})
        cls.update_settings()

    @classmethod
    def update_settings(cls) -> None:
        """Updates the index settings."""
        cls.meilisearch_client().index(cls.index_name()).update_settings(cls.SETTINGS)

    # --------------------------------------------------
    # Indexing
    # --------------------------------------------------
    @classmethod
    def index(cls, instance: M) -> None:
        """Indexes the model instance."""
        cls.index_multiple([instance])

    @classmethod
    def index_multiple(cls, instances: Union[List[M], QuerySet[M]]) -> None:
        """Indexes multiple model instances."""
        objects = [cls.build_object(instance) for instance in instances]
        cls.meilisearch_client().index(cls.index_name()).add_documents(objects)

    @classmethod
    def index_from_query(cls, query: Q) -> None:
        """Indexes all the instances matching the query."""
        cls._index_from_query(query, cls.index_name())

    @classmethod
    def index_all(cls) -> None:
        """Indexes all the instances of the model."""
        cls._index_from_query(Q(), cls.index_name())

    @classmethod
    def index_all_atomically(cls) -> None:
        """Indexes all the instances of the model atomically."""
        client = cls.meilisearch_client()
        # Create temporary index
        tmp_index_name = f"{cls.index_name()}_tmp"
        client.create_index(tmp_index_name, {"primaryKey": cls.PRIMARY_KEY})
        client.index(tmp_index_name).update_settings(cls.SETTINGS)
        # Index all objects on it
        cls._index_from_query(Q(), tmp_index_name)
        # Swap indexes and cleanup
        client.swap_indexes([{"indexes": [cls.index_name(), tmp_index_name]}])
        client.delete_index(tmp_index_name)

    @classmethod
    def unindex(cls, id_: int) -> None:
        """Deletes the instance from the index."""
        cls.unindex_multiple([id_])

    @classmethod
    def unindex_multiple(cls, ids: Union[List[int], List[str]]) -> None:
        """Deletes multiple instances from the index."""
        cls.meilisearch_client().index(cls.index_name()).delete_documents(ids)

    # --------------------------------------------------
    # Searching
    # --------------------------------------------------
    @classmethod
    def search(
        cls,
        query: str,
        only_hits: bool = False,
        filters: MeilisearchFilters = None,
        **params: Unpack[MeilisearchSearchParameters],
    ) -> Union[MeilisearchSearchHits, MeilisearchSearchResults]:
        filters = filters or {}
        params["filter"] = build_search_filter(**filters) or None
        response = (
            cls.meilisearch_client().index(cls.index_name()).search(query, params)
        )
        if only_hits:
            return {"hits": response["hits"]}
        return response

    # --------------------------------------------------
    # Utils
    # --------------------------------------------------
    @classmethod
    def meilisearch_client(cls) -> Client:
        """Returns the Meilisearch client. Cached property."""
        if cls._meilisearch_client is None:
            cls._meilisearch_client = Client(
                settings.MEILISEARCH_HOST, settings.MEILISEARCH_API_KEY
            )
        return cls._meilisearch_client

    # --------------------------------------------------
    # Private utils
    # --------------------------------------------------
    @classmethod
    def _index_from_query(cls, query: Q, index_name: str) -> None:
        """Indexes all the objects matching the query on the given index."""
        queryset = cls.MODEL_CLASS.objects.filter(query)
        paginator = Paginator(queryset, 500)
        for page in paginator.page_range:
            instances = paginator.page(page).object_list
            objects = [cls.build_object(instance) for instance in instances]
            if len(objects) > 0:
                cls.meilisearch_client().index(index_name).add_documents(objects)
