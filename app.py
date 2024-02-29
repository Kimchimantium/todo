from flask import Flask, render_template, url_for, request, jsonify, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import SelectField, SubmitField, StringField, SearchField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor


#TODO
# initial setting ✓


app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf1319'
app.config['CKEDITOR_PKG_TYPE'] = 'full-all' # choose CKEditor form type
ckeditor = CKEditor(app)


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
