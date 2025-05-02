from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import random

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ["endpoint"])

# Simulated DB (in-memory)
products = [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]

@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    start = time.time()
    time.sleep(random.uniform(0.1, 0.3))  # Simulate latency
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    return "Welcome to the DevOps Demo App!"

@app.route("/products", methods=["GET", "POST"])
def manage_products():
    REQUEST_COUNT.labels(method=request.method, endpoint="/products").inc()
    start = time.time()

    if request.method == "POST":
        new_product = request.json
        new_product["id"] = len(products) + 1
        products.append(new_product)
        result = jsonify(new_product), 201
    else:
        result = jsonify(products)

    REQUEST_LATENCY.labels(endpoint="/products").observe(time.time() - start)
    return result

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

