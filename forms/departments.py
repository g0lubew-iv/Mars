from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class DepartmentsForm(FlaskForm):
    title = StringField("Title of Department", validators=[DataRequired()])
    chief = IntegerField("Chief's id", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    members = StringField("Members", validators=[DataRequired()])
    submit = SubmitField("Add")
