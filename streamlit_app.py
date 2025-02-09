import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="SAAS Pricing", layout="wide")

# --- Custom Styling for a Tech-Like UI ---
st.markdown("""
    <style>
        /* General container styling */
        .block-container {
            max-width: 800px;
            margin: auto;
        }
        /* Plan selection styling */
        .plan-selection {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }
        .selected-plan {
            display: inline-block;
            padding: 6px 15px;
            font-size: 18px;
            font-weight: bold;
            color: white;
            background-color: black;
            border-radius: 8px;
            margin-right: 10px;
        }
        .unselected-plan {
            display: inline-block;
            font-size: 18px;
            font-weight: bold;
            color: grey;
            cursor: pointer;
        }
        /* Monitoring Frequency Dropdown */
        .monitoring-container {
            background-color: #F5F5F5;
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
        }
        th {
            background-color: #F5F5F5;
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

col1, col2 = st.columns([0.2, 0.2])
with col1:
    if st.button("Monthly", key="monthly_plan"):
        st.session_state["plan"] = "monthly"
with col2:
    if st.button("Annual (-20%)", key="annual_plan"):
        st.session_state["plan"] = "annual"

# Default plan selection if not already set
if "plan" not in st.session_state:
    st.session_state["plan"] = "monthly"

# Highlight selected plan
if st.session_state["plan"] == "monthly":
    st.markdown("<span class='selected-plan'>Monthly</span> / <span class='unselected-plan'>Annual (-20%)</span>", unsafe_allow_html=True)
else:
    st.markdown("<span class='unselected-plan'>Monthly</span> / <span class='selected-plan'>Annual (-20%)</span>", unsafe_allow_html=True)

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
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Select Your Plan", layout="wide")

st.title("Select Your Plan")

# Billing cycle selection
col1, col2, col3 = st.columns([1,1,1])
with col2:
    billing_cycle = st.radio("", ("Monthly", "Annual (-20%)"), horizontal=True)

# Monitoring frequency selection
frequency = st.selectbox(
    "Monitoring frequency",
    ("Daily", "Twice Weekly", "Weekly", "Bi-Weekly", "Monthly")
)

# Define frequency multipliers
frequency_multiplier = {
    "Daily": 30,
    "Twice Weekly": 8,
    "Weekly": 4,
    "Bi-Weekly": 2,
    "Monthly": 1
}

# Define websites data
websites = [
    {"name": "bonami.cz", "fixed_fee": 150, "data_updates": 608},
    {"name": "helveti.cz", "fixed_fee": 150, "data_updates": 120},
    {"name": "biano.cz", "fixed_fee": 150, "data_updates": 5}
]

# Calculate prices
def calculate_price(fixed_fee, data_updates, frequency, billing_cycle):
    monthly_price = fixed_fee + data_updates * frequency_multiplier[frequency]
    if billing_cycle == "Annual (-20%)":
        return monthly_price * 0.8
    return monthly_price

# Create DataFrame
df = pd.DataFrame(websites)
df["Monthly Price"] = df.apply(lambda row: calculate_price(
    row["fixed_fee"], 
    row["data_updates"], 
    frequency, 
    billing_cycle
), axis=1)

# Calculate totals
totals = df.sum()

# Add totals to DataFrame
df.loc["TOTAL"] = totals

# Format DataFrame
df["Monthly Price"] = df["Monthly Price"].round(2)
df["Data Updates"] = df["data_updates"].astype(str) + " × " + str(frequency_multiplier[frequency])
df = df.rename(columns={"name": "Website", "fixed_fee": "Fixed Fee"})
df = df[["Website", "Monthly Price", "Fixed Fee", "Data Updates"]]

# Display table
st.table(df.style.format({
    "Monthly Price": "{:.2f} Kč",
    "Fixed Fee": "{:.0f} Kč"
}).hide_index())

# Add explanation of calculation
st.markdown("**Monthly Price** = **Fixed Fee** + **Data Updates**")
