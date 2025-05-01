"""
Crypto Lens Module
Calculates crypto taxes and TDS based on FIFO method
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np

from constants import (
    CRYPTO_TAX_RATE,
    CRYPTO_TDS_RATE
)

class CryptoLens:
    def __init__(self):
        self.tax_rate = CRYPTO_TAX_RATE
        self.tds_rate = CRYPTO_TDS_RATE
        self.fifo_ledger = []

    def process_transaction(
        self,
        date: datetime,
        type: str,
        amount: float,
        price: float,
        exchange: str
    ) -> Dict[str, float]:
        """Process a single crypto transaction"""
        if type.lower() == 'buy':
            self.fifo_ledger.append({
                'date': date,
                'amount': amount,
                'price': price,
                'exchange': exchange
            })
            return {'tax': 0.0, 'tds': 0.0}
        
        elif type.lower() == 'sell':
            remaining_amount = amount
            total_cost = 0.0
            total_proceeds = amount * price
            
            # Process using FIFO method
            while remaining_amount > 0 and self.fifo_ledger:
                oldest_lot = self.fifo_ledger[0]
                
                if oldest_lot['amount'] <= remaining_amount:
                    # Use entire lot
                    total_cost += oldest_lot['amount'] * oldest_lot['price']
                    remaining_amount -= oldest_lot['amount']
                    self.fifo_ledger.pop(0)
                else:
                    # Use partial lot
                    total_cost += remaining_amount * oldest_lot['price']
                    oldest_lot['amount'] -= remaining_amount
                    remaining_amount = 0
            
            # Calculate capital gain
            capital_gain = total_proceeds - total_cost
            
            # Calculate tax and TDS
            tax = capital_gain * self.tax_rate
            tds = total_proceeds * self.tds_rate
            
            return {
                'capital_gain': capital_gain,
                'tax': tax,
                'tds': tds,
                'total_proceeds': total_proceeds,
                'total_cost': total_cost
            }
        
        return {'tax': 0.0, 'tds': 0.0}

    def process_csv_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process crypto transaction data from CSV"""
        results = []
        
        for _, row in df.iterrows():
            result = self.process_transaction(
                pd.to_datetime(row['date']),
                row['type'],
                row['amount'],
                row['price'],
                row.get('exchange', 'Unknown')
            )
            
            results.append({
                'date': row['date'],
                'type': row['type'],
                'amount': row['amount'],
                'price': row['price'],
                'exchange': row.get('exchange', 'Unknown'),
                **result
            })
        
        return pd.DataFrame(results)

    def get_fifo_summary(self) -> pd.DataFrame:
        """Get summary of remaining FIFO lots"""
        if not self.fifo_ledger:
            return pd.DataFrame()
        
        return pd.DataFrame(self.fifo_ledger)

    def render(self):
        """Render the Crypto Lens interface"""
        st.title("Crypto Lens")
        st.markdown("""
            Calculate your crypto taxes and TDS using FIFO method.
            Upload your transaction history or enter manually.
        """)

        # Input method selection
        input_method = st.radio(
            "Choose Input Method",
            ["Upload CSV", "Manual Entry"]
        )

        if input_method == "Upload CSV":
            # File upload
            uploaded_file = st.file_uploader(
                "Upload Transaction History (CSV)",
                type=['csv'],
                help="CSV should have columns: date, type, amount, price, exchange"
            )
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    required_columns = ['date', 'type', 'amount', 'price']
                    
                    if all(col in df.columns for col in required_columns):
                        # Process transactions
                        results_df = self.process_csv_data(df)
                        
                        # Display results
                        st.subheader("Transaction Analysis")
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Display FIFO summary
                        st.subheader("FIFO Ledger")
                        fifo_df = self.get_fifo_summary()
                        if not fifo_df.empty:
                            st.dataframe(fifo_df, use_container_width=True)
                        else:
                            st.info("No remaining lots in FIFO ledger")
                        
                        # Display tax summary
                        st.subheader("Tax Summary")
                        tax_summary = results_df[['tax', 'tds']].sum()
                        st.metric(
                            "Total Tax Liability",
                            f"₹{tax_summary['tax']:,.2f}",
                            f"TDS: ₹{tax_summary['tds']:,.2f}"
                        )
                        
                        # Display charts
                        st.subheader("Visualization")
                        
                        # Capital gains over time
                        chart1 = alt.Chart(results_df).mark_line().encode(
                            x='date:T',
                            y='capital_gain:Q',
                            tooltip=['date', 'capital_gain', 'tax']
                        ).properties(
                            title="Capital Gains Over Time"
                        )
                        
                        st.altair_chart(chart1, use_container_width=True)
                        
                        # Tax liability by transaction
                        chart2 = alt.Chart(results_df).mark_bar().encode(
                            x='date:T',
                            y='tax:Q',
                            color='type:N',
                            tooltip=['date', 'tax', 'tds']
                        ).properties(
                            title="Tax Liability by Transaction"
                        )
                        
                        st.altair_chart(chart2, use_container_width=True)
                        
                    else:
                        st.error("CSV file must contain all required columns: date, type, amount, price")
                
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

        else:  # Manual Entry
            # Initialize session state for transactions
            if 'transactions' not in st.session_state:
                st.session_state.transactions = []

            # Input form
            st.subheader("Enter Transaction Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Date")
                type = st.selectbox("Type", ["Buy", "Sell"])
                amount = st.number_input("Amount", min_value=0.0)
            
            with col2:
                price = st.number_input("Price (₹)", min_value=0.0)
                exchange = st.text_input("Exchange")

            if st.button("Add Transaction"):
                if date and type and amount and price:
                    # Process transaction
                    result = self.process_transaction(
                        date,
                        type,
                        amount,
                        price,
                        exchange
                    )
                    
                    # Add to session state
                    st.session_state.transactions.append({
                        'date': date,
                        'type': type,
                        'amount': amount,
                        'price': price,
                        'exchange': exchange,
                        **result
                    })
                    
                    st.success("Transaction added successfully!")
                else:
                    st.error("Please fill in all required fields")

            # Display transactions
            if st.session_state.transactions:
                st.subheader("Your Transactions")
                transactions_df = pd.DataFrame(st.session_state.transactions)
                st.dataframe(transactions_df, use_container_width=True)
                
                # Display FIFO summary
                st.subheader("FIFO Ledger")
                fifo_df = self.get_fifo_summary()
                if not fifo_df.empty:
                    st.dataframe(fifo_df, use_container_width=True)
                else:
                    st.info("No remaining lots in FIFO ledger")
                
                # Display tax summary
                st.subheader("Tax Summary")
                tax_summary = transactions_df[['tax', 'tds']].sum()
                st.metric(
                    "Total Tax Liability",
                    f"₹{tax_summary['tax']:,.2f}",
                    f"TDS: ₹{tax_summary['tds']:,.2f}"
                )

        # Display tax rates and rules
        st.sidebar.subheader("Tax Rates & Rules")
        st.sidebar.markdown(f"""
            - Crypto Tax Rate: {self.tax_rate * 100}%
            - TDS Rate: {self.tds_rate * 100}%
            - FIFO Method: First In, First Out
            - No Loss Set-off: Crypto losses cannot be set off against other income
        """) 