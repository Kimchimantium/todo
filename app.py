from flask import Flask, render_template, flash, url_for, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import SelectField, SubmitField, StringField, TimeField, DateField, SearchField, BooleanField, \
    IntegerField, EmailField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import date, datetime, time

# TODO
# set render.com PostgreSQL URL as SQLAlchemy URI ✓
# make RegisterForm, TodoForm ✓
# make instance/todo_.json archive ✓
# migrate from todo_.json to SQLDB

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'  # choose CKEditor form type
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Bootstrap(app)
ckeditor = CKEditor(app)


class Kimchimantium(db.Model):
    __tablename__ = 'userInfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(40), unique=True)
    password_hash = db.Column(db.String(20), unique=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegisterForm(FlaskForm):
    username = StringField(label='Name',
                           validators=[DataRequired()])
    password = StringField(label='Password',
                           validators=[DataRequired()])
    password_2 = StringField(label='Password Check',
                             validators=[DataRequired()])
    email = EmailField(label='Email',
                       validators=[DataRequired()])
    submit = SubmitField()


class TodoForm(FlaskForm):
    task = StringField(label='task',
                       validators=[DataRequired()])
    description = StringField(label='description',
                              validators=[DataRequired()])
    importance = IntegerField(label='importance',
                              validators=[DataRequired()])
    date = DateField(label='date',
                     validators=[DataRequired()])
    time = TimeField(label='time',
                     validators=[DataRequired()])
    done = BooleanField(label='complete')
    submit = SubmitField()


def db_init():
    with app.app_context():
        db.create_all()


# db_init()

@app.route('/', methods=['POST', 'GET'])
def home():
    form = TodoForm()
    todo_list = []
    if form.validate_on_submit() and request.method == 'POST':
        todo_list.append(
            {
                'task': form.task.data,
                'description': form.description.data,
                'importance': form.importance.data,
                'date': form.date.data.isoformat(),
                'time': form.time.data.strftime('%H:%M'),
                'done': form.done.data, }
        )
        with open('instance/todo.json', 'w') as file:
            json.dump(todo_list, file, indent=4, ensure_ascii=False)


    return render_template('index.html', form=form)


@app.route('/add_todo')
def add_todo():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    sql_db = db.session.query(Kimchimantium).all()
    for user in sql_db:
        print(user.id, user.email, user.username, user.password_hash)

    if request.method == 'POST' and form.validate_on_submit():
        received_username = form.username.data
        received_password = form.password.data
        received_password_2 = form.password_2.data
        received_email = form.email.data

        # register conditions
        if Kimchimantium.query.filter_by(username=received_username).first():
            flash('username already in use', 'error')
        elif received_password != received_password_2:
            flash('check password', 'error')
        elif Kimchimantium.query.filter_by(email=received_email).first():
            flash('email already in use', 'error')
        else:
            new_email, new_username, new_password = received_email, received_username, received_password
            new_user = Kimchimantium(username=new_username, email=new_email)
            new_user.set_password(new_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registered Successfully!', 'Success')
    return render_template('register.html',
                           form=form)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
