import time
from collections import defaultdict 
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store request count and timestamps per IP
request_counters = defaultdict(lambda: {"count": 0, "timestamps": []})

# Configuration for rate limits
RATE_LIMIT = 7  # max requests
TIME_WINDOW = 60  # in seconds

def is_rate_limited(ip_address):
    data = request_counters[ip_address]
    current_time = time.time()
    # Remove timestamps outside the rate limiting window
    data["timestamps"] = [t for t in data["timestamps"] if t > current_time - TIME_WINDOW]
    # Check if current rate exceeds the limit
    if len(data["timestamps"]) >= RATE_LIMIT:
        return True
    else:
        data["timestamps"].append(current_time)
        return False

@app.route('/')
def index():
    return 'Hello, this is the server!'

@app.route("/query", methods=["POST"])
def handle_query():
    print("hello")
    ip_address = request.remote_addr
    print(f"Received request from IP: {ip_address}")
    if is_rate_limited(ip_address):
        print("Rate limit exceeded for this IP.")
        return jsonify({"error": "Rate limit exceeded"}), 429
    # Process the query
    query_data = request.json.get("query")
    print(f"Processing query: {query_data}")
    # A dummy response for illustration purposes
    response = {"response": f"Processed query: {query_data}"}
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
