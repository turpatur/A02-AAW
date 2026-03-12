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

            channel.queue_declare(queue="archive_queue", durable=True)
            channel.queue_bind(exchange="post_events", queue="archive_queue")
            return channel, "archive_queue"
        except pika.exceptions.AMQPConnectionError:
            print("[ARCHIVE] RabbitMQ not ready, retrying in 3s...")
            time.sleep(3)

channel, queue_name = connect()

def callback(ch, method, properties, body):
    event = json.loads(body)
    with open("archive.txt", "a") as f:
        f.write(event["content"] + "\n")
    print("[ARCHIVE] Saved post")

channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True
)

print("Archive service waiting for events...")
channel.start_consuming()