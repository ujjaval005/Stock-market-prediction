import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

# User input for stock symbol and date range
company = input("Enter stock symbol (e.g., AAPL, TSLA, RELIANCE.NS): ").strip().upper()
start_date = input("Enter start date (YYYY-MM-DD): ").strip()
end_date = input("Enter end date (YYYY-MM-DD): ").strip()

# Download stock data
stock = yf.download(company, start=start_date, end=end_date)
if stock.empty:
    print("⚠️ Error: No data found. Check the stock symbol and date range.")
    exit()

# Data Cleaning
stock.dropna(inplace=True)

# Train ARIMA Model
stock['Returns'] = stock['Close'].pct_change()
stock.dropna(inplace=True)

# Define ARIMA model parameters (p, d, q)
p, d, q = 5, 1, 0  # You can tune these parameters
model = ARIMA(stock['Close'], order=(p, d, q))
model_fit = model.fit()

# Predict the next 30 days
forecast_steps = 30  # Number of days to predict
forecast = model_fit.forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=stock.index[-1], periods=forecast_steps + 1, freq='B')[1:]

# Convert forecast to DataFrame
forecast_df = pd.DataFrame({'Date': forecast_index, 'Predicted_Close': forecast.values})
forecast_df.set_index('Date', inplace=True)

# Save results
csv_filename = f"{company}_ARIMA_forecast.csv"
forecast_df.to_csv(csv_filename)
print(f"✅ Forecast data saved to {csv_filename}")

# Plot actual vs predicted prices
plt.figure(figsize=(12, 6))
plt.plot(stock['Close'], label='Actual Close Price', color='blue')
plt.plot(forecast_df, label='ARIMA Forecast', linestyle='dashed', color='red')
plt.title(f"{company} - ARIMA Forecast for Next {forecast_steps} Days")
plt.legend()
plt.show()
