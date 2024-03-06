from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200))
    description = db.Column(db.String(200))
    importance = db.Column(db.Integer)
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    done = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)