from flask import Flask, request, jsonify
from flask_cors import CORS
import pika, json
 
app = Flask(__name__)
CORS(app)
 
@app.route("/post", methods=["POST"])
def post():
    content = request.json["content"]
 
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq")
    )
    channel = connection.channel()
    channel.exchange_declare(exchange="post_events", exchange_type="fanout")
 
    event = {
        "event": "PostCreated",
        "content": content
    }
 
    channel.basic_publish(
        exchange="post_events",
        routing_key="",
        body=json.dumps(event)
    )
 
    connection.close()
    return {"status": "ok"}
 
app.run(host="0.0.0.0", port=5000)
 