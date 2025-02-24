import json
from datetime import datetime

from aiokafka import AIOKafkaProducer

from MockStreamData.operator.base_operator import BaseOperator


class KafkaOperator(BaseOperator):
    def __init__(self, topic, kafka_server="localhost:9092"):
        self.topic = topic
        self.kafka_server = kafka_server
        self.producer = None

    async def start(self):
        """Initialize the asynchronous Kafka producer."""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.kafka_server,
            value_serializer=lambda v: json.dumps(v, default=lambda o: o.isoformat() if isinstance(o, datetime) else o).encode('utf-8')
        )
        await self.producer.start()
        print("KafkaOperator started.")

    async def send(self, data):
        """Send data to Kafka using send_and_wait."""
        print(data)
        await self.producer.send_and_wait(self.topic, data)
        print(f"Sent to Kafka on topic '{self.topic}': {data}")

    async def stop(self):
        """Close the Kafka producer."""
        if self.producer:
            await self.producer.stop()
            print("KafkaOperator stopped.")