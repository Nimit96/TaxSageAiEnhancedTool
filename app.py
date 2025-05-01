"""
TaxSageAiEnhanced - Main Application
Streamlit-based tax planning and optimization tool for Indian taxpayers
"""

import streamlit as st
from typing import Dict, List
import pandas as pd
import altair as alt
from datetime import datetime

# Import modules
from modules.salary_architect import SalaryArchitect
from modules.deduction_scanner import DeductionScanner
from modules.capital_gain_suite import CapitalGainSuite
from modules.crypto_lens import CryptoLens
from modules.master_playbook import MasterPlaybook
from modules.ethical_shield import EthicalShield
from modules.auto_update import AutoUpdate

# Page configuration
st.set_page_config(
    page_title="TaxSageAiEnhanced",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("TaxSageAiEnhanced")
st.sidebar.markdown("---")

# Navigation options
PAGES: Dict[str, str] = {
    "Salary Architect": "Optimize your salary structure",
    "Deduction Scanner": "Track and maximize deductions",
    "Capital Gain Suite": "Manage capital gains",
    "Crypto Lens": "Calculate crypto taxes",
    "Master Playbook": "Advanced tax strategies",
    "Ethical Shield": "Stay compliant",
    "Auto Update": "Check for updates"
}

# Add navigation to sidebar
selected_page = st.sidebar.radio(
    "Navigate to:",
    list(PAGES.keys()),
    format_func=lambda x: f"{x} - {PAGES[x]}"
)

# Main content area
st.title("TaxSageAiEnhanced")
st.markdown("""
    Welcome to TaxSageAiEnhanced - Your AI-powered tax planning companion for FY 2024-25.
    Select a module from the sidebar to get started.
""")

# Initialize modules
salary_architect = SalaryArchitect()
deduction_scanner = DeductionScanner()
capital_gain_suite = CapitalGainSuite()
crypto_lens = CryptoLens()
master_playbook = MasterPlaybook()
ethical_shield = EthicalShield()
auto_update = AutoUpdate()

# Page routing
if selected_page == "Salary Architect":
    salary_architect.render()
elif selected_page == "Deduction Scanner":
    deduction_scanner.render()
elif selected_page == "Capital Gain Suite":
    capital_gain_suite.render()
elif selected_page == "Crypto Lens":
    crypto_lens.render()
elif selected_page == "Master Playbook":
    master_playbook.render()
elif selected_page == "Ethical Shield":
    ethical_shield.render()
elif selected_page == "Auto Update":
    auto_update.render()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>TaxSageAiEnhanced v1.0.0 | MIT License</p>
        <p>Disclaimer: This tool is for informational purposes only. Please consult a tax professional for specific advice.</p>
    </div>
""", unsafe_allow_html=True) 