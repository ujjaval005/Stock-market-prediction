import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# User input for stock symbol and date range
company = input("Enter stock symbol (e.g., AAPL, TSLA, RELIANCE.NS): ").strip().upper()
start_date = input("Enter start date (YYYY-MM-DD): ").strip()
end_date = input("Enter end date (YYYY-MM-DD): ").strip()

# Download stock data
stock = yf.download(company, start=start_date, end=end_date)
if stock.empty:
    print("⚠️ Error: No data found. Check the stock symbol and date range.")
    exit()

# Download Market Index Data (NIFTY 50 and S&P 500)
nifty = yf.download("^NSEI", start=start_date, end=end_date)  # NIFTY 50
sp500 = yf.download("^GSPC", start=start_date, end=end_date)  # S&P 500

# Data Cleaning
stock.dropna(inplace=True)
nifty.dropna(inplace=True)
sp500.dropna(inplace=True)

# 🔹 Moving Averages (SMA & EMA)
stock["SMA_50"] = stock["Close"].rolling(window=50).mean()
stock["SMA_200"] = stock["Close"].rolling(window=200).mean()
stock["EMA_50"] = stock["Close"].ewm(span=50, adjust=False).mean()

# 🔹 Bollinger Bands
stock["SMA_20"] = stock["Close"].rolling(window=20).mean()
stock["STD_20"] = stock["Close"].rolling(window=20).std()
stock["Upper_Band"] = stock["SMA_20"] + (stock["STD_20"] * 2)
stock["Lower_Band"] = stock["SMA_20"] - (stock["STD_20"] * 2)

# 🔹 Correlation with Market Indexes
stock["Returns"] = stock["Close"].pct_change()
nifty["Returns"] = nifty["Close"].pct_change()
sp500["Returns"] = sp500["Close"].pct_change()

corr_nifty = stock["Returns"].corr(nifty["Returns"])
corr_sp500 = stock["Returns"].corr(sp500["Returns"])

# 📊 Save to CSV
csv_filename = f"{company}_analysis.csv"
stock.to_csv(csv_filename, index=True)
print(f"✅ Data saved to {csv_filename}")

# 📊 Save to Excel with Multiple Sheets
excel_filename = f"{company}_analysis.xlsx"
with pd.ExcelWriter(excel_filename, engine="xlsxwriter") as writer:
    stock.to_excel(writer, sheet_name="Stock Data")
    nifty.to_excel(writer, sheet_name="NIFTY 50 Data")
    sp500.to_excel(writer, sheet_name="S&P 500 Data")

    # Summary Sheet
    summary = pd.DataFrame({
        "Metric": ["Correlation with NIFTY 50", "Correlation with S&P 500"],
        "Value": [corr_nifty, corr_sp500]
    })
    summary.to_excel(writer, sheet_name="Market Correlation", index=False)

print(f"✅ Data also saved to {excel_filename}")

# 📊 Plot Moving Averages
plt.figure(figsize=(12, 6))
plt.plot(stock["Close"], label="Close Price", color="blue")
plt.plot(stock["SMA_50"], label="SMA 50", linestyle="dashed", color="green")
plt.plot(stock["SMA_200"], label="SMA 200", linestyle="dotted", color="red")
plt.plot(stock["EMA_50"], label="EMA 50", linestyle="dashdot", color="orange")
plt.title(f"{company} - Price Trends (SMA & EMA)")
plt.legend()
plt.show()

# 📊 Plot Bollinger Bands
plt.figure(figsize=(12, 6))
plt.plot(stock["Close"], label="Close Price", color="blue")
plt.plot(stock["SMA_20"], label="SMA 20", linestyle="dashed", color="black")
plt.fill_between(stock.index, stock["Upper_Band"], stock["Lower_Band"], color="gray", alpha=0.3)
plt.title(f"{company} - Bollinger Bands")
plt.legend()
plt.show()

# ✅ Print Correlation Results
print("\n📈 Market Correlation:")
print(f"Correlation with NIFTY 50: {corr_nifty:.2f}")
print(f"Correlation with S&P 500: {corr_sp500:.2f}")
