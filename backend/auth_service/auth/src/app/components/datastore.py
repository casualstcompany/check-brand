from extension import db
from flask_security import SQLAlchemyUserDatastore
from models import Role, User


def get_datastore(db):
    return SQLAlchemyUserDatastore(db, User, Role)


datastore = get_datastore(db)
