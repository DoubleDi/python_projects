import logging
from parser import Entity

from elasticsearch import AsyncElasticsearch, helpers

logging.basicConfig(level=logging.INFO)


class ElasticSearchService:
    es = AsyncElasticsearch(
        "http://127.0.0.1:9200",
        basic_auth=("elastic", "123change"),
    )

    @classmethod
    async def create_index(cls):
        await cls.es.indices.create(
            index="test-index",
            mappings={
                "properties": {
                    "speckle_type": {"type": "keyword"},
                    "area": {"type": "double"},
                    "data": {"type": "flattened"},
                }
            },
        )

    @classmethod
    async def bulk_insert(cls, entities: list[Entity]):
        to_insert = []
        for e in entities:
            to_insert.append(e.model_dump())
            if len(to_insert) == 100:
                await helpers.async_bulk(
                    cls.es,
                    index="test-index",
                    actions=to_insert,
                )
                to_insert = []
            logging.info(f"Inserted {len(to_insert)} entities")

    @classmethod
    async def query_with_filter(cls, value: str):
        must = [
            {"term": {"speckle_type": "Objects.BuiltElements.Room"}},
            {"range": {"area": {"gt": 1.5}}},
        ]
        if value:
            must.append({"match": {"data": value}})
        return await cls.es.search(
            index="test-index",
            body={
                "query": {
                    "bool": {
                        "must": must,
                    },
                }
            },
        )

    @classmethod
    async def aggregate(cls):
        return await cls.es.search(
            index="test-index",
            body={
                "aggs": {
                    "min_area": {
                        "min": {
                            "field": "area",
                        }
                    },
                    "max_area": {
                        "max": {
                            "field": "area",
                        }
                    },
                }
            },
        )
