import streamlit as st
import pandas as pd

# --- ✅ Fix: Set Page Config as the first command ---
st.set_page_config(page_title="Vyberte si svůj plán", layout="wide")

# --- Custom Styling for a Tech-Like UI ---
st.markdown("""
    <style>
        /* Center the plan selection */
        .plan-selection {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        /* Subtext */
        .plan-subtext {
            text-align: center;
            font-size: 20px;
            color: grey;
            margin-bottom: 20px;
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
            {days_left} dní zbývá ve zkušební verzi
        </span>
        <a href='https://www.deepscout.ai/pricing' target='_blank' 
           style='background-color: #0073e6; color: white; padding: 8px 16px; 
                  font-size: 14px; font-weight: bold; text-decoration: none; 
                  border-radius: 5px; display: inline-block;'>
            Upgradovat nyní
        </a>
    </div>
""", unsafe_allow_html=True)

st.write("")

# --- Plan Selection Heading & Subtext ---
st.markdown("<h3 style='text-align: center;'>Vyberte si svůj plán</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Naše ceny jsou založeny na skutečném využití DeepScout. Vyberte si požadovanou frekvenci monitorování a začněte ještě dnes!</p>", unsafe_allow_html=True)
st.write("")

# --- Monitoring Frequency Selection (No Space Between Label & Select Box) ---
st.markdown("<p style='font-size:18px; font-weight:bold; margin-bottom: 0;'>Frekvence monitorování</p>", unsafe_allow_html=True)
frequency_options = {"Denně": 30, "Dvakrát týdně": 8, "Týdně": 4, "Dvakrát měsíčně": 2, "Měsíčně": 1}
selected_frequency = st.selectbox("", list(frequency_options.keys()), index=2, key="monitoring_freq", label_visibility="collapsed")

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
df["Celková cena"] = df["fixed_fee"] + df["data_updates"] * frequency_multiplier

# Format Prices
df["Celková cena"] = df["Celková cena"].astype(int).astype(str) + " Kč"
df["fixed_fee"] = df["fixed_fee"].astype(str) + " Kč"

# Add currency only to the first number in "data_updates"
df["data_updates"] = df["data_updates"].astype(str) + f" Kč × {frequency_multiplier}"

# **Fix: Correct Totals Row**
total_fixed_fee = sum([w["fixed_fee"] for w in websites])  # Sum of all fixed fees
total_data_updates_raw = sum([w["data_updates"] for w in websites])  # Sum of raw data updates
total_price = sum([int(price.split()[0]) for price in df["Celková cena"]])  # Sum of total prices

# **Ensure "TOTAL" row has correct values**
df.loc[len(df)] = [
    "CELKEM",  
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
            Upgradovat nyní
        </a>
    </div>
""", unsafe_allow_html=True)

# --- Professional Disclaimer ---
st.markdown("""
    <p class='disclaimer' style='font-size: 13px; text-align: center; color: grey;'>
        Ceny jsou odhadovány na základě velikosti webů z našeho prvního monitorování. 
        Jak se weby v průběhu času mění, mohou se mírně změnit i tyto částky.
        Vždy zajistíme, aby vaše ceny byly transparentní a spravedlivé. 
        Podrobné informace o cenách naleznete na 
        <a href='https://www.deepscout.ai/pricing' target='_blank'>našem webu</a>.
    </p>
""", unsafe_allow_html=True)

st.markdown("""
    <p class='disclaimer' style='font-size: 13px; text-align: center; color: grey;'>
        * Některé weby mohou mít vyšší náklady na monitorování kvůli své struktuře 
        nebo opatřením proti scrapingu.
    </p>
""", unsafe_allow_html=True)
