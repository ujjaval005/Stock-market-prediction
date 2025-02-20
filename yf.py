import yfinance as yf
import pandas as pd



# User input for stock symbol, date range, and interval
company = input("Enter stock symbol (e.g., AAPL, TSLA): ")
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Download historical stock data with selected interval
stock = yf.download(company, start=start_date, end=end_date,)

# Data Cleaning
stock.drop_duplicates(inplace=True)  # Remove duplicate rows if any
stock.dropna(inplace=True)  # Remove rows with missing values

# Moving Averages Calculation
stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
stock["SMA_200"] = stock["Close"].rolling(window=200).mean()

# Handling NaN values after moving average calculation
stock.dropna(inplace=True)


#print(stock.tail(100))
stock.tail(100).to_csv("stock_data.csv", index=True)
print("Stock data saved to stock_data.csv")

