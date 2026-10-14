
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Lebanon Estate AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    return joblib.load("lebanon_house_model.pkl")

@st.cache_data
def load_data():
    return pd.read_csv("lebanon_housing_clean.csv")

model = load_model()
df = load_data()
regions = sorted(df["region"].dropna().unique())

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #0b1120;
    color: #f1f5f9;
    font-family: 'Inter', sans-serif;
}
.block-container {
    max-width: 900px;
    padding: 0.7rem 1.5rem 0.5rem;
}
#MainMenu, footer {visibility: hidden;}
header[data-testid="stHeader"] {height: 1.5rem; background: transparent;}

.hero {
    text-align: center;
    padding: 17px 20px 13px;
    background: linear-gradient(120deg, #172554, #172033, #263449);
    border: 1px solid #334155;
    border-radius: 18px;
    margin-bottom: 12px;
}
.eyebrow {
    color: #fbbf24;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}
.hero h1 {
    color: #fff;
    font-size: 30px;
    font-weight: 800;
    margin: 7px 0;
    line-height: 1.2;
}
.hero p {
    color: #cbd5e1;
    font-size: 12px;
    margin: 0;
}
.stats {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
}
.stat {
    flex: 1;
    text-align: center;
    background: #141e30;
    border: 1px solid #29364b;
    border-radius: 12px;
    padding: 9px;
}
.stat-label {
    color: #94a3b8;
    font-size: 10px;
}
.stat-value {
    color: #fbbf24;
    font-size: 19px;
    font-weight: 800;
    margin-top: 3px;
}
.form-card {
    background: #141e30;
    border: 1px solid #29364b;
    border-radius: 16px;
    padding: 17px 20px 12px;
}
.form-title {
    color: #fff;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 3px;
}
.form-subtitle {
    color: #94a3b8;
    font-size: 11px;
    margin-bottom: 10px;
}
label {
    color: #e2e8f0 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
}
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #0b1120;
    border: 1px solid #3a4960;
    border-radius: 9px;
    color: #fff;
}
div[data-baseweb="select"] * {color: #fff;}
.stNumberInput, .stSelectbox {margin-bottom: 0.35rem;}
.stButton > button {
    background: #fbbf24;
    color: #111827;
    border: none;
    border-radius: 9px;
    min-height: 42px;
    font-size: 12px;
    font-weight: 800;
}
.stButton > button:hover {
    background: #fcd34d;
    color: #111827;
    border: none;
}
.result {
    text-align: center;
    background: linear-gradient(120deg, #1c2d42, #18283a);
    border: 1px solid #d6a72c;
    border-radius: 14px;
    padding: 13px;
    margin-top: 12px;
}
.result-label {
    color: #cbd5e1;
    font-size: 10px;
    letter-spacing: 1.5px;
}
.result-price {
    color: #fbbf24;
    font-size: 32px;
    font-weight: 800;
    margin: 3px 0;
}
.result-meta {
    color: #cbd5e1;
    font-size: 11px;
}
.note {
    color: #94a3b8;
    font-size: 10px;
    text-align: center;
    margin-top: 10px;
    line-height: 1.5;
}
.footer {
    color: #64748b;
    font-size: 9px;
    text-align: center;
    margin-top: 9px;
}
div[data-testid="stAlert"] {
    padding: 7px 12px;
    margin-top: 8px;
    border-radius: 9px;
    font-size: 11px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero">
    <div class="eyebrow">PROPERTY INTELLIGENCE · LEBANON</div>
    <h1>Lebanon Estate AI</h1>
    <p>Smart apartment price estimates, powered by machine learning.</p>
</div>
""", unsafe_allow_html=True)

# Compact statistics
st.markdown(f"""
<div class="stats">
    <div class="stat">
        <div class="stat-label">LISTINGS</div>
        <div class="stat-value">{len(df)}</div>
    </div>
    <div class="stat">
        <div class="stat-label">REGIONS</div>
        <div class="stat-value">{df["region"].nunique()}</div>
    </div>
    <div class="stat">
        <div class="stat-label">MODEL</div>
        <div class="stat-value" style="font-size:16px">Random Forest</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Single centered form
st.markdown("""
<div class="form-card">
    <div class="form-title">Estimate your apartment price</div>
    <div class="form-subtitle">
        Enter the property details below to generate an estimate.
    </div>
</div>
""", unsafe_allow_html=True)

area = st.number_input(
    "Apartment area (m²)",
    min_value=20.0,
    max_value=2000.0,
    value=150.0,
    step=5.0
)

default_region = (
    regions.index("Hadath, Baabda")
    if "Hadath, Baabda" in regions else 0
)

region = st.selectbox(
    "Select location",
    regions,
    index=default_region
)

predict = st.button(
    "✦  PREDICT APARTMENT PRICE",
    type="primary",
    use_container_width=True
)

if predict:
    apartment = pd.DataFrame({
        "area_m2": [area],
        "region": [region]
    })

    predicted_price = model.predict(apartment)[0]

    st.markdown(f"""
    <div class="result">
        <div class="result-label">ESTIMATED ASKING PRICE</div>
        <div class="result-price">${predicted_price:,.0f}</div>
        <div class="result-meta">{region} · {area:,.0f} m²</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "This is an experimental estimate, not a professional valuation."
    )

st.markdown("""
<div class="note">
    Based on 223 collected listings across 99 regions.<br>
    Current test R²: 0.201 · Predictions may differ substantially from market prices.
</div>
<div class="footer">
    LEBANON ESTATE AI · MACHINE LEARNING PROJECT
</div>
""", unsafe_allow_html=True)
