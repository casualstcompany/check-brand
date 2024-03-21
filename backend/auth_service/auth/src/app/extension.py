from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_security import Security
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()
db = SQLAlchemy()
ma = Marshmallow()
security = Security()
