# app.py
from flask import Flask
from config import Config
from models import db
from routes.users import app as users  # Changed the import
from flask_cors import CORS
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.register_blueprint(users)  # Registering the blueprint

# Configure CORS
CORS(app, origins='http://localhost:3000', supports_credentials=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
