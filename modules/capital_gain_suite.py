"""
Capital Gain Suite Module
Manages capital gains from equity, mutual funds, and real estate
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import numpy as np

from constants import (
    LTCG_TAX_RATE,
    STCG_TAX_RATE,
    LTCG_EXEMPTION_LIMIT
)

class CapitalGainSuite:
    def __init__(self):
        self.ltcg_tax_rate = LTCG_TAX_RATE
        self.stcg_tax_rate = STCG_TAX_RATE
        self.ltcg_exemption_limit = LTCG_EXEMPTION_LIMIT
        self.long_term_threshold = timedelta(days=365)

    def calculate_holding_period(self, purchase_date: datetime, sale_date: datetime) -> timedelta:
        """Calculate holding period for an asset"""
        return sale_date - purchase_date

    def is_long_term(self, holding_period: timedelta) -> bool:
        """Check if holding period qualifies as long-term"""
        return holding_period >= self.long_term_threshold

    def calculate_capital_gains(
        self,
        purchase_price: float,
        sale_price: float,
        purchase_date: datetime,
        sale_date: datetime,
        expenses: float = 0.0
    ) -> Dict[str, float]:
        """Calculate capital gains and tax liability"""
        holding_period = self.calculate_holding_period(purchase_date, sale_date)
        is_ltcg = self.is_long_term(holding_period)
        
        # Calculate capital gain
        capital_gain = sale_price - purchase_price - expenses
        
        # Calculate tax
        if is_ltcg:
            # Apply exemption limit
            taxable_gain = max(0, capital_gain - self.ltcg_exemption_limit)
            tax = taxable_gain * self.ltcg_tax_rate
            tax_type = "LTCG"
        else:
            tax = capital_gain * self.stcg_tax_rate
            tax_type = "STCG"
        
        return {
            'capital_gain': capital_gain,
            'tax': tax,
            'tax_type': tax_type,
            'holding_period_days': holding_period.days,
            'is_long_term': is_ltcg
        }

    def process_trade_data(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Process trade data and calculate gains/losses"""
        results = []
        
        for _, trade in trades_df.iterrows():
            result = self.calculate_capital_gains(
                trade['purchase_price'],
                trade['sale_price'],
                pd.to_datetime(trade['purchase_date']),
                pd.to_datetime(trade['sale_date']),
                trade.get('expenses', 0.0)
            )
            
            results.append({
                'symbol': trade['symbol'],
                'purchase_date': trade['purchase_date'],
                'sale_date': trade['sale_date'],
                'purchase_price': trade['purchase_price'],
                'sale_price': trade['sale_price'],
                'capital_gain': result['capital_gain'],
                'tax': result['tax'],
                'tax_type': result['tax_type'],
                'holding_period_days': result['holding_period_days']
            })
        
        return pd.DataFrame(results)

    def optimize_loss_harvesting(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Optimize loss harvesting strategy"""
        # Group by tax type and calculate net gains/losses
        grouped = trades_df.groupby('tax_type').agg({
            'capital_gain': 'sum',
            'tax': 'sum'
        }).reset_index()
        
        # Calculate net position
        net_position = grouped['capital_gain'].sum()
        net_tax = grouped['tax'].sum()
        
        # Add summary row
        summary = pd.DataFrame([{
            'tax_type': 'Net Position',
            'capital_gain': net_position,
            'tax': net_tax
        }])
        
        return pd.concat([grouped, summary], ignore_index=True)

    def render(self):
        """Render the Capital Gain Suite interface"""
        st.title("Capital Gain Suite")
        st.markdown("""
            Calculate and optimize your capital gains from equity, mutual funds, and real estate.
            Upload your trade data or enter manually to get detailed analysis.
        """)

        # Input method selection
        input_method = st.radio(
            "Choose Input Method",
            ["Upload CSV", "Manual Entry"]
        )

        if input_method == "Upload CSV":
            # File upload
            uploaded_file = st.file_uploader(
                "Upload Trade Data (CSV)",
                type=['csv'],
                help="CSV should have columns: symbol, purchase_date, sale_date, purchase_price, sale_price, expenses"
            )
            
            if uploaded_file is not None:
                try:
                    trades_df = pd.read_csv(uploaded_file)
                    required_columns = ['symbol', 'purchase_date', 'sale_date', 'purchase_price', 'sale_price']
                    
                    if all(col in trades_df.columns for col in required_columns):
                        # Process trades
                        results_df = self.process_trade_data(trades_df)
                        
                        # Display results
                        st.subheader("Trade Analysis")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Display summary
                        st.subheader("Tax Summary")
                        summary_df = self.optimize_loss_harvesting(results_df)
                        st.dataframe(summary_df, use_container_width=True)
                        
                        # Display charts
                        st.subheader("Visualization")
                        
                        # Capital gains by holding period
                        chart1 = alt.Chart(results_df).mark_bar().encode(
                            x='holding_period_days',
                            y='capital_gain',
                            color='tax_type',
                            tooltip=['symbol', 'capital_gain', 'tax']
                        ).properties(
                            title="Capital Gains by Holding Period"
                        )
                        
                        st.altair_chart(chart1, use_container_width=True)
                        
                        # Tax liability by trade
                        chart2 = alt.Chart(results_df).mark_bar().encode(
                            x='symbol',
                            y='tax',
                            color='tax_type',
                            tooltip=['symbol', 'capital_gain', 'tax']
                        ).properties(
                            title="Tax Liability by Trade"
                        )
                        
                        st.altair_chart(chart2, use_container_width=True)
                        
                    else:
                        st.error("CSV file must contain all required columns: symbol, purchase_date, sale_date, purchase_price, sale_price")
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

        else:  # Manual Entry
            # Initialize session state for trades
            if 'trades' not in st.session_state:
                st.session_state.trades = []

            # Input form
            st.subheader("Enter Trade Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                symbol = st.text_input("Symbol")
                purchase_date = st.date_input("Purchase Date")
                purchase_price = st.number_input("Purchase Price (₹)", min_value=0.0)
            
            with col2:
                sale_date = st.date_input("Sale Date")
                sale_price = st.number_input("Sale Price (₹)", min_value=0.0)
                expenses = st.number_input("Expenses (₹)", min_value=0.0, value=0.0)

            if st.button("Add Trade"):
                if symbol and purchase_date and sale_date:
                    # Calculate gains
                    result = self.calculate_capital_gains(
                        purchase_price,
                        sale_price,
                        purchase_date,
                        sale_date,
                        expenses
                    )
                    
                    # Add to session state
                    st.session_state.trades.append({
                        'symbol': symbol,
                        'purchase_date': purchase_date,
                        'sale_date': sale_date,
                        'purchase_price': purchase_price,
                        'sale_price': sale_price,
                        'expenses': expenses,
                        **result
                    })
                    
                    st.success("Trade added successfully!")
                else:
                    st.error("Please fill in all required fields")

            # Display trades
            if st.session_state.trades:
                st.subheader("Your Trades")
                trades_df = pd.DataFrame(st.session_state.trades)
                st.dataframe(trades_df, use_container_width=True)
                
                # Display summary
                st.subheader("Tax Summary")
                summary_df = self.optimize_loss_harvesting(trades_df)
                st.dataframe(summary_df, use_container_width=True)

        # Display tax rates and rules
        st.sidebar.subheader("Tax Rates & Rules")
        st.sidebar.markdown(f"""
            - LTCG Tax Rate: {self.ltcg_tax_rate * 100}%
            - STCG Tax Rate: {self.stcg_tax_rate * 100}%
            - LTCG Exemption Limit: ₹{self.ltcg_exemption_limit:,.0f}
            - Long-term Holding Period: {self.long_term_threshold.days} days
        """) 