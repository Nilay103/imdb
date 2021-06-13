from flask import Flask
from flask_restful import Api

from constants import MONGODB_URL, SECRET_KEY
from database import initialize_db
from registration import registration_bp
from routers import initialize_routes

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["MONGO_URI"] = MONGODB_URL
api = Api(app)
initialize_db(app)
initialize_routes(api)
app.register_blueprint(registration_bp)

if __name__ == "__main__":
    app.run()
