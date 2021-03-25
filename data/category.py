import sqlalchemy
from .db_session import SqlAlchemyBase


class HazardCategory(SqlAlchemyBase):
	__tablename__ = 'hazard_category'
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
	hazard_description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
	association_table = sqlalchemy.Table(
		"jobs_to_hazard_category",
		SqlAlchemyBase.metadata,
		sqlalchemy.Column("jobs", sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id")),
		sqlalchemy.Column("category", sqlalchemy.Integer, sqlalchemy.ForeignKey("hazard_category.id")))
