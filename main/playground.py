from datetime import datetime
date_time_str = "08 Jun 22 22:45"
date_time = datetime.strptime(date_time_str, '%d %b %y %H:%M')
print(date_time)