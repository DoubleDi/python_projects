import json
import logging

import requests
from kafka import KafkaConsumer
from psycopg2 import connect
from pydantic import BaseModel


class FileMessage(BaseModel):
    id: str
    url: str


logging.basicConfig(level=logging.INFO)


class Consumer:
    def __init__(self, topic_name, kafka_hosts, db_conn) -> None:
        self.consumer = KafkaConsumer(
            topic_name, bootstrap_servers=kafka_hosts, group_id="downloading"
        )
        self.db = connect(db_conn)
        self.db.autocommit = True
        self.topic_name = topic_name
        self.consumer.subscribe([self.topic_name])

    def consume_files(self):
        print("Consuming files")
        for message in self.consumer:
            print(f"Consuming message {message}")
            file_id = message.key.decode()
            cursor = self.db.cursor()
            cursor.execute(
                "select * from file_processing_queue where id = %s FOR UPDATE",
                (file_id,),
            )

            file_tuple = cursor.fetchone()

            print(f"Consuming file {file_tuple}")

            if not file_tuple:
                continue

            payload = FileMessage(**json.loads(message.value.decode()))

            try:
                content = self.process_file(payload.url)
            except Exception as e:
                status = "FAILED"
                reason = str(e)
                self.db.cursor().execute(
                    "update file_processing_queue set status = '%s', reason = '%s' where id = %s",
                    (
                        status,
                        reason,
                        file_id,
                    ),
                )
            else:
                status = "SUCCESS"
                reason = ""
                self.db.cursor().execute(
                    "update file_processing_queue set status = %s, content = %s where id = %s",
                    (status, json.dumps(content), file_id),
                )

            logging.info(f"Consumed file {file_id}")

    def process_file(self, url: str):
        resp = requests.get(url)
        return resp.json()


if __name__ == "__main__":
    consumer = Consumer(
        "test-topic",
        "localhost:9092",
        "postgres://postgres:postgres@127.0.0.1:5432/postgres",
    )

    consumer.consume_files()
