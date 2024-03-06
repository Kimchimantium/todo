from flask import Flask, render_template, flash, url_for, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, TimeField, DateField, SearchField, BooleanField, \
    IntegerField, EmailField, RadioField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import json
from datetime import date, datetime, time
from sqldb import Todo, db

# TODO
# change sql URL to portfolio integrated postgresql (render.com external db)✓
# db-browser.html: make sqldb browser ✓
# index.html: make importance show with the task ✓
# index.html: checkbox activate ✓
# index.html: clear form input after submit ✓
# index.html: timer anime to todo.time ✓
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'  # choose CKEditor form type
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

Bootstrap(app)
ckeditor = CKEditor(app)


def db_init():
    with app.app_context():
        db.create_all()


db_init()


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
                       validators=[DataRequired()],
                       render_kw={'placeholder': 'name of the TODO'}
                       )
    description = StringField(label='description',
                              render_kw={'style': 'width: 84%;',
                                         'placeholder': 'detail of the TODO'},
                              validators=[DataRequired()], )
    importance = RadioField(label='importance',
                            choices=[('1', '1 - Not Important'),
                                     ('2', '2'),
                                     ('3', '3 - Neutral'),
                                     ('4', '4'),
                                     ('5', '5 - Very Important')],
                            validators=[DataRequired()],
                            render_kw={'placeholder': 'detail of the TODO 1-5'}
                            )
    date = DateField(label='date',
                     validators=[DataRequired()],
                     render_kw={'placeholder': 'detail of the task'}
                     )
    time = TimeField(label='time',
                     validators=[DataRequired()])
    done = BooleanField(label='complete')
    submit = SubmitField()


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
        # add to Todo_ db
        new_todo = Todo(
            task=form.task.data,
            description=form.description.data,
            importance=form.importance.data,
            date=form.date.data,
            time=form.time.data,
            done=form.done.data
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')

    todo_db = Todo.query.order_by(Todo.date).all()
    todo_cols = [col.name for col in Todo.__table__.columns]

    # delete todo
    if request.method == 'GET':
        if request.args.get('action') == 'delete':
            to_delete = request.args.get('todo_id')
            print(to_delete)
            to_delete_db = Todo.query.get(to_delete)
            db.session.delete(to_delete_db)
            db.session.commit()
            return redirect('/')
    #  switch todo.done
        elif request.args.get('action') == 'done':
            to_done = request.args.get('todo_id')
            print(to_done)
            to_done_db = Todo.query.get(to_done)
            to_done_db.done = 1 if to_done_db.done == 0 else 0
            print(to_done_db.done)
            db.session.commit()
            return redirect('/')
    return render_template('index.html',
                           form=form,
                           todo_db=todo_db,
                           todo_cols=todo_cols)


@app.route('/add_todo')
def add_todo():
    return render_template('index.html')


@app.route('/db-browser', methods=['POST', 'GET'])
def db_browser():
    todo_db = Todo.query.order_by(Todo.id).all()
    todo_cols = [col.name for col in Todo.__table__.columns]

    return render_template('db-browser.html',
                           todo_db=todo_db,
                           todo_cols=todo_cols,
                           )


@app.route('/db-browser/delete/<int:todo_id>', methods=['POST', 'GET'])
def delete_todo(todo_id):
    if request.method == 'POST':
        delete_row = Todo.query.get(todo_id)
        db.session.delete(delete_row)
        db.session.commit()
        return redirect(url_for('db_browser'))

if __name__ == '__main__':
    app.run(debug=True, port=8086)
