from flask import Flask, render_template, flash, url_for, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from forms import RegisterForm, TodoForm, LoginForm
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_login import (UserMixin, login_user, current_user,
                         LoginManager, login_required, current_user, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash
import os
from dotenv import load_dotenv
from sqldb import Todo, TodoUser, db

# TODO
# index.html: make db edit form as modal ✓
# index.html: change TODO table format ✓
# adopt flask-login ✓
# admin.html: admin page for admin authority only ✓
# db: one-to-many relationship set between TodoUser and Todo db ✓
# minor bug fix after testing ✓
# index.html: pagination for todos
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['CKEDITOR_PKG_TYPE'] = 'full-all'  # choose CKEditor form type
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

Bootstrap(app)
ckeditor = CKEditor(app)


def db_init():
    with app.app_context():
        db.create_all()


# db_init()


def db_delete(db_name):
    with app.app_context():
        db.session.query(db_name).delete()
        db.session.commit()


# db_delete(TodoUser)
@app.route('/', methods=['POST', 'GET'])
@login_required
def home():
    form = TodoForm()
    todo_db = current_user.todos.order_by(Todo.date, Todo.time).all()
    todo_cols = [col.name for col in Todo.__table__.columns]

    if request.method == 'GET':
        action = request.args.get('action')
        print(f"action: {action}")
        todo_id = request.args.get('todo_id')
        print(f"todo_id: {todo_id}")
        todo = Todo.query.filter_by(id=todo_id).first()
        if action == 'delete':
            db.session.delete(todo)
            db.session.commit()
            return redirect(url_for('home'))
        elif action == 'done':
            todo.done = not todo.done
            db.session.commit()

    return render_template('index.html',
                           form=form,
                           todo_db=todo_db,
                           todo_cols=todo_cols)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = TodoUser.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email Already Exists')
        elif form.password.data != form.password_2.data:
            flash('Password Unmatch Check Again Please')
        else:
            try:
                hashed_password = generate_password_hash(form.password.data)
                is_admin = form.email.data == 'admin@gmail.com' and form.username.data == 'admin'
                new_user = TodoUser(username=form.username.data,
                                    email=form.email.data,
                                    password=hashed_password,
                                    is_admin=is_admin)
                db.session.add(new_user)
                db.session.commit()
                flash('Sign Up Successful, Please Sign In to Access Site', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                flash(f"An Error Occured During Sign Up: {e}")
    return render_template('register.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('logging in...')
        print(f"username: {form.username.data}")
        user = TodoUser.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Login Unsuccessful", 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@login_manager.user_loader
def load_user(user_id):
    return TodoUser.query.get(user_id)


@app.route('/add_todo', methods=["POST", 'GET'])
@login_required
def add_todo():
    form = TodoForm()
    if form.validate_on_submit() and request.method == 'POST':
        # add to Todo_ db
        new_todo = Todo(
            task=form.task.data,
            description=form.description.data,
            importance=form.importance.data,
            date=form.date.data,
            time=form.time.data,
            done=form.done.data,
            user_id=current_user.id
        )
        db.session.add(new_todo)
        db.session.commit()
        print(f"added to db {form.task.data}")
        return redirect(url_for('home'))
    return render_template('index.html',
                           form=form)


@app.route('/admin', methods=['POST', 'GET'])
@login_required
def admin():
    # Check if the current user is an admin
    if not current_user.is_admin:
        flash('Access denied: You must be an admin to access this page.', 'danger')
        return redirect(url_for('home'))
    user_db = TodoUser.query.all()
    user_cols = [col.name for col in TodoUser.__table__.columns]
    todo_db = Todo.query.order_by(Todo.id).all()
    todo_cols = [col.name for col in Todo.__table__.columns]

    return render_template('admin.html',
                           user_db=user_db,
                           user_cols=user_cols,
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
