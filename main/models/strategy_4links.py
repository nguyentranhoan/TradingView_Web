from typing import List

from main.db import db

from sqlalchemy import func, distinct


class Strategy4LinksModel(db.Model):
    __tablename__ = 'strategy_4links'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    time = db.Column(db.String(50), nullable=False)
    pair = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    four_hr_chart = db.Column(db.String(255), nullable=False)
    strategy = db.Column(db.String(255), nullable=False)
    one_day_chart = db.Column(db.String(255), nullable=False)
    one_week_chart = db.Column(db.String(255), nullable=False)
    one_month_chart = db.Column(db.String(255), nullable=False)
    profit_r = db.Column(db.Float(precision=2))
    comments = db.Column(db.String(255))

    @classmethod
    def find_by_id(cls, _id, strategy) -> "Strategy4LinksModel":
        return cls.query.filter_by(id=_id, strategy=strategy).first()

    @classmethod
    def get_distinct_years(cls, strategy: str) -> List:
        """Model.query is a shortcut to db.session.query(Model),
        it's not callable. If you're not querying a model,
        continue to use db.session.query(...)
        as you would with regular SQLAlchemy."""
        return db.session.query(func.distinct(cls.year)).filter_by(strategy=strategy).group_by(cls.year).order_by(cls.year.asc()).all()

    @classmethod
    def get_distinct_months_by_year(cls, strategy: str, year: int) -> List:
        return db.session.query(func.distinct(cls.month)).filter_by(strategy=strategy, year=year).group_by(cls.month).order_by(cls.month.asc()).all()

    @classmethod
    def get_distinct_pairs_by_month(cls, strategy: str, year: int, month: int) -> List:
        return db.session.query(func.distinct(cls.pair)).filter_by(strategy=strategy, year=year, month=month).group_by(cls.pair).order_by(cls.pair.asc()).all()

    @classmethod
    def get_distinct_pairs_by_year(cls, strategy: str, year: int) -> List:
        return db.session.query(func.distinct(cls.pair)).filter_by(strategy=strategy, year=year).group_by(cls.pair).order_by(cls.pair.asc()).all()

    @classmethod
    def get_distinct_days_by_month(cls, strategy: str, year: int, month: int) -> List:
        return db.session.query(func.distinct(cls.day)).filter_by(strategy=strategy, year=year, month=month).group_by(cls.day).order_by(cls.day.asc()).all()

    @classmethod
    def get_distinct_months_by_pair(cls, strategy: str, year: int, pair: str) -> List:
        return db.session.query(func.distinct(cls.month)).filter_by(strategy=strategy, year=year, pair=pair).group_by(cls.month).order_by(cls.month.asc()).all()

    @classmethod
    def get_daily_transaction(cls, strategy: str, year: int, month: int, day: int) -> List:
        return cls.query.filter_by(strategy=strategy, year=year, month=month, day=day).order_by(cls.time.asc()).all()

    @classmethod
    def get_transaction_by_month(cls, strategy: str, year: int, month: int) -> List:
        return cls.query.filter_by(strategy=strategy, year=year, month=month).order_by(cls.time.asc()).all()

    @classmethod
    def get_transaction_by_pair(cls, strategy: str, year: int, month: int, pair: str) -> List:
        return cls.query.filter_by(strategy=strategy, year=year, month=month, pair=pair).order_by(cls.time.asc()).all()

    @classmethod
    def find_all(cls, strategy: str):
        return cls.query.filter_by(strategy=strategy).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # end of file
