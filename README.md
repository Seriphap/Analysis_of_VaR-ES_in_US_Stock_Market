# 📈 Analysis of Value at Risk (VaR) and Expected Shortfall (ES) in the U.S. Stock Market

This project analyzes **Value at Risk (VaR)** and **Expected Shortfall (ES)** in the U.S. stock market using Python and provides an interactive Streamlit app for visualization and exploration.

# 🔗 Streamlit App
https://analysisofvar-esinusstockmarket-aguwj6dzqxusyjzkqroywv.streamlit.app/


## 🏷️ Topic

The primary goal of this repository is to analyze risk measures—specifically, Value at Risk (VaR) and Expected Shortfall (ES)—to assess the risk of loss on investments in the U.S. stock market. The analysis covers statistical techniques, risk modeling, and interactive visualizations.

---

## 🚀 Streamlit App

An interactive Streamlit app is included to:
- Visualize and compare VaR and ES across various U.S. stocks and time intervals
- Allow users to select different stocks, confidence levels, and time windows
- Display dynamic charts and tables
- Experiment with custom scenarios and parameters

To run the app locally:
```bash
pip install -r requirements.txt
streamlit run app.py
```
(Adjust the above command if your main app file uses a different name.)

---

## 📁 Project Structure

```
Analysis_of_VaR-ES_in_US_Stock_Market/
│
├── app.py                # Streamlit app entry point
├── data/                 # Raw and processed datasets
│   └── us_stocks.csv     # Example stock data file
├── data_loader.py        # Raw and processed datasets from API and upload from user
├── src/                  # Core analysis scripts and modules
│   ├── risk_metrics.py   # Functions to compute VaR and ES
│   └── plotter.py        # Stock chart and Histogram (Return VS (VaR/ES))
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```
_Note: Actual file names and structure may vary. Update as needed for your repo._

---

## 📊 Dataset

- **Source:** The dataset contains historical price data for major U.S. stocks (e.g., S&P 500 constituents).
- **Typical columns:** `Date`, `Open`, `High`, `Low`, `Close`, `Volume`, `Ticker`
- **Preprocessing:** Data is cleaned, missing values handled, and returns calculated as input for risk calculations.

---

## ✨ Features

- **VaR and ES Calculation:** Implements classical (historical, parametric) and advanced (Monte Carlo, EVT) methods for risk estimation.
- **Comparative Visualization:** Interactive plots to compare risk metrics across stocks, portfolios, and time frames.
- **Scenario Analysis:** Users can simulate shocks or adjust confidence intervals and immediately see results.
- **Modular Codebase:** Clear separation of data loading, cleaning, risk calculation, and visualization modules.
- **Easy Extensibility:** Add new stocks, import custom datasets, or extend with additional risk metrics.

---

## 📚 References

- [VaR and ES Concepts – Investopedia](https://www.investopedia.com/terms/v/valueatrisk.asp)
- [U.S. Stock Market Datasets – Alphavantage](https://www.alphavantage.co/documentation/)

---

## 💡 How to Contribute

1. Fork the repository
2. Create a new branch for your feature or fix
3. Submit a detailed pull request

---

For questions or feedback, please open an issue or contact [Seriphap](https://github.com/Seriphap).

```
**Note:**  
Some details (like actual file names and dataset specifics) may need to be updated based on your latest project files and data.
```
