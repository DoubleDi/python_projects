import json
import logging

from kafka import KafkaConsumer, KafkaProducer
from psycopg2 import connect
from pydantic import BaseModel


class FileMessage(BaseModel):
    id: str
    url: str


logging.basicConfig(level=logging.INFO)


class Consumer:
    def __init__(self, topic_name, produce_topic_name, kafka_hosts, db_conn) -> None:
        self.consumer = KafkaConsumer(
            topic_name, bootstrap_servers=kafka_hosts, group_id="updating"
        )
        self.producer = KafkaProducer(bootstrap_servers=kafka_hosts)
        self.db = connect(db_conn)
        self.db.autocommit = True
        self.topic_name = topic_name
        self.produce_topic_name = produce_topic_name
        self.consumer.subscribe([self.topic_name])

    def consume_files(self):
        print("Consuming files")
        for message in self.consumer:
            print(f"Consuming message {message}")
            file_id = message.key.decode()
            payload = FileMessage(**json.loads(message.value.decode()))
            payload.url = "THIS IS A NEW URL"
            print(f"Sending new file {payload}")
            self.producer.send(
                self.produce_topic_name,
                key=file_id.encode(),
                value=payload.json().encode(),
            )


if __name__ == "__main__":
    consumer = Consumer(
        "test-topic",
        "test-topic-2",
        "localhost:9092",
        "postgres://postgres:postgres@127.0.0.1:5432/postgres",
    )

    consumer.consume_files()
