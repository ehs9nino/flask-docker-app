from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Docker!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080 if PORT is not set
    app.run(host="0.0.0.0", port=port)
