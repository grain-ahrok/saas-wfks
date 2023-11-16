from flask import Flask
from config import Config
from routes.users import users
from routes.customer import customer
from routes.admin import Pi5neer
from flask_cors import CORS
from models import db, bcrypt
from models import *  
from flask_migrate import Migrate
from datetime import datetime
# Import and register models
from models.admin import Admin
from models.user import User
from models.domain import Domain
from models.user_application import UserApplication
from models.security_policy import SecurityPolicy
from models.sp_url import SpUrl
from models.sp_ip import SpIp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

# Import and register routes
app.register_blueprint(users)
app.register_blueprint(customer)
app.register_blueprint(Pi5neer)

# Configure CORS    
CORS(app, origins='http://127.0.0.1:3000', supports_credentials=True)

# Initialize Flask-Migrate
migrate = Migrate(app, db)


if __name__ == '__main__':
    # Remove the app.run() and replace it with the following block
    with app.app_context():
        db.create_all()
    app.run(debug=True)