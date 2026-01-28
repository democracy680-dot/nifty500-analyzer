import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="NIFTY 500 Professional Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS FOR PROFESSIONAL STYLING
# ============================================================================
st.markdown("""
<style>
    /* Main title styling */
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Section headers */
    .section-header {
        color: #2c3e50;
        border-left: 5px solid #3498db;
        padding-left: 10px;
        margin: 2rem 0 1rem 0;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #e8f4f8;
        border-left: 4px solid #3498db;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<h1 class="main-title">📊 NIFTY 500 Professional Market Analyzer</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced Analytics & Real-time Market Intelligence Dashboard</p>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/india-stock-exchange.png", width=80)
    st.title("⚙️ Configuration")
    
    st.markdown("---")
    st.markdown("### 📁 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload NSE NIFTY 500 CSV Report",
        type=["csv"],
        help="Upload the daily NIFTY 500 report from NSE"
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Filter Options")
    
    if uploaded_file is not None:
        min_price_change = st.slider(
            "Min Price Change (%)",
            min_value=-10.0,
            max_value=10.0,
            value=0.0,
            step=0.5
        )
        
        min_volume_multiplier = st.slider(
            "Volume Spike Multiplier",
            min_value=1.0,
            max_value=5.0,
            value=2.0,
            step=0.5,
            help="Filter stocks with volume > multiplier × median volume"
        )
        
        show_advanced = st.checkbox("Show Advanced Analytics", value=True)
        
    st.markdown("---")
    st.markdown("### 📚 About")
    st.info("""
    This dashboard provides comprehensive analysis of NIFTY 500 stocks with:
    - Interactive visualizations
    - Multi-timeframe momentum analysis
    - Volume profile analytics
    - Sector performance tracking
    - Technical pattern recognition
    """)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

if uploaded_file is None:
    st.markdown("""
    <div class="info-box">
        <h3>👋 Welcome to NIFTY 500 Professional Analyzer</h3>
        <p>Please upload a NIFTY 500 CSV file from the sidebar to begin your analysis.</p>
        <p><strong>Features:</strong></p>
        <ul>
            <li>📈 Interactive price & volume charts</li>
            <li>🎯 Smart stock screening & filtering</li>
            <li>📊 Multi-timeframe momentum analysis</li>
            <li>🔍 Pattern recognition & alerts</li>
            <li>💼 Sector-wise performance breakdown</li>
            <li>📉 Risk & volatility metrics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================================================================
# DATA LOADING & PROCESSING
# ============================================================================

try:
    df = pd.read_csv(uploaded_file)
    
    # Clean column names
    df.columns = (
        df.columns.str.upper()
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace("(", "", regex=False)
        .str.replace(")", "", regex=False)
        .str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with single space
    )
    
    # Show debug info in sidebar
    with st.sidebar:
        with st.expander("📋 Debug: Detected Columns"):
            st.text("Available columns in CSV:")
            for col in df.columns[:20]:  # Show first 20 columns
                st.text(f"• {col}")
            if len(df.columns) > 20:
                st.text(f"... and {len(df.columns) - 20} more")
    
    # Column mapping
    column_map = {
        "SYMBOL": ["SYMBOL", "STOCK", "NAME"],
        "OPEN": ["OPEN", "OPEN PRICE"],
        "HIGH": ["HIGH", "HIGH PRICE"],
        "LOW": ["LOW", "LOW PRICE"],
        "PREVCLOSE": ["PREV CLOSE", "PREVIOUS CLOSE", "PREVCLOSE"],
        "CLOSE": ["LTP", "INDICATIVE CLOSE", "CLOSE", "CLOSE PRICE", "LAST PRICE"],
        "VALUE": ["VALUE RS IN LAKHS", "VALUE IN LAKHS", "VALUE"],
        "VOLUME": ["VOLUME SHARES", "VOLUME", "VOL"],
        "30D": ["30 D %CHNG", "30 D CHNG", "30D CHNG", "30 DAY CHANGE"],
        "90D": ["90 D %CHNG", "90 D %CHG", "90 D CHNG", "90D CHNG", "90 DAY CHANGE"],
        "365D": ["365 D %CHNG", "365 D CHNG", "365D CHNG", "365 DAY CHANGE", "1Y CHNG"]
    }
    
    def find_col(possible_names):
        for col in df.columns:
            if col in possible_names:
                return col
        return None
    
    # Find columns
    symbol = find_col(column_map["SYMBOL"])
    open_c = find_col(column_map["OPEN"])
    high = find_col(column_map["HIGH"])
    low = find_col(column_map["LOW"])
    prev = find_col(column_map["PREVCLOSE"])
    close = find_col(column_map["CLOSE"])
    value = find_col(column_map["VALUE"])
    volume = find_col(column_map["VOLUME"])
    day30 = find_col(column_map["30D"])
    day90 = find_col(column_map["90D"])
    day365 = find_col(column_map["365D"])
    
    # Validation
    required_cols = [symbol, open_c, high, low, prev, close]
    missing_cols = []
    
    if symbol is None:
        missing_cols.append("SYMBOL")
    if open_c is None:
        missing_cols.append("OPEN")
    if high is None:
        missing_cols.append("HIGH")
    if low is None:
        missing_cols.append("LOW")
    if prev is None:
        missing_cols.append("PREV CLOSE")
    if close is None:
        missing_cols.append("CLOSE/LTP")
    
    if missing_cols:
        st.error(f"❌ **Required columns not found:** {', '.join(missing_cols)}")
        st.warning("""
        **Expected column names (case-insensitive):**
        - SYMBOL (or STOCK, NAME)
        - OPEN (or OPEN PRICE)
        - HIGH (or HIGH PRICE)
        - LOW (or LOW PRICE)
        - PREV CLOSE (or PREVIOUS CLOSE)
        - CLOSE (or LTP, INDICATIVE CLOSE, LAST PRICE)
        
        **Your CSV has these columns:**
        """)
        st.code(", ".join(df.columns.tolist()))
        st.info("💡 Check the DATA_FORMAT_GUIDE.md file for proper CSV format.")
        st.stop()
    
    # Convert to numeric
    price_cols = [open_c, high, low, prev, close]
    for col in price_cols:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "").str.replace("₹", "").str.strip(),
            errors="coerce"
        )
    
    if volume:
        df[volume] = pd.to_numeric(
            df[volume].astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        )
    
    if value:
        df[value] = pd.to_numeric(
            df[value].astype(str).str.replace(",", "").str.strip(),
            errors="coerce"
        )
    
    for col in [day30, day90, day365]:
        if col:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace("%", "").str.strip(),
                errors="coerce"
            )
    
    # ============================================================================
    # CALCULATIONS & DERIVED METRICS
    # ============================================================================
    
    df["PRICE_CHANGE_%"] = ((df[close] - df[prev]) / df[prev]) * 100
    df["PRICE_CHANGE_ABS"] = df[close] - df[prev]
    df["INTRADAY_RANGE_%"] = ((df[high] - df[low]) / df[prev]) * 100
    df["GAP_%"] = ((df[open_c] - df[prev]) / df[prev]) * 100
    df["HIGH_PROXIMITY_%"] = ((df[close] - df[low]) / (df[high] - df[low])) * 100
    
    # Momentum Score
    momentum = 0
    weights_sum = 0
    if day30:
        momentum += 0.5 * df[day30].fillna(0)
        weights_sum += 0.5
    if day90:
        momentum += 0.3 * df[day90].fillna(0)
        weights_sum += 0.3
    if day365:
        momentum += 0.2 * df[day365].fillna(0)
        weights_sum += 0.2
    
    df["MOMENTUM_SCORE"] = momentum
    
    # Volume Analysis
    if volume:
        median_volume = df[volume].median()
        df["VOLUME_SPIKE"] = df[volume] > (min_volume_multiplier * median_volume)
        df["VOLUME_RATIO"] = df[volume] / median_volume
    else:
        df["VOLUME_SPIKE"] = False
        df["VOLUME_RATIO"] = 1.0
    
    # Behavior Classification
    conditions = [
        (df["PRICE_CHANGE_%"] > 2) & (df["VOLUME_SPIKE"]) & (df["HIGH_PROXIMITY_%"] > 70),
        (df["PRICE_CHANGE_%"] > 1) & (df["INTRADAY_RANGE_%"] > 1.5) & (df["VOLUME_SPIKE"]),
        (df["PRICE_CHANGE_%"] > 0) & (df["INTRADAY_RANGE_%"] < 1),
        (df["PRICE_CHANGE_%"] < 0) & (df["INTRADAY_RANGE_%"] > 2) & (df["VOLUME_SPIKE"]),
        (df["PRICE_CHANGE_%"] < -2) & (df["VOLUME_SPIKE"]),
        (df["PRICE_CHANGE_%"] < -1)
    ]
    choices = [
        "🚀 Breakout",
        "📈 Strong Trend",
        "🟢 Mild Up",
        "⚠️ Distribution",
        "🔴 Breakdown",
        "📉 Exhaustion"
    ]
    df["BEHAVIOR"] = np.select(conditions, choices, default="➖ Normal")
    
    # Volatility Score
    df["VOLATILITY_SCORE"] = df["INTRADAY_RANGE_%"] * df["VOLUME_RATIO"]
    
    # Trading Signal
    signal_conditions = [
        (df["PRICE_CHANGE_%"] > 1) & (df["VOLUME_SPIKE"]) & (df["MOMENTUM_SCORE"] > 0),
        (df["PRICE_CHANGE_%"] < -1) & (df["VOLUME_SPIKE"]) & (df["MOMENTUM_SCORE"] < 0),
    ]
    signal_choices = ["🟢 BUY SIGNAL", "🔴 SELL SIGNAL"]
    df["SIGNAL"] = np.select(signal_conditions, signal_choices, default="⚪ NEUTRAL")
    
    # Remove any rows with NaN in critical columns
    df = df.dropna(subset=[close, "PRICE_CHANGE_%"])
    
    # ============================================================================
    # KEY METRICS DASHBOARD
    # ============================================================================
    
    st.markdown('<h2 class="section-header">📊 Market Overview</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_stocks = len(df)
    advancers = (df["PRICE_CHANGE_%"] > 0).sum()
    decliners = (df["PRICE_CHANGE_%"] < 0).sum()
    unchanged = total_stocks - advancers - decliners
    avg_change = df["PRICE_CHANGE_%"].mean()
    
    with col1:
        st.metric(
            "Total Stocks",
            f"{total_stocks}",
            delta=None,
            delta_color="off"
        )
    
    with col2:
        st.metric(
            "Advancers",
            f"{advancers}",
            delta=f"{(advancers/total_stocks)*100:.1f}%",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Decliners",
            f"{decliners}",
            delta=f"{(decliners/total_stocks)*100:.1f}%",
            delta_color="inverse"
        )
    
    with col4:
        st.metric(
            "Unchanged",
            f"{unchanged}",
            delta=None,
            delta_color="off"
        )
    
    with col5:
        st.metric(
            "Avg Change",
            f"{avg_change:.2f}%",
            delta=None,
            delta_color="normal" if avg_change > 0 else "inverse"
        )
    
    # ============================================================================
    # MARKET SENTIMENT GAUGE
    # ============================================================================
    
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Advance-Decline Pie Chart
        fig_sentiment = go.Figure(data=[go.Pie(
            labels=['Advancers', 'Decliners', 'Unchanged'],
            values=[advancers, decliners, unchanged],
            hole=.4,
            marker_colors=['#28a745', '#dc3545', '#6c757d'],
            textinfo='label+percent',
            textfont_size=14
        )])
        
        fig_sentiment.update_layout(
            title="Market Breadth Analysis",
            title_font_size=18,
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig_sentiment, use_container_width=True)
    
    with col2:
        # Market Sentiment Indicator
        sentiment_score = ((advancers - decliners) / total_stocks) * 100
        
        if sentiment_score > 20:
            sentiment = "🟢 Bullish"
            sentiment_color = "#28a745"
        elif sentiment_score > 0:
            sentiment = "🟡 Mildly Bullish"
            sentiment_color = "#ffc107"
        elif sentiment_score > -20:
            sentiment = "🟠 Mildly Bearish"
            sentiment_color = "#fd7e14"
        else:
            sentiment = "🔴 Bearish"
            sentiment_color = "#dc3545"
        
        st.markdown(f"""
        <div style="background-color: {sentiment_color}20; padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;">
            <h2 style="color: {sentiment_color}; margin: 0;">Market Sentiment</h2>
            <h1 style="color: {sentiment_color}; margin: 10px 0;">{sentiment}</h1>
            <p style="font-size: 1.5rem; font-weight: bold; color: {sentiment_color}; margin: 0;">
                {sentiment_score:+.1f}%
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # ============================================================================
    # PRICE CHANGE DISTRIBUTION
    # ============================================================================
    
    st.markdown('<h2 class="section-header">📈 Price Change Distribution</h2>', unsafe_allow_html=True)
    
    fig_dist = go.Figure()
    
    fig_dist.add_trace(go.Histogram(
        x=df["PRICE_CHANGE_%"],
        nbinsx=50,
        name="Price Change Distribution",
        marker_color='#3498db',
        opacity=0.7
    ))
    
    fig_dist.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="Neutral")
    fig_dist.add_vline(x=avg_change, line_dash="dot", line_color="green", 
                       annotation_text=f"Avg: {avg_change:.2f}%")
    
    fig_dist.update_layout(
        title="Distribution of Stock Returns",
        xaxis_title="Price Change (%)",
        yaxis_title="Number of Stocks",
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # ============================================================================
    # TOP GAINERS & LOSERS
    # ============================================================================
    
    st.markdown('<h2 class="section-header">🏆 Top Performers & Laggards</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🚀 Top 10 Gainers")
        top_gainers = df.nlargest(10, "PRICE_CHANGE_%")
        
        fig_gainers = go.Figure(go.Bar(
            x=top_gainers["PRICE_CHANGE_%"],
            y=top_gainers[symbol],
            orientation='h',
            marker=dict(
                color=top_gainers["PRICE_CHANGE_%"],
                colorscale='Greens',
                showscale=False
            ),
            text=top_gainers["PRICE_CHANGE_%"].round(2),
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>'
        ))
        
        fig_gainers.update_layout(
            height=400,
            yaxis={'categoryorder': 'total ascending'},
            xaxis_title="Price Change (%)",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_gainers, use_container_width=True)
    
    with col2:
        st.markdown("### 🔻 Top 10 Losers")
        top_losers = df.nsmallest(10, "PRICE_CHANGE_%")
        
        fig_losers = go.Figure(go.Bar(
            x=top_losers["PRICE_CHANGE_%"],
            y=top_losers[symbol],
            orientation='h',
            marker=dict(
                color=top_losers["PRICE_CHANGE_%"],
                colorscale='Reds',
                reversescale=True,
                showscale=False
            ),
            text=top_losers["PRICE_CHANGE_%"].round(2),
            texttemplate='%{text}%',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Change: %{x:.2f}%<extra></extra>'
        ))
        
        fig_losers.update_layout(
            height=400,
            yaxis={'categoryorder': 'total descending'},
            xaxis_title="Price Change (%)",
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_losers, use_container_width=True)
    
    # ============================================================================
    # VOLUME ANALYSIS
    # ============================================================================
    
    if volume:
        st.markdown('<h2 class="section-header">📊 Volume Analysis</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Volume Spike Leaders
            st.markdown("### 🔥 Highest Volume Spikes")
            volume_leaders = df.nlargest(10, "VOLUME_RATIO")
            
            fig_volume = go.Figure(go.Bar(
                x=volume_leaders["VOLUME_RATIO"],
                y=volume_leaders[symbol],
                orientation='h',
                marker=dict(
                    color=volume_leaders["VOLUME_RATIO"],
                    colorscale='Oranges',
                    showscale=False
                ),
                text=volume_leaders["VOLUME_RATIO"].round(2),
                texttemplate='%{text}x',
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Volume Ratio: %{x:.2f}x<extra></extra>'
            ))
            
            fig_volume.update_layout(
                height=400,
                yaxis={'categoryorder': 'total ascending'},
                xaxis_title="Volume Ratio (vs Median)",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_volume, use_container_width=True)
        
        with col2:
            # Volume vs Price Change Scatter
            st.markdown("### 📊 Volume vs Price Change")
            
            fig_scatter = px.scatter(
                df,
                x="PRICE_CHANGE_%",
                y="VOLUME_RATIO",
                color="BEHAVIOR",
                size="VOLATILITY_SCORE",
                hover_data=[symbol],
                color_discrete_map={
                    "🚀 Breakout": "#28a745",
                    "📈 Strong Trend": "#20c997",
                    "🟢 Mild Up": "#5cb85c",
                    "➖ Normal": "#6c757d",
                    "⚠️ Distribution": "#ffc107",
                    "📉 Exhaustion": "#fd7e14",
                    "🔴 Breakdown": "#dc3545"
                }
            )
            
            fig_scatter.update_layout(
                height=400,
                xaxis_title="Price Change (%)",
                yaxis_title="Volume Ratio",
                showlegend=True,
                legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02)
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # ============================================================================
    # MOMENTUM HEATMAP
    # ============================================================================
    
    if day30 or day90 or day365:
        st.markdown('<h2 class="section-header">🔥 Multi-Timeframe Momentum Analysis</h2>', unsafe_allow_html=True)
        
        # Create momentum dataframe for top stocks - only include available columns
        momentum_cols = [symbol]
        timeframe_labels = []
        
        if day30:
            momentum_cols.append(day30)
            timeframe_labels.append('30 Days')
        if day90:
            momentum_cols.append(day90)
            timeframe_labels.append('90 Days')
        if day365:
            momentum_cols.append(day365)
            timeframe_labels.append('365 Days')
        
        if len(momentum_cols) > 1:  # At least symbol + one timeframe column
            momentum_df = df.nlargest(20, "MOMENTUM_SCORE")[momentum_cols].copy()
            momentum_df = momentum_df.set_index(symbol)
            
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=momentum_df.values.T,
                x=momentum_df.index,
                y=timeframe_labels,
                colorscale='RdYlGn',
                text=momentum_df.values.T,
                texttemplate='%{text:.1f}%',
                textfont={"size": 10},
                colorbar=dict(title="Change %")
            ))
            
            fig_heatmap.update_layout(
                title="Top 20 Stocks by Momentum Score - Multi-Timeframe Performance",
                height=300,
                xaxis_title="Stock Symbol",
                yaxis_title="Timeframe"
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("💡 Multi-timeframe data (30D/90D/365D columns) not available in the uploaded file. Upload a file with historical change columns to see momentum analysis.")
    
    # ============================================================================
    # ACTIONABLE INSIGHTS & SIGNALS
    # ============================================================================
    
    st.markdown('<h2 class="section-header">🎯 Actionable Trading Signals</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🟢 Buy Signals", "🔴 Sell Signals", "⭐ High Conviction"])
    
    with tab1:
        buy_signals = df[df["SIGNAL"] == "🟢 BUY SIGNAL"].sort_values("MOMENTUM_SCORE", ascending=False)
        st.markdown(f"**Found {len(buy_signals)} stocks with BUY signals**")
        
        if len(buy_signals) > 0:
            display_cols = [symbol, close, "PRICE_CHANGE_%", "VOLUME_RATIO", "MOMENTUM_SCORE", 
                          "INTRADAY_RANGE_%", "BEHAVIOR"]
            if day30:
                display_cols.append(day30)
            
            st.dataframe(
                buy_signals[display_cols].head(20),
                use_container_width=True,
                height=400
            )
        else:
            st.info("No buy signals found with current criteria.")
    
    with tab2:
        sell_signals = df[df["SIGNAL"] == "🔴 SELL SIGNAL"].sort_values("MOMENTUM_SCORE")
        st.markdown(f"**Found {len(sell_signals)} stocks with SELL signals**")
        
        if len(sell_signals) > 0:
            display_cols = [symbol, close, "PRICE_CHANGE_%", "VOLUME_RATIO", "MOMENTUM_SCORE", 
                          "INTRADAY_RANGE_%", "BEHAVIOR"]
            if day30:
                display_cols.append(day30)
            
            st.dataframe(
                sell_signals[display_cols].head(20),
                use_container_width=True,
                height=400
            )
        else:
            st.info("No sell signals found with current criteria.")
    
    with tab3:
        high_conviction = df[
            (df["VOLUME_SPIKE"]) &
            (df["PRICE_CHANGE_%"].abs() > 2) &
            (df["MOMENTUM_SCORE"].abs() > 3)
        ].sort_values("PRICE_CHANGE_%", ascending=False)
        
        st.markdown(f"**Found {len(high_conviction)} high conviction opportunities**")
        st.markdown("*Stocks with strong price move, high volume, and positive momentum*")
        
        if len(high_conviction) > 0:
            display_cols = [symbol, close, "PRICE_CHANGE_%", "VOLUME_RATIO", "MOMENTUM_SCORE", 
                          "VOLATILITY_SCORE", "BEHAVIOR", "SIGNAL"]
            
            st.dataframe(
                high_conviction[display_cols],
                use_container_width=True,
                height=400
            )
        else:
            st.info("No high conviction opportunities found with current criteria.")
    
    # ============================================================================
    # BEHAVIOR BREAKDOWN
    # ============================================================================
    
    st.markdown('<h2 class="section-header">🎭 Market Behavior Breakdown</h2>', unsafe_allow_html=True)
    
    behavior_counts = df["BEHAVIOR"].value_counts()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_behavior = go.Figure(data=[go.Bar(
            x=behavior_counts.index,
            y=behavior_counts.values,
            marker_color=['#28a745', '#20c997', '#5cb85c', '#6c757d', '#ffc107', '#fd7e14', '#dc3545'],
            text=behavior_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
        )])
        
        fig_behavior.update_layout(
            title="Stock Count by Behavior Pattern",
            xaxis_title="Behavior",
            yaxis_title="Number of Stocks",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig_behavior, use_container_width=True)
    
    with col2:
        st.markdown("### 📋 Behavior Legend")
        st.markdown("""
        - **🚀 Breakout**: Strong upward move with high volume
        - **📈 Strong Trend**: Significant price & volume increase
        - **🟢 Mild Up**: Gentle upward movement
        - **➖ Normal**: Stable, no significant movement
        - **⚠️ Distribution**: Price drop with high volume
        - **📉 Exhaustion**: Declining with low momentum
        - **🔴 Breakdown**: Sharp decline with high volume
        """)
    
    # ============================================================================
    # ADVANCED ANALYTICS (if enabled)
    # ============================================================================
    
    if show_advanced:
        st.markdown('<h2 class="section-header">🔬 Advanced Analytics</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Volatility Analysis
            st.markdown("### 📊 Volatility Distribution")
            
            fig_volatility = px.box(
                df,
                y="VOLATILITY_SCORE",
                color="BEHAVIOR",
                points="outliers",
                color_discrete_map={
                    "🚀 Breakout": "#28a745",
                    "📈 Strong Trend": "#20c997",
                    "🟢 Mild Up": "#5cb85c",
                    "➖ Normal": "#6c757d",
                    "⚠️ Distribution": "#ffc107",
                    "📉 Exhaustion": "#fd7e14",
                    "🔴 Breakdown": "#dc3545"
                }
            )
            
            fig_volatility.update_layout(
                height=400,
                yaxis_title="Volatility Score",
                showlegend=True
            )
            
            st.plotly_chart(fig_volatility, use_container_width=True)
        
        with col2:
            # Gap Analysis
            st.markdown("### 📉 Gap Analysis")
            
            gap_stats = {
                "Gap Up (>1%)": (df["GAP_%"] > 1).sum(),
                "Gap Down (<-1%)": (df["GAP_%"] < -1).sum(),
                "Flat Open": ((df["GAP_%"] >= -1) & (df["GAP_%"] <= 1)).sum()
            }
            
            fig_gap = go.Figure(data=[go.Pie(
                labels=list(gap_stats.keys()),
                values=list(gap_stats.values()),
                marker_colors=['#28a745', '#dc3545', '#6c757d'],
                hole=.3
            )])
            
            fig_gap.update_layout(
                title="Opening Gap Distribution",
                height=400,
                showlegend=True
            )
            
            st.plotly_chart(fig_gap, use_container_width=True)
    
    # ============================================================================
    # COMPLETE DATA TABLE
    # ============================================================================
    
    st.markdown('<h2 class="section-header">📋 Complete Market Data</h2>', unsafe_allow_html=True)
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        behavior_filter = st.multiselect(
            "Filter by Behavior",
            options=df["BEHAVIOR"].unique(),
            default=None
        )
    
    with col2:
        signal_filter = st.multiselect(
            "Filter by Signal",
            options=df["SIGNAL"].unique(),
            default=None
        )
    
    with col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["PRICE_CHANGE_%", "VOLUME_RATIO", "MOMENTUM_SCORE", "VOLATILITY_SCORE", close],
            index=0
        )
    
    # Apply filters
    filtered_df = df.copy()
    
    if behavior_filter:
        filtered_df = filtered_df[filtered_df["BEHAVIOR"].isin(behavior_filter)]
    
    if signal_filter:
        filtered_df = filtered_df[filtered_df["SIGNAL"].isin(signal_filter)]
    
    filtered_df = filtered_df.sort_values(sort_by, ascending=False)
    
    # Display table
    display_columns = [symbol, close, "PRICE_CHANGE_%", "PRICE_CHANGE_ABS", 
                      "INTRADAY_RANGE_%", "VOLUME_RATIO", "MOMENTUM_SCORE", 
                      "BEHAVIOR", "SIGNAL"]
    
    # Add optional columns if they exist
    if day30 and day30 in df.columns:
        display_columns.append(day30)
    if day90 and day90 in df.columns:
        display_columns.append(day90)
    if day365 and day365 in df.columns:
        display_columns.append(day365)
    
    st.dataframe(
        filtered_df[display_columns].reset_index(drop=True),
        use_container_width=True,
        height=500
    )
    
    # Export option
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name="nifty500_analysis.csv",
            mime="text/csv"
        )
    
    with col2:
        st.metric("Filtered Results", len(filtered_df))

except Exception as e:
    st.error(f"❌ Error processing file: {str(e)}")
    st.info("Please ensure the CSV file is in the correct format from NSE.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>NIFTY 500 Professional Analyzer</strong> | Built with Streamlit & Plotly</p>
    <p style='font-size: 0.9rem;'>⚠️ Disclaimer: This tool is for informational purposes only. Not financial advice.</p>
</div>
""", unsafe_allow_html=True)