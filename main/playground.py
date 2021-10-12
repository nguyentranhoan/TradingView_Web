import sqlite3
import pandas as pd

DATABASE_URL = "C:/Users/Nguye/Documents/GitHub/TradingView_Web/main/test.db" #'C:/Users/HP/Desktop/TradingView_Web/main/.data'

if __name__ == '__main__':
    conn = sqlite3.connect(DATABASE_URL)
    # save sqlite table in a DataFrame
    momentum = pd.read_sql('SELECT * from momentum', conn)
    # write DataFrame to CSV file
    momentum.to_csv('C:/Users/Nguye/Documents/GitHub/TradingView_Web/main/.data/momentum.csv', index=False)
    

    """
    REMEMBER TO ADJUST momentum.csv file FORMAT BEFORE MIGRATING TO NEW DATABASE.
    """