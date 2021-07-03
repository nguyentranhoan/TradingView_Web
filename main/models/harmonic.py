from typing import List

from main.db import db
from sqlalchemy import func, distinct


class HarmonicModel(db.Model):
    __tablename__ = 'harmonic'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    pair = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    one_hr_chart = db.Column(db.String(255), nullable=False)
    one_day_chart = db.Column(db.String(255), nullable=False)
    profit_r = db.Column(db.Float(precision=2), nullable=False)
    comments = db.Column(db.String(255))

    @classmethod
    def find_by_id(cls, _id) -> "HarmonicModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_distinct_years(cls) -> List:
        """Model.query is a shortcut to db.session.query(Model),
        it's not callable. If you're not querying a model,
        continue to use db.session.query(...)
        as you would with regular SQLAlchemy."""
        return db.session.query(func.distinct(cls.year)).group_by(cls.year).order_by(cls.year.asc()).all()

    @classmethod
    def get_distinct_months_by_year(cls, year: int) -> List:
        return db.session.query(func.distinct(cls.month)).filter_by(year=year).group_by(cls.month).order_by(cls.month.asc()).all()

    @classmethod
    def get_distinct_pairs_by_year(cls, year: int) -> List:
        return db.session.query(func.distinct(cls.pair)).filter_by(year=year).group_by(cls.pair).order_by(cls.pair.asc()).all()

    @classmethod
    def get_distinct_days_by_month(cls, year: int, month: int) -> List:
        return db.session.query(func.distinct(cls.day)).filter_by(year=year, month=month).group_by(cls.day).order_by(
            cls.day.asc()).all()

    @classmethod
    def get_distinct_months_by_pair(cls, year: int, pair: str) -> List:
        return db.session.query(func.distinct(cls.month)).filter_by(year=year, pair=pair).group_by(cls.month).order_by(
            cls.month.asc()).all()

    @classmethod
    def get_daily_transaction(cls, year: int, month: int, day: int) -> List:
        return cls.query.filter_by(year=year, month=month, day=day).order_by(cls.time.asc()).all()

    @classmethod
    def get_transaction_by_pair(cls, year: int, month: int, pair: str) -> List:
        return cls.query.filter_by(year=year, month=month, pair=pair).order_by(cls.time.asc()).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # end of file
