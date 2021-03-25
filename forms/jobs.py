from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class JobsForm(FlaskForm):
    job = StringField("Название работы", validators=[DataRequired()])
    team_leader = IntegerField("id тимлидера", validators=[DataRequired()])
    work_size = IntegerField("Продолжительность", validators=[DataRequired()])
    list_collaborators = StringField("Список id участников", validators=[DataRequired()])
    is_finished = BooleanField("Завершена")
    category = IntegerField("id уровня опасности", validators=[DataRequired()])
    submit = SubmitField('Добавить')
