from flask import Flask
from config import Config
from models import db, bcrypt
from routes.users import users
from routes.customer import customer
from routes.admin import admin
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(users)
app.register_blueprint(customer)
app.register_blueprint(admin)

# Configure CORS    
CORS(app, origins='http://localhost:3000', supports_credentials=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
