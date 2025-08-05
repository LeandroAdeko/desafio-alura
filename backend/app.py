from flask import Flask, request
from flask_cors import CORS
from routes import blueprints
from flask_jwt_extended import JWTManager
import os


app = Flask(__name__)

frontend_url = os.environ.get("FRONTEND_URL")
CORS(
    app,
    supports_credentials=True,
    origin=frontend_url,
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["Authorization"],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    resources={r"/*": {"origins": frontend_url}},
)
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
jwt = JWTManager(app)

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
