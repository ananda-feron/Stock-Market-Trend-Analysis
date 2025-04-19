import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# === S&P 500 Analysis ===
ticker = '^GSPC'
data = yf.download(ticker, start='2020-01-01', end='2024-12-31', group_by='ticker')

# Flatten column headers if MultiIndex
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(1)

print("S&P 500 Data Preview:")
print(data.head())

# Calculate moving averages and volatility
data['20_MA'] = data['Close'].rolling(window=20).mean()
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['Volatility'] = data['Close'].rolling(window=20).std()

# Stock trend visualization
plt.figure(figsize=(14, 6))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['20_MA'], label='20-Day MA')
plt.plot(data['50_MA'], label='50-Day MA')
plt.title('S&P 500 Price and Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

# Export to Excel
data.to_excel('SP500_Stock_Analysis.xlsx', engine='openpyxl')


# === Comparison of Major Stock Indices ===
tickers = ['^GSPC', '^IXIC', 'ISF.L']
combined_data = {}

for t in tickers:
    print(f"\nDownloading data for {t}...")
    df = yf.download(t, start='2020-01-01', end='2024-12-31', group_by='ticker')

    # Flatten columns if necessary
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(1)

    # Ensure 'Close' column exists and is a valid Series
    if not df.empty and 'Close' in df.columns and isinstance(df['Close'], pd.Series):
        combined_data[t] = df['Close']
        print(f"✅ Successfully added: {t}")
    else:
        print(f"❌ Invalid or incomplete data for {t}")

# Show which indices were successfully added
print("\nCombined keys:", list(combined_data.keys()))

# Plot comparison chart
if combined_data:
    combined_df = pd.DataFrame(combined_data)

    # Normalize all trends to start at 100 for easier comparison
    normalized_df = combined_df / combined_df.iloc[0] * 100

    normalized_df.plot(figsize=(14, 6), title="Normalized Index Comparison (Base = 100)")
    plt.xlabel('Date')
    plt.ylabel('Normalized Value')
    plt.grid(True)
    plt.show()
else:
    print("⚠️ No valid stock data available to plot.")
