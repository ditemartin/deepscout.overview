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
        /* Divider */
        .divider {
            font-size: 22px;
            font-weight: bold;
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

# --- Header: Free Trial Countdown + Upgrade Button ---
days_left = 7  # Set dynamically if needed

st.markdown(f"""
    <div style="display: flex; justify-content: space-between; 
                align-items: center; background-color: #F5F5F5; 
                padding: 10px 20px; border-radius: 5px; margin-bottom: 20px;">
        <span style="font-size: 16px; font-weight: bold; color: black;">
            {days_left} days left in free trial
        </span>
        <a href='https://www.deepscout.ai/pricing' target='_blank' 
           style='background-color: #0073e6; color: white; padding: 8px 16px; 
                  font-size: 14px; font-weight: bold; text-decoration: none; 
                  border-radius: 5px; display: inline-block;'>
            Upgrade Now
        </a>
    </div>
""", unsafe_allow_html=True)

# --- Monitoring Frequency Selection ---
st.markdown("<p style='font-size:18px; font-weight:bold;'>Monitoring Frequency</p>", unsafe_allow_html=True)
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

# Apply calculations
df["Total Price"] = df["fixed_fee"] + df["data_updates"] * frequency_multiplier

# Format Prices
df["Total Price"] = df["Total Price"].astype(int).astype(str) + " Kč"
df["fixed_fee"] = df["fixed_fee"].astype(str) + " Kč"

# Add currency only to the first number in "data_updates"
df["data_updates"] = df["data_updates"].astype(str) + f" Kč × {frequency_multiplier}"

# **Fix: Correct Totals Row**
total_fixed_fee = sum([w["fixed_fee"] for w in websites])  # Sum of all fixed fees
total_data_updates_raw = sum([w["data_updates"] for w in websites])  # Sum of raw data updates
total_price = sum([int(price.split()[0]) for price in df["Total Price"]])  # Sum of total prices

# **Ensure "TOTAL" row has correct values**
df.loc[len(df)] = [
    "TOTAL",  
    f"{total_fixed_fee} Kč",
    f"{total_data_updates_raw} Kč × {frequency_multiplier}",
    f"{total_price} Kč"
]

# --- Display Table ---
st.write("")
st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)
st.write("")

# --- Call to Action: Upgrade Now Button ---
st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <a href='https://www.deepscout.ai/pricing' target='_blank' 
           style='background-color: #0073e6; color: white; padding: 12px 24px; 
                  font-size: 16px; font-weight: bold; text-decoration: none; 
                  border-radius: 5px; display: inline-block;'>
            Upgrade Now
        </a>
    </div>
""", unsafe_allow_html=True)

# --- Professional Disclaimer ---
st.markdown("""
    <p class='disclaimer' style='font-size: 13px; text-align: center; color: grey;'>
        Price estimates are based on website sizes from our initial monitoring. 
        As the websites change over time, these numbers will also change slightly.
        We’ll always ensure your pricing remains transparent and fair. 
        You can find detailed information about our pricing on 
        <a href='https://www.deepscout.ai/pricing' target='_blank'>our website</a>.
    </p>
""", unsafe_allow_html=True)

st.markdown("""
    <p class='disclaimer' style='font-size: 13px; text-align: center; color: grey;'>
        * Some websites may have higher monitoring costs due to their structure 
        or anti-scraping measures.
    </p>
""", unsafe_allow_html=True)
