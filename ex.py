import datetime
from flask import Flask, render_template, request
from data import db_session
from data.users import User

from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data.jobs import Jobs
from data.department import Department
from forms.departments import DepartmentsForm
from forms.user import LoginForm, RegisterForm
from forms.jobs import JobsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
	form = JobsForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		jobs = Jobs()
		jobs.job = form.job.data
		jobs.team_leader = form.team_leader.data
		jobs.work_size = form.work_size.data
		jobs.collaborators = form.list_collaborators.data
		jobs.is_finished = form.is_finished.data
		current_user.job.append(jobs)
		db_sess.merge(current_user)
		db_sess.commit()
		return redirect('/')
	return render_template('jobs.html', title='Добавление работы', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
	form = JobsForm()
	if request.method == "GET":
		db_sess = db_session.create_session()
		if current_user.id == 1:
			jobs = db_sess.query(Jobs).first()
		else:
			jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
		if jobs:
			form.job.data = jobs.job
			form.team_leader.data = jobs.team_leader
			form.work_size.data = jobs.work_size
			form.list_collaborators.data = jobs.collaborators
			form.is_finished.data = jobs.is_finished
		else:
			abort(404)
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		if current_user.id == 1:
			jobs = db_sess.query(Jobs).first()
		else:
			jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
		if jobs:
			jobs.job = form.job.data
			jobs.team_leader = form.team_leader.data
			jobs.work_size = form.work_size.data
			jobs.collaborators = form.list_collaborators.data
			jobs.is_finished = form.is_finished.data
			db_sess.commit()
			return redirect('/')
		else:
			abort(404)
	return render_template('jobs.html', title='Редактирование работы', form=form)


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
	db_sess = db_session.create_session()
	if current_user.id == 1:
		jobs = db_sess.query(Jobs).first()
	else:
		jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
	if jobs:
		db_sess.delete(jobs)
		db_sess.commit()
	else:
		abort(404)
	return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		if form.password.data != form.password_again.data:
			return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")
		db_sess = db_session.create_session()
		if db_sess.query(User).filter(User.email == form.email.data).first():
			return render_template('register.html', title='Регистрация', form=form, message="Такой пользователь уже есть")
		user = User(
			name=form.name.data,
			surname=form.surname.data,
			email=form.email.data,
			hashed_password=form.password_again.data,
			age=form.age.data,
			position=form.position.data,
			speciality=form.speciality.data,
			address=form.address.data,
			modified_date=datetime.datetime.now()
		)
		user.set_password(form.password.data)
		db_sess.add(user)
		db_sess.commit()
		return redirect('/login')
	return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
	db_sess = db_session.create_session()
	return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		user = db_sess.query(User).filter(User.email == form.email.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember_me.data)
			return redirect("/")
		return render_template('login.html', message="Неправильный логин или пароль", form=form)
	return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect("/")


@app.route("/")
def index():
	db_session.global_init("db/mars_explorer.db")
	db_sess = db_session.create_session()
	departments_ = db_sess.query(Department)
	return render_template("index_d.html", departments=departments_, current_user=current_user)


# DEPARTMENTS


@app.route("/departments", methods=['GET', 'POST'])
@login_required
def add_departments():
	form = DepartmentsForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		departments = Department()
		departments.title = form.title.data
		departments.chief = form.chief.data
		departments.email = form.email.data
		departments.members = form.members.data
		current_user.department.append(departments)
		db_sess.merge(current_user)
		db_sess.commit()
		return redirect('/')
	return render_template("departments.html", title="Adding Department", form=form)


if __name__ == '__main__':
	app.run(port=8080, host="127.0.0.1")
