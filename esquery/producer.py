import logging
from time import sleep
from uuid import uuid4

from kafka import KafkaProducer
from psycopg2 import connect
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)


class FileMessage(BaseModel):
    id: str
    url: str


class Producer:
    def __init__(self, topic_name, kafka_hosts, db_conn) -> None:
        self.producer = KafkaProducer(bootstrap_servers=kafka_hosts)
        self.db = connect(db_conn)
        self.db.autocommit = True
        self.topic_name = topic_name

    def produce_file(self) -> str:
        file_id = str(uuid4())
        self.db.cursor().execute(
            "insert into file_processing_queue (id, status) values (%s, 'STARTED') on conflict (id) do update set status = 'STARTED'",
            (file_id,),
        )
        self.producer.send(
            self.topic_name,
            key=file_id.encode(),
            value=FileMessage(
                id=file_id,
                url="https://api.thecatapi.com/v1/images/search?limit=1&has_breeds=1&api_key=live_woC2cOByClEMmW9qTc8THyh55wPJANTQuTLG0kHSeRhE0ERv2k4N6VnNRG987kfU",
            )
            .json()
            .encode(),
        )
        self.producer.flush()
        return file_id


if __name__ == "__main__":
    producer = Producer(
        "test-topic",
        "localhost:9092",
        "postgres://postgres:postgres@127.0.0.1:5432/postgres",
    )

    while True:
        for i in range(100):
            file = producer.produce_file()
            logging.info(f"Produced file {file}")
        sleep(10)
