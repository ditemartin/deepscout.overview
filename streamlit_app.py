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
    if st.butt
