# Step 1 - Read API once
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.set_page_config(page_title="Live API Demo (Simple)", page_icon="📡", layout="wide")
# Disable fade/transition so charts don't blink between reruns
st.markdown("""
    <style>
      [data-testid="stPlotlyChart"], .stPlotlyChart, .stElementContainer {
        transition: none !important;
        opacity: 1 !important;
      }
    </style>
""", unsafe_allow_html=True)

st.title("📡 Simple Live Data Demo (Open-Meteo)")
st.caption("Friendly demo with manual refresh + fallback data so it never crashes.")


lat, lon = 39.7392, -104.9903  # Denver
# Documentation: https://open-meteo.com/en/docs
# Fetch current weather
wurl = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m"

# Fetch hourly forecast data (returns arrays)
hourly_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,wind_speed_10m&past_days=1"

@st.cache_data(ttl=600) # cached for 10 minutes
def get_weather():
    r = requests.get(wurl, timeout=10); r.raise_for_status()
    j = r.json()["current"]
    return pd.DataFrame([{"time": pd.to_datetime(j["time"]),
                          "temperature (°C)": j["temperature_2m"],
                          "wind (km/h)": j["wind_speed_10m"]}])

st.subheader("Weather Data")


@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def fetch_weather(url: str):
    """Return (df, error_message). Never raise. Safe for beginners."""
    try:
        resp = requests.get(url, timeout=10)
        # Handle 429 and other non-200s
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After", "a bit")
            return None, f"429 Too Many Requests — try again after {retry_after}s"
        resp.raise_for_status()
        data = resp.json()
        current = data["current"]
        df = pd.DataFrame([{
            "time": pd.to_datetime(current["time"]),
            "temperature (°C)": current["temperature_2m"],
            "wind (km/h)": current["wind_speed_10m"]
        }])
        return df, None
    except requests.RequestException as e:
        return None, f"Network/HTTP error: {e}"

@st.cache_data(ttl=600, show_spinner=False)  # Cache for 10 minutes
def fetch_hourly_weather(url: str):
    """Fetch hourly weather data (returns arrays). Returns (df, error_message)."""
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 429:
            retry_after = resp.headers.get("Retry-After", "a bit")
            return None, f"429 Too Many Requests — try again after {retry_after}s"
        resp.raise_for_status()
        data = resp.json()
        hourly = data["hourly"]
        
        # Convert arrays to DataFrame
        df = pd.DataFrame({
            "time": pd.to_datetime(hourly["time"]),
            "temperature (°C)": hourly["temperature_2m"],
            "wind (km/h)": hourly["wind_speed_10m"]
        })
        return df, None
    except requests.RequestException as e:
        return None, f"Network/HTTP error: {e}"

# Step 4 - REFRESH BUTTON
# --- Auto Refresh Controls ---
st.subheader("🔁 Auto Refresh Settings")

# Let user choose how often to refresh (in seconds)
refresh_sec = st.slider("Refresh every (sec)", 10, 120, 30)

# Toggle to turn automatic refreshing on/off
auto_refresh = st.toggle("Enable auto-refresh", value=False)

# Show current refresh time
st.caption(f"Last refreshed at: {time.strftime('%H:%M:%S')}")

# Step 5 - MAIN VIEW
st.subheader("Live Weather Data (with Auto-Refresh)")
df, err = fetch_weather(wurl)

if err:
    st.warning(f"{err}\nShowing sample data so the demo continues.")
    df = pd.DataFrame([{"time": pd.to_datetime("2025-10-22 16:41:55"), "temperature (°C)": 21.8, "wind (km/h)": 7.4}])

st.dataframe(df, use_container_width=True)

# --- TIME SERIES VISUALIZATION ---
st.subheader("📈 Weather Trends Over Time")

# Fetch hourly data from API (past 24 hours + forecast)
hourly_df, hourly_err = fetch_hourly_weather(hourly_url)

if hourly_err:
    st.warning(f"Could not fetch hourly data: {hourly_err}")
elif hourly_df is not None and len(hourly_df) > 0:
    # Create dual-axis line chart using Plotly
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add temperature trace
    fig.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['temperature (°C)'],
            name="Temperature",
            line=dict(color='#FF6B6B', width=3),
            mode='lines+markers'
        ),
        secondary_y=False,
    )
    
    # Add wind speed trace
    fig.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['wind (km/h)'],
            name="Wind Speed",
            line=dict(color='#4ECDC4', width=3),
            mode='lines+markers'
        ),
        secondary_y=True,
    )
    
    # Update layout
    fig.update_xaxes(title_text="Time")
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=False, color='#FF6B6B')
    fig.update_yaxes(title_text="Wind Speed (km/h)", secondary_y=True, color='#4ECDC4')
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data point count
    st.caption(f"📊 Showing {len(hourly_df)} hourly data points (past 24 hours)")
else:
    st.info("Waiting for hourly data...")

# If auto-refresh is ON, wait and rerun the app
if auto_refresh:
    time.sleep(refresh_sec)
    fetch_weather.clear()
    st.rerun()