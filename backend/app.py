from flask import Flask
from config import Config
from routes.users import users
from routes.app import app as route_app
from routes.admin import Pi5neer
from routes.security_policy import security_policy_
from flask_cors import CORS
from models import db, bcrypt
from models import *  
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import datetime,timedelta
# Import and register models
from models.admin import Admin
from models.user import User
from models.domain import Domain
from models.user_application import UserApplication
from models.security_policy import SecurityPolicy
from models.sp_url import SpUrl
from models.sp_ip import SpIp
from decouple import config as config_
from flask_mail import Mail # forgot pw 관련

app = Flask(__name__)

#app.config['JWT_SECRET_KEY'] = config_['key']
app.config['JWT_SECRET_KEY'] = config_('key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # 30분으로 설정
jwt = JWTManager(app)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

mail=Mail(app) # forgot pw 관련

# Import and register routes
app.register_blueprint(users)
app.register_blueprint(route_app)
app.register_blueprint(Pi5neer)
app.register_blueprint(security_policy_)

# Configure CORS    
CORS(app, origins='http://127.0.0.1:3000', supports_credentials=True)

# Initialize Flask-Migrate
migrate = Migrate(app, db)


if __name__ == '__main__':
    # Remove the app.run() and replace it with the following block
    with app.app_context():
        db.create_all()
    app.run(debug=True)
