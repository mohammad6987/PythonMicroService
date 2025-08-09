from kafka import KafkaProducer,KafkaConsumer
import json



def init_queue() :
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v , default=str).encode('utf-8')
    )
    return producer




def init_consumer():
    """Start Kafka consumer for reading messages."""
    consumer = KafkaConsumer(
        'orders',
        bootstrap_servers='localhost:9092',
        value_deserializer=safe_deserializer,
        group_id='user-service-group',
        auto_offset_reset='earliest'
    )
    return consumer


def safe_deserializer(v):
    if not v:
        return None  # skip empty messages
    try:
        return json.loads(v.decode('utf-8'))
    except json.JSONDecodeError:
        print("Received invalid JSON:", v)
        return None
