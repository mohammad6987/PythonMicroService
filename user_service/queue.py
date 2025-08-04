from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v , default=str).encode('utf-8')
)

def publish_user_created(user):
    producer.send('user-created', user)


def publish_
