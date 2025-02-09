import streamlit as st
import pandas as pd

# --- ✅ Fix: Set Page Config as the first command ---
st.set_page_config(page_title="Select Your Plan", layout="wide")

# --- Custom Styling for a Tech-Like UI ---
st.markdown("""
    <style>
        /* Center the plan selection */
        .plan-selection {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        /* Styling for plan selection buttons */
        .plan-button {
            background: none;
            border: none;
            font-size: 22px;
            font-weight: normal;
            color: grey;
            cursor: pointer;
            padding: 8px 15px;
        }
        .plan-button-selected {
            background: none;
            border: none;
            font-size: 22px;
            font-weight: bold;
            color: black;
            cursor: pointer;
            padding: 8px 15px;
        }
        .divider {
            font-size: 22px;
            font-weight: bold;
            color: black;
            padding: 0 10px;
        }
        /* Table Styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 18px;
            border-radius: 10px;
            overflow: hidden;
        }
        th {
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        /* Make total row bold */
        tr:last-child td {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- Plan Selection (Monthly / Annual) ---
st.markdown("<div class='plan-selection'>Select Your Plan</div>", unsafe_allow_html=True)

# Initialize session state if not set
if "plan" not in st.session_state:
    st.session_state["plan"] = "monthly"

# Center-aligned buttons
col1, col2, col3, col4, col5 = st.columns([2, 2, 0.5, 2, 2])  
with col2:
    if st.button("Monthly", key="monthly", help="Click to select Monthly plan",
                 use_container_width=True):
        st.session_state["plan"] = "monthly"
with col3:
    st.markdown("<p class='divider'>/</p>", unsafe_allow_html=True)
with col4:
    if st.button("Annual (-20%)", key="annual", help="Click to select Annual plan",
                 use_container_width=True):
        st.session_state["plan"] = "annual"

# Apply styling to selected button
st.markdown(f"""
    <style>
        [data-testid="stButton"] button {{
            background: none !important;
            border: none !important;
            font-size: 22px !important;
            font-weight: normal !important;
            color: grey !important;
            padding: 8px 15px !important;
        }}
        [data-testid="stButton"]:nth-child({2 if st.session_state["plan"] == "monthly" else 4}) button {{
            font-weight: bold !important;
            color: black !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.write("")

# --- Monitoring Frequency Selection (in one row) ---
col_freq1, col_freq2 = st.columns([1, 2])
with col_freq1:
    st.markdown("<p style='font-size:18px; font-weight:bold;'>Monitoring Frequency</p>", unsafe_allow_html=True)
with col_freq2:
    frequency_options = {"Daily": 30, "Twice Weekly": 8, "Weekly": 4, "Bi-Weekly": 2, "Monthly": 1}
    selected_frequency = st.selectbox("", list(frequency_options.keys()), index=2, key="monitoring_freq")

st.write("")

# --- Data Setup ---
websites = [
    {"website": "bonami.cz", "fixed_fee": 150, "data_updates": 608},
    {"website": "helveti.cz", "fixed_fee": 150, "data_updates": 120},
    {"website": "biano.cz", "fixed_fee": 150, "data_updates": 5}
]

# Convert to DataFrame
df = pd.DataFrame(websites)

# Apply frequency multiplier
frequency_multiplier = frequency_options[selected_frequency]
df["Total Price"] = df["fixed_fee"] + df["data_updates"] * frequency_multiplier

# Apply annual discount if selected
if st.session_state["plan"] == "annual":
    df["Total Price"] *= 0.8

# Format Prices
df["Total Price"] = df["Total Price"].astype(int).astype(str) + " Kč"
df["fixed_fee"] = df["fixed_fee"].astype(str) + " Kč"
df["data_updates"] = df["data_updates"].astype(str) + f" × {frequency_multiplier}"

# Sum Totals
total_fixed_fee = sum([150 for _ in range(len(df))])
total_data_updates = sum([w["data_updates"] for w in websites]) * frequency_multiplier
total_price = sum([int(price.split()[0]) for price in df["Total Price"]])

# Add TOTAL row
df.loc[len(df)] = ["TOTAL", f"{total_price} Kč", f"{total_fixed_fee} Kč", f"{total_data_updates} × {frequency_multiplier}"]

# --- Display Table ---
st.write("")
st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)
