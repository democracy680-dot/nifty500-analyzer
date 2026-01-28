# 📊 NIFTY 500 Professional Market Analyzer

A comprehensive, interactive dashboard for analyzing NSE NIFTY 500 stocks with advanced analytics, beautiful visualizations, and actionable trading signals.

![Dashboard Preview](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly)

## 🚀 Features

### Core Analytics
- **Real-time Market Overview**: Instant view of advancers, decliners, and market breadth
- **Multi-timeframe Momentum Analysis**: 30-day, 90-day, and 365-day performance tracking
- **Volume Profile Analytics**: Identify unusual volume spikes and liquidity patterns
- **Behavior Pattern Recognition**: Automatic classification of stock movements
- **Trading Signal Generation**: AI-driven buy/sell signals based on multiple factors

### Interactive Visualizations
- 📈 **Price Change Distribution**: Histogram showing market-wide returns
- 🥧 **Market Breadth Pie Chart**: Visual representation of market sentiment
- 📊 **Top Gainers/Losers**: Horizontal bar charts with color gradients
- 🔥 **Volume Spike Leaders**: Identify stocks with abnormal trading activity
- 🎯 **Scatter Plots**: Volume vs Price change correlation analysis
- 🌡️ **Momentum Heatmaps**: Multi-timeframe performance comparison
- 📉 **Volatility Box Plots**: Distribution analysis by behavior pattern
- 🎭 **Behavior Breakdown**: Stock count by trading pattern

### Advanced Features
- **Smart Filtering**: Filter by behavior, signals, price change, and volume
- **Customizable Thresholds**: Adjust sensitivity via sidebar controls
- **Export Functionality**: Download filtered results as CSV
- **Professional Styling**: Custom CSS for a polished, modern interface
- **Responsive Design**: Works seamlessly on desktop and tablets
- **Real-time Updates**: Instant recalculation as filters change

### Trading Signal Categories
- 🟢 **Buy Signals**: Stocks with positive momentum and volume confirmation
- 🔴 **Sell Signals**: Stocks showing weakness with volume
- ⭐ **High Conviction**: Strong moves with exceptional volume and momentum

### Behavior Classifications
- 🚀 **Breakout**: Strong upward move with high volume (>2% gain, 70%+ near high)
- 📈 **Strong Trend**: Significant price increase with volume confirmation
- 🟢 **Mild Up**: Gentle upward movement with low volatility
- ➖ **Normal**: Stable, no significant movement
- ⚠️ **Distribution**: Price drop with high volume (potential reversal)
- 📉 **Exhaustion**: Declining with low momentum
- 🔴 **Breakdown**: Sharp decline with high volume

## 📋 Requirements

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
```

## 🔧 Installation

1. **Clone or download the analyzer**:
```bash
# Create a new directory
mkdir nifty500-analyzer
cd nifty500-analyzer

# Save the Python file
# Copy nifty500_professional_analyzer.py to this directory
```

2. **Install required packages**:
```bash
pip install streamlit pandas numpy plotly
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Running the Dashboard

1. **Launch the application**:
```bash
streamlit run nifty500_professional_analyzer.py
```

2. **Access the dashboard**:
   - The app will automatically open in your default browser
   - Default URL: `http://localhost:8501`

### Using the Dashboard

1. **Upload Data**:
   - Download the NIFTY 500 daily report CSV from NSE
   - Click "Browse files" in the sidebar
   - Select your CSV file

2. **Configure Settings** (Sidebar):
   - **Min Price Change**: Set minimum price movement threshold
   - **Volume Spike Multiplier**: Adjust volume sensitivity (default: 2x median)
   - **Show Advanced Analytics**: Toggle additional analysis sections

3. **Explore Sections**:
   - **Market Overview**: High-level metrics and sentiment
   - **Price Distribution**: Understand market-wide movement patterns
   - **Top Performers**: Identify winners and losers
   - **Volume Analysis**: Spot unusual trading activity
   - **Momentum Heatmap**: Compare multi-timeframe performance
   - **Trading Signals**: Review actionable opportunities
   - **Complete Data Table**: Filter and export detailed data

4. **Filter & Export**:
   - Use behavior and signal filters in the data table
   - Sort by any metric
   - Download filtered results as CSV

## 📊 Data Format

The analyzer expects NIFTY 500 CSV files from NSE with these columns:

### Required Columns:
- `SYMBOL` - Stock ticker symbol
- `OPEN` - Opening price
- `HIGH` - Day's high price
- `LOW` - Day's low price
- `PREV CLOSE` - Previous close price
- `LTP` or `INDICATIVE CLOSE` - Latest trading price

### Optional Columns (for enhanced analysis):
- `VOLUME (SHARES)` - Trading volume
- `VALUE (Rs. IN LAKHS)` - Trading value
- `30 D % CHNG` - 30-day price change
- `90 D % CHNG` - 90-day price change
- `365 D % CHNG` - 365-day price change

