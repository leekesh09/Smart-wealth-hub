import streamlit as st

st.set_page_config(
    page_title="Stock Guide App",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
    <style>
        .theme-success {
            background: linear-gradient(90deg, #172554, #1e3a8a, #1d4ed8);
            border-left: 6px solid #38bdf8;
            color: white;
            padding: 16px 20px;
            border-radius: 16px;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
            margin-bottom: 14px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="theme-success">
        ✅ Welcome! Explore stock data, future predictions, and risk analysis in one dashboard.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #0f172a, #1e293b);
        }

        .hero-box {
            background: linear-gradient(135deg, #1d4ed8, #2563eb, #0ea5e9);
            padding: 30px;
            border-radius: 20px;
            color: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.25);
            margin-bottom: 20px;
        }

        .feature-card {
            background-color: #ffffff;
            padding: 22px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
            border-left: 6px solid #2563eb;
            margin-bottom: 18px;
        }

        .feature-title {
            font-size: 22px;
            font-weight: bold;
            color: #0f172a;
            margin-bottom: 10px;
        }

        .feature-text {
            font-size: 16px;
            color: #334155;
        }

        .highlight {
            color: #facc15;
            font-weight: bold;
        }

        .small-box {
            background: #f8fafc;
            padding: 18px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            text-align: center;
            color: #1e293b;
        }

        .footer-box {
            background: linear-gradient(135deg, #111827, #1f2937);
            color: white;
            padding: 20px;
            border-radius: 18px;
            margin-top: 30px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 Navigation")
st.sidebar.info("""
Welcome to the **Stock Guide App**.

Use this platform to:
- Analyze stock data
- View future price predictions
- Calculate CAPM returns
- Measure Beta risk
- Make better investment decisions
""")

st.sidebar.markdown("### 📌 Market Highlights")
st.sidebar.success("✔ Real-time style dashboard")
st.sidebar.warning("✔ Prediction-based insights")
st.sidebar.info("✔ Risk and return analysis")

st.markdown("""
    <div class="hero-box">
        <h1>📈 Stock Guide App</h1>
        <h4>Your smart assistant for stock analysis, forecasting, and investment insights</h4>
        <p>
            Explore powerful tools to analyze stock market trends, predict future prices,
            and evaluate risk using financial models like <span class="highlight">CAPM</span>.
            This platform is designed for students, beginners, and investors who want a
            professional stock market dashboard experience.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("## 📌 Dashboard Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="📊 Stocks Covered", value="500+", delta="Live Analysis")

with col2:
    st.metric(label="📈 Prediction Window", value="30 Days", delta="Forecast Ready")

with col3:
    st.metric(label="⚖ Risk Analysis", value="CAPM Beta", delta="Smart Calculation")

with col4:
    st.metric(label="💹 Market Insights", value="Advanced", delta="Decision Support")

st.markdown("## 🚀 Services We Provide")
st.write("""
This application helps users understand the stock market in a simple and interactive way.
From stock information to future forecasting and risk-return analysis, this platform combines
financial knowledge with data science to support smarter investment decisions.
""")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">1️⃣ Stock Information</div>
            <div class="feature-text">
                Access detailed information about your selected stocks including historical trends,
                company-related insights, price movements, and market behavior. This section gives
                users a strong foundation before making any investment decision.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">2️⃣ Stock Price Prediction</div>
            <div class="feature-text">
                Explore predicted closing prices for upcoming days using historical stock data and
                forecasting models. This module helps users estimate future trends and identify
                possible opportunities in the market.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">3️⃣ CAPM Return</div>
            <div class="feature-text">
                Understand the expected return of a stock using the Capital Asset Pricing Model (CAPM).
                This feature helps investors compare return expectations with the level of market risk involved.
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">4️⃣ CAPM Beta</div>
            <div class="feature-text">
                Calculate Beta to measure how sensitive a stock is compared to the overall market.
                A higher beta indicates higher volatility, while a lower beta suggests relatively stable movement.
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("## 💡 Why Use This App?")
a, b, c = st.columns(3)

with a:
    st.markdown("""
        <div class="small-box">
            <h4>📘  Beginner Friendly</h4>
            <p>Simple interface for students and new investors to understand stock analysis easily.</p>
        </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
        <div class="small-box">
            <h4>🤖 Data-Driven Prediction</h4>
            <p>Uses forecasting models and financial calculations to generate useful investment insights.</p>
        </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
        <div class="small-box">
            <h4>📉 Risk Management</h4>
            <p>Helps users evaluate stock risk, beta, and expected return before making decisions.</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="footer-box">
        <h3>📍 Start Your Smart Investment Journey Today</h3>
        <p>
            Analyze stocks, predict prices, and understand risk-return relationships
            all in one place with the Stock Guide App.
        </p>
    </div>
""", unsafe_allow_html=True)

st.warning("Disclaimer: This app is for educational and informational purposes only. It does not provide financial advice.")