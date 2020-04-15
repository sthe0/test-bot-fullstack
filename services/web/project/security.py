# -*- coding: utf-8 -*-
from flask_security import (
    Security,
    SQLAlchemySessionUserDatastore,
    login_required
)
from project.common import app, db
from project.models import User, Role


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)
