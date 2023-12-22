class Strategy4Links(object):
    datetime: str
    year: int
    month: int
    day: int
    time: str
    pair: str
    position: str
    four_hr_chart: str
    strategy: str
    one_day_chart: str
    one_week_chart: str
    one_month_chart: str
    profit_r: float
    comments: str

    def __init__(self,
                 datetime: str,
                 year: int,
                 month: int,
                 day: int,
                 time: str,
                 pair: str,
                 position: str,
                 four_hr_chart: str,
                 strategy: str,
                 one_day_chart: str,
                 one_week_chart: str,
                 one_month_chart: str,
                 profit_r: float,
                 comments: str) -> None:
        self.datetime = datetime
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.pair = pair
        self.position = position
        self.four_hr_chart = four_hr_chart
        self.strategy = strategy
        self.one_day_chart = one_day_chart
        self.one_week_chart = one_week_chart
        self.one_month_chart = one_month_chart
        self.profit_r = profit_r
        self.comments = comments
