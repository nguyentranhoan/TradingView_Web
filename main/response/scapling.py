
class Scapling(object):
    datetime: str
    year: int
    month: int
    day: int
    time: str
    pair: str
    position: str
    fifteen_min_chart: str
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
                 fifteen_min_chart: str,
                 profit_r: float,
                 comments: str) -> None:
        self.datetime = datetime
        self.year = year
        self.month = month
        self.day = day
        self.time = time
        self.pair = pair
        self.position = position
        self.fifteen_min_chart = fifteen_min_chart
        self.profit_r = profit_r
        self.comments = comments