## 🎨 Customization

### Color Scheme
The dashboard uses a professional color palette:
- **Green tones** (#28a745, #20c997, #5cb85c) - Positive movements
- **Red tones** (#dc3545, #fd7e14) - Negative movements
- **Blue tones** (#3498db, #1f77b4) - Neutral/informational
- **Yellow/Orange** (#ffc107, #fd7e14) - Warnings/caution

### Modifying Thresholds

Edit these values in the code to adjust sensitivity:

```python
# Behavior classification thresholds
(df["PRICE_CHANGE_%"] > 2)  # Breakout threshold
(df["VOLUME_SPIKE"])         # Volume spike (adjustable in sidebar)
(df["HIGH_PROXIMITY_%"] > 70) # Near high threshold

# Signal generation
(df["MOMENTUM_SCORE"] > 0)   # Positive momentum threshold
```

## 📈 Calculated Metrics

### Price Metrics
- **Price Change %**: `((Close - Prev Close) / Prev Close) × 100`
- **Intraday Range %**: `((High - Low) / Prev Close) × 100`
- **Gap %**: `((Open - Prev Close) / Prev Close) × 100`
- **High Proximity %**: `((Close - Low) / (High - Low)) × 100`

### Volume Metrics
- **Volume Ratio**: `Current Volume / Median Volume`
- **Volume Spike**: Boolean flag when Volume > Multiplier × Median

### Composite Scores
- **Momentum Score**: Weighted average of 30D (50%), 90D (30%), 365D (20%) changes
- **Volatility Score**: `Intraday Range % × Volume Ratio`

## 🔍 Interpretation Guide

### Market Sentiment
- **Bullish** (>20%): Strong positive breadth, majority advancing
- **Mildly Bullish** (0-20%): More advancers than decliners
- **Mildly Bearish** (-20-0%): More decliners than advancers
- **Bearish** (<-20%): Strong negative breadth, majority declining

### Trading Signals
- **Buy Signal**: Price > 1%, Volume spike, Positive momentum
- **Sell Signal**: Price < -1%, Volume spike, Negative momentum
- **High Conviction**: |Price| > 2%, Volume spike, |Momentum| > 3

### Volume Analysis
- **1-2x**: Normal volume
- **2-3x**: Increased interest
- **3-5x**: High interest (monitor closely)
- **>5x**: Exceptional activity (news/event driven)

## ⚠️ Important Notes

### Disclaimers
- **Not Financial Advice**: This tool is for informational and educational purposes only
- **No Guarantees**: Past performance does not indicate future results
- **Do Your Research**: Always conduct thorough analysis before trading
- **Risk Management**: Use proper position sizing and stop losses

### Best Practices
1. **Use Multiple Timeframes**: Don't rely on single-day data
2. **Confirm Volume**: High volume confirms price moves
3. **Check Momentum**: Align with longer-term trends
4. **Consider Market Context**: Individual stock moves vs overall market
5. **Set Alerts**: Monitor high conviction opportunities
6. **Regular Updates**: Analyze daily for best results

## 🐛 Troubleshooting

### Common Issues

**Problem**: "Required columns not found"
- **Solution**: Ensure CSV is from NSE and contains required columns
- Check for extra spaces or special characters in headers

**Problem**: Charts not displaying
- **Solution**: Update Plotly: `pip install --upgrade plotly`
- Clear browser cache and reload

**Problem**: Slow performance with large files
- **Solution**: Filter data before upload or use more recent Python/Pandas versions
- Disable "Show Advanced Analytics" in sidebar

**Problem**: Export not working
- **Solution**: Ensure you have write permissions in the directory
- Try a different browser

## 🔄 Updates & Roadmap

### Current Version: 2.0

### Planned Features
- [ ] Real-time data integration via NSE API
- [ ] Historical data analysis and backtesting
- [ ] Custom alert system with notifications
- [ ] Sector-wise performance breakdown
- [ ] Technical indicator integration (RSI, MACD, etc.)
- [ ] Portfolio tracking and analysis
- [ ] Comparison with index performance
- [ ] Machine learning price prediction

## 🤝 Contributing

Suggestions and improvements are welcome! Some areas for contribution:
- Additional technical indicators
- More sophisticated pattern recognition
- Performance optimizations
- UI/UX improvements
- Documentation enhancements

## 📄 License

This tool is provided as-is for educational purposes. Feel free to modify and adapt to your needs.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the data format requirements
3. Ensure all dependencies are installed correctly

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Pandas](https://pandas.pydata.org/) - Data manipulation
- [NumPy](https://numpy.org/) - Numerical computing

---

**Happy Analyzing! 📊📈**

*Remember: The best analysis combines quantitative metrics with qualitative judgment. Use this tool as one part of your research process.*
