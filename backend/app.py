from flask import Flask
from flask_cors import CORS
from routes import blueprints

app = Flask(__name__)
CORS(app)

for bp in blueprints:
    app.register_blueprint(bp)

@app.route("/ping")
def ping():
    return "pong"

@app.route("/")
def home():
    return "Ola mundo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
