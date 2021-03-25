import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Department(SqlAlchemyBase):
	def __repr__(self):
		return self.title

	__tablename__ = "departments"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	title = sqlalchemy.Column(sqlalchemy.String)
	chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
	email = sqlalchemy.Column(sqlalchemy.String)
	members = sqlalchemy.Column(sqlalchemy.String)

	user = orm.relation("User")
