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
