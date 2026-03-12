import pika
import json
import time

def connect():
    while True:
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq")
            )
            channel = connection.channel()
            channel.exchange_declare(exchange="post_events", exchange_type="fanout")

            channel.queue_declare(queue="wordcount_queue", durable=True)
            channel.queue_bind(exchange="post_events", queue="wordcount_queue")
            return channel, "wordcount_queue"
        except pika.exceptions.AMQPConnectionError:
            print("[WORDCOUNT] RabbitMQ not ready, retrying in 3s...")
            time.sleep(3)

channel, queue_name = connect()

def callback(ch, method, properties, body):
    event = json.loads(body)
    content = event["content"]
    word_count = len(content.split())
    print("[WORDCOUNT] Words:", word_count)

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print("Word counter waiting for events...")
channel.start_consuming()