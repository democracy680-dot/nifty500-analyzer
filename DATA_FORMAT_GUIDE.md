# 📋 NIFTY 500 Data Format Guide

## Overview
This guide explains the expected CSV format for the NIFTY 500 Professional Analyzer.

## Where to Get Data
Download the daily NIFTY 500 report from the National Stock Exchange (NSE):
- **Website**: https://www.nseindia.com
- **Section**: Market Data → Reports → NIFTY 500
- **Format**: CSV file

## Expected Column Structure

### Required Columns (Must Have)

| Column Name | Description | Example |
|------------|-------------|---------|
| SYMBOL | Stock ticker symbol | RELIANCE, TCS, INFY |
| OPEN | Opening price for the day | 2,450.50 |
| HIGH | Highest price during the day | 2,485.75 |
| LOW | Lowest price during the day | 2,445.00 |
| PREV CLOSE | Previous day's closing price | 2,440.00 |
| LTP or INDICATIVE CLOSE | Latest traded price / Current close | 2,470.25 |

### Optional Columns (Recommended for Enhanced Analysis)

| Column Name | Description | Example |
|------------|-------------|---------|
| VOLUME (SHARES) | Number of shares traded | 15,234,567 |
| VALUE (Rs. IN LAKHS) | Total trading value in lakhs | 37,450.50 |
| 30 D % CHNG | 30-day percentage change | 5.67% |
| 90 D % CHNG | 90-day percentage change | 12.34% |
| 365 D % CHNG | 365-day percentage change | 45.67% |

## Sample CSV Structure

```csv
SYMBOL,OPEN,HIGH,LOW,PREV CLOSE,LTP,VOLUME (SHARES),VALUE (Rs. IN LAKHS),30 D % CHNG,90 D % CHNG,365 D % CHNG
RELIANCE,2450.50,2485.75,2445.00,2440.00,2470.25,15234567,37450.50,5.67,12.34,45.67
TCS,3250.00,3280.50,3245.00,3240.00,3265.75,8567234,27890.25,3.45,8.90,38.50
INFY,1550.75,1565.00,1548.50,1545.00,1560.25,12345678,19234.75,4.23,10.56,42.30
```

## Data Format Notes

### Number Formats
The analyzer handles various number formats:
- **With commas**: `2,450.50` ✓
- **Without commas**: `2450.50` ✓
- **With currency symbol**: `₹2,450.50` ✓
- **With percentage**: `5.67%` ✓

All of these will be automatically cleaned and converted to numeric values.

### Column Name Variations
The analyzer recognizes various column name formats:
- Case insensitive (OPEN, Open, open all work)
- Handles line breaks in headers
- Ignores parentheses and periods
- Strips extra whitespace

### Common Column Name Variations

**For CLOSE price**, the analyzer looks for:
- LTP
- INDICATIVE CLOSE
- CLOSE

**For VOLUME**, the analyzer looks for:
- VOLUME (SHARES)
- VOLUME  SHARES
- VOLUME

**For PREVIOUS CLOSE**, the analyzer looks for:
- PREV CLOSE
- PREVIOUS CLOSE

## Data Quality Checks

The analyzer performs automatic validation:

✅ **Checks for required columns**: Stops if essential columns are missing
✅ **Converts to numeric**: Automatically handles formatting
✅ **Removes invalid data**: Drops rows with critical missing values
✅ **Handles missing optional data**: Calculations adjust if optional columns are absent

## Preparing Your Data

### If Using Excel
1. Open the NSE CSV file in Excel
2. Verify column headers match expected names
3. Save as CSV (Comma delimited)
4. Upload to the analyzer

### If Using Google Sheets
1. Import the NSE CSV
2. Check headers
3. Download as CSV
4. Upload to the analyzer

### Manual Preparation
If your CSV has different column names:
1. Open in a text editor
2. Update the first row (headers) to match expected names
3. Save the file
4. Upload

## Example: Minimal Working CSV

This is the absolute minimum data needed:

```csv
SYMBOL,OPEN,HIGH,LOW,PREV CLOSE,LTP
RELIANCE,2450.50,2485.75,2445.00,2440.00,2470.25
TCS,3250.00,3280.50,3245.00,3240.00,3265.75
INFY,1550.75,1565.00,1548.50,1545.00,1560.25
```

This will work, but you'll miss out on:
- Volume analysis
- Multi-timeframe momentum
- Volume spike detection

## Example: Full-Featured CSV

For best results, include all columns:

```csv
SYMBOL,OPEN,HIGH,LOW,PREV CLOSE,LTP,VOLUME (SHARES),VALUE (Rs. IN LAKHS),30 D % CHNG,90 D % CHNG,365 D % CHNG
RELIANCE,2450.50,2485.75,2445.00,2440.00,2470.25,15234567,37450.50,5.67,12.34,45.67
TCS,3250.00,3280.50,3245.00,3240.00,3265.75,8567234,27890.25,3.45,8.90,38.50
INFY,1550.75,1565.00,1548.50,1545.00,1560.25,12345678,19234.75,4.23,10.56,42.30
HDFCBANK,1650.00,1668.50,1645.00,1648.00,1662.75,9876543,16432.50,2.89,7.65,35.20
ICICIBANK,950.25,965.75,948.00,945.00,960.50,11234567,10789.25,4.56,9.87,40.15
```

## Troubleshooting Data Issues

### Issue: "Required columns not found"
**Solution**: 
- Check that your CSV has SYMBOL, OPEN, HIGH, LOW, PREV CLOSE, and LTP (or INDICATIVE CLOSE)
- Open the CSV in a text editor to verify exact column names
- Ensure there are no extra spaces in column names

### Issue: Charts showing strange values
**Solution**:
- Check for non-numeric characters in price/volume columns
- The analyzer auto-cleans commas, ₹, and %, but other characters might cause issues
- Verify decimal points use "." not ","

### Issue: Some stocks missing from analysis
**Solution**:
- Check for empty cells in required columns
- The analyzer drops rows with missing critical data
- Ensure all rows have at least the required columns filled

### Issue: Momentum scores not calculating
**Solution**:
- Verify you have 30 D % CHNG, 90 D % CHNG, or 365 D % CHNG columns
- Check column names match exactly (spaces matter)
- If using different names, update the column_map in the code

## Testing Your CSV

Before uploading a large file, test with a small sample:
1. Create a CSV with 5-10 stocks
2. Include all required columns
3. Upload and verify it loads correctly
4. Then use your full dataset

## Getting Help

If you continue to have data format issues:
1. Compare your CSV with the examples above
2. Check the error message from the analyzer
3. Verify column names match exactly
4. Ensure numeric data is properly formatted
5. Try the minimal working example first

---

**Pro Tip**: The NSE CSV format changes occasionally. If you encounter issues, check if NSE has updated their report format and adjust column names accordingly.
