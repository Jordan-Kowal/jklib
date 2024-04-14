# Built-in
from time import sleep
from typing import Generic, Type, TypeVar

# Third-party
from meilisearch import Client

# Django
from django.db.models import Model, Q
from django.test import tag

# Application
from jklib.meili.dj.indexer import MeilisearchModelIndexer

SLEEP_TIME = 0.07

M = TypeVar("M", bound=Model)


@tag("integration")
class IndexerBaseTestMixin(Generic[M]):
    """
    Base test mixin for testing MeilisearchModelIndexer subclasses.

    Make sure `index_name` is mocked in the setUp method.

    Provides tests for all methods from MeilisearchModelIndexer
    except `build_object` and `index_name`.
    """

    meilisearch_client: Client

    indexer_class: Type[MeilisearchModelIndexer]
    item_1: M
    item_2: M
    search_attribute: str

    def setUp(self):
        super().setUp()
        self.meilisearch_client.delete_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)

    def tearDown(self):
        self.meilisearch_client.delete_index(self.indexer_class.index_name())
        super().tearDown()

    def test_index_exists(self) -> None:
        self.assertFalse(self.indexer_class.index_exists())
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        self.assertTrue(self.indexer_class.index_exists())

    def test_maybe_create_index(self) -> None:
        self.assertFalse(self.indexer_class.index_exists())
        self.indexer_class.maybe_create_index()
        sleep(SLEEP_TIME)
        self.assertTrue(self.indexer_class.index_exists())

    def test_update_settings(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        self.indexer_class.update_settings()
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).get_settings()
        for key, value in self.indexer_class.SETTINGS.items():
            self.assertEqual(response[key], value)

    def test_index(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search(getattr(self.item_1, self.search_attribute))
        self.assertSearchHits(response, [])
        self.indexer_class.index(self.item_1)
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search(getattr(self.item_1, self.search_attribute))
        self.assertSearchHits(response, [self.item_1])

    def test_index_multiple(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [])
        self.indexer_class.index_multiple([self.item_1, self.item_2])
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [self.item_1, self.item_2])

    def test_index_from_query(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search(getattr(self.item_1, self.search_attribute))
        self.assertSearchHits(response, [])
        self.indexer_class.index_from_query(Q(id=self.item_1.id))
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search(getattr(self.item_1, self.search_attribute))
        self.assertSearchHits(response, [self.item_1])

    def test_index_all(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [])
        self.indexer_class.index_all()
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [self.item_1, self.item_2])

    def test_index_all_atomically(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertEqual(response["hits"], [])
        self.indexer_class.index_all_atomically()
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [self.item_1, self.item_2])

    def test_unindex(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        self.indexer_class.index(self.item_1)
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search(getattr(self.item_1, self.search_attribute))
        self.assertSearchHits(response, [self.item_1])
        self.indexer_class.unindex(self.item_1.id)
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search(getattr(self.item_1, self.search_attribute))
        self.assertSearchHits(response, [])

    def test_unindex_multiple(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        sleep(SLEEP_TIME)
        self.indexer_class.index_multiple([self.item_1, self.item_2])
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [self.item_1, self.item_2])
        self.indexer_class.unindex_multiple([self.item_1.id, self.item_2.id])
        sleep(SLEEP_TIME)
        response = self.meilisearch_client.index(
            self.indexer_class.index_name()
        ).search("")
        self.assertSearchHits(response, [])

    def test_search(self) -> None:
        self.meilisearch_client.create_index(self.indexer_class.index_name())
        search_value = getattr(self.item_1, self.search_attribute)
        sleep(SLEEP_TIME)
        response = self.indexer_class.search(search_value)
        self.assertSearchHits(response, [])
        self.indexer_class.index(self.item_1)
        sleep(SLEEP_TIME)
        response = self.indexer_class.search(search_value)
        self.assertSearchHits(response, [self.item_1])
        self.assertEqual(response.get("limit"), 20)
        response = self.indexer_class.search(search_value, limit=1)
        self.assertSearchHits(response, [self.item_1])
        self.assertEqual(response.get("limit"), 1)
        response = self.indexer_class.search(search_value, only_hits=True, limit=1)
        self.assertSearchHits(response, [self.item_1])
        self.assertNotIn("limit", response)

    def test_meilisearch_client(self) -> None:
        self.assertIsInstance(self.indexer_class.meilisearch_client(), Client)

    def assertSearchHits(self, response, items):
        ids = {hit["id"] for hit in response["hits"]}
        self.assertSetEqual(
            ids, {getattr(item, self.indexer_class.PRIMARY_KEY) for item in items}
        )
