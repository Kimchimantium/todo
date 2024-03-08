from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, PasswordField, StringField, TimeField, DateField, SearchField, \
    BooleanField, \
    IntegerField, EmailField, RadioField, HiddenField
from wtforms.validators import DataRequired, URL


class RegisterForm(FlaskForm):
    username = StringField(label='Name',
                           validators=[DataRequired()])
    password = PasswordField(label='Password',
                             validators=[DataRequired()])
    password_2 = PasswordField(label='Password Check',
                               validators=[DataRequired()])
    email = EmailField(label='Email',
                       validators=[DataRequired()])
    submit = SubmitField(render_kw={'style': "border: none; background-color: transparent; color: #fafafa;"})


class LoginForm(FlaskForm):
    username = StringField(label='Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(render_kw={'style': "border: none; background-color: transparent; color: #fafafa;"})

class TodoForm(FlaskForm):
    todo_id = HiddenField()
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
    submit = SubmitField(render_kw={'style': "border: none; background-color: transparent; color: #fafafa;"})
