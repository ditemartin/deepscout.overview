import streamlit as st
import pandas as pd

# --- ✅ Fix: Set Page Config as the first command ---
st.set_page_config(page_title="Select Your Plan", layout="wide")

# --- Custom Styling for a Tech-Like UI ---
st.markdown("""
    <style>
        /* Center the plan selection text */
        .plan-selection {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        /* Styling for plan selection (clickable text) */
        .plan-option {
            display: inline-block;
            padding: 8px 15px;
            font-size: 20px;
            font-weight: bold;
            color: grey;
            cursor: pointer;
            margin: 0 5px;
        }
        .selected-plan {
            font-weight: bold;
            color: black;
            text-decoration: underline;
        }
        /* Monitoring Frequency Dropdown */
        .monitoring-container {
            background-color: #BBBBBB;
            padding: 10px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        }
        /* Table Styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            font-size: 18px;
            border-radius: 10px; /* Rounded corners */
            overflow: hidden;
        }
        th {
            background-color: #BBBBBB;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        .total-row {
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --- Plan Selection (Monthly / Annual) ---
st.markdown("<div class='plan-selection'>Select Your Plan</div>", unsafe_allow_html=True)

# Initialize session state if not set
if "plan" not in st.session_state:
    st.session_state["plan"] = "monthly"

# Center-aligned text selection
col1, col2, col3 = st.columns([1.5, 2, 1.5])  
with col2:
    # Dynamic classes for text highlighting
    monthly_class = "selected-plan" if st.session_state["plan"] == "monthly" else "plan-option"
    annual_class = "selected-plan" if st.session_state["plan"] == "annual" else "plan-option"

    # Clickable text elements using buttons (to properly trigger session state update)
    colA, colB = st.columns([0.5, 0.5])
    with colA:
        if st.button("Monthly", key="monthly", help="Click to select Monthly plan"):
            st.session_state["plan"] = "monthly"
    with colB:
        if st.button("Annual (-20%)", key="annual", help="Click to select Annual plan"):
            st.session_state["plan"] = "annual"

# Display selected plan as styled text
st.markdown(f"<p style='text-align:center; font-size:20px;'><span class='{monthly_class}'>Monthly</span> / <span class='{annual_class}'>Annual (-20%)</span></p>", 
            unsafe_allow_html=True)

st.write("")

# --- Monitoring Frequency Selection ---
st.markdown("<div class='monitoring-container'>Monitoring Frequency</div>", unsafe_allow_html=True)
frequency_options = {"Daily": 30, "Twice Weekly": 8, "Weekly": 4, "Bi-Weekly": 2, "Monthly": 1}
selected_frequency = st.selectbox("", list(frequency_options.keys()), index=2)

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
