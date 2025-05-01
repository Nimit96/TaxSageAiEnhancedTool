"""
Reports and Visualizations Module
Contains functions for generating tax reports and visualizations
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
from datetime import datetime
import streamlit as st

class TaxReports:
    @staticmethod
    def generate_income_summary(income_data: Dict[str, Any]) -> None:
        """Generate income summary visualization"""
        # Create income breakdown
        income_breakdown = {
            'Salary': income_data['salary_amount'],
            'Other Income': income_data.get('other_income', 0)
        }
        
        # Create pie chart
        fig = px.pie(
            values=list(income_breakdown.values()),
            names=list(income_breakdown.keys()),
            title='Income Breakdown',
            hole=0.3
        )
        st.plotly_chart(fig)

    @staticmethod
    def generate_deduction_summary(deductions: List[Dict[str, Any]]) -> None:
        """Generate deduction summary visualization"""
        if not deductions:
            st.warning('No deductions found')
            return
            
        # Create DataFrame
        df = pd.DataFrame(deductions)
        
        # Create bar chart
        fig = px.bar(
            df,
            x='section',
            y='amount',
            title='Deductions by Section',
            labels={'section': 'Section', 'amount': 'Amount (₹)'}
        )
        st.plotly_chart(fig)

    @staticmethod
    def generate_capital_gains_summary(gains: List[Dict[str, Any]]) -> None:
        """Generate capital gains summary visualization"""
        if not gains:
            st.warning('No capital gains found')
            return
            
        # Create DataFrame
        df = pd.DataFrame(gains)
        
        # Calculate holding period
        df['holding_period'] = (pd.to_datetime(df['sale_date']) - 
                              pd.to_datetime(df['purchase_date'])).dt.days
        
        # Create scatter plot
        fig = px.scatter(
            df,
            x='holding_period',
            y='sale_price',
            color='asset_type',
            size='purchase_price',
            title='Capital Gains Analysis',
            labels={
                'holding_period': 'Holding Period (Days)',
                'sale_price': 'Sale Price (₹)',
                'asset_type': 'Asset Type'
            }
        )
        st.plotly_chart(fig)

    @staticmethod
    def generate_crypto_summary(transactions: List[Dict[str, Any]]) -> None:
        """Generate crypto transactions summary visualization"""
        if not transactions:
            st.warning('No crypto transactions found')
            return
            
        # Create DataFrame
        df = pd.DataFrame(transactions)
        
        # Create line chart
        fig = px.line(
            df,
            x='date',
            y='amount',
            color='transaction_type',
            title='Crypto Transactions Timeline',
            labels={
                'date': 'Date',
                'amount': 'Amount (₹)',
                'transaction_type': 'Transaction Type'
            }
        )
        st.plotly_chart(fig)

    @staticmethod
    def generate_tax_liability_summary(
        income_data: Dict[str, Any],
        deductions: List[Dict[str, Any]],
        gains: List[Dict[str, Any]],
        crypto_transactions: List[Dict[str, Any]]
    ) -> None:
        """Generate comprehensive tax liability summary"""
        # Calculate total income
        total_income = income_data['salary_amount'] + income_data.get('other_income', 0)
        
        # Calculate total deductions
        total_deductions = sum(d['amount'] for d in deductions)
        
        # Calculate total capital gains
        total_gains = sum(g['sale_price'] - g['purchase_price'] for g in gains)
        
        # Calculate total crypto gains
        total_crypto = sum(t['amount'] for t in crypto_transactions 
                          if t['transaction_type'] == 'sell')
        
        # Create summary DataFrame
        summary = pd.DataFrame({
            'Category': ['Salary', 'Other Income', 'Deductions', 
                        'Capital Gains', 'Crypto Gains'],
            'Amount': [income_data['salary_amount'], 
                      income_data.get('other_income', 0),
                      -total_deductions,
                      total_gains,
                      total_crypto]
        })
        
        # Create waterfall chart
        fig = go.Figure(go.Waterfall(
            name="Tax Liability",
            orientation="v",
            measure=["relative", "relative", "total", "relative", "relative"],
            x=summary['Category'],
            y=summary['Amount'],
            textposition="outside",
            text=summary['Amount'].apply(lambda x: f'₹{x:,.2f}'),
            connector={"line":{"color":"rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Tax Liability Summary",
            showlegend=False
        )
        
        st.plotly_chart(fig)

    @staticmethod
    def generate_tax_savings_analysis(deductions: List[Dict[str, Any]]) -> None:
        """Generate tax savings analysis visualization"""
        if not deductions:
            st.warning('No deductions found')
            return
            
        # Create DataFrame
        df = pd.DataFrame(deductions)
        
        # Group by section
        section_summary = df.groupby('section')['amount'].sum().reset_index()
        
        # Create treemap
        fig = px.treemap(
            section_summary,
            path=['section'],
            values='amount',
            title='Tax Savings by Section',
            labels={'section': 'Section', 'amount': 'Amount (₹)'}
        )
        
        st.plotly_chart(fig)

    @staticmethod
    def generate_investment_timeline(
        deductions: List[Dict[str, Any]],
        gains: List[Dict[str, Any]],
        crypto_transactions: List[Dict[str, Any]]
    ) -> None:
        """Generate investment timeline visualization"""
        # Combine all investment data
        investments = []
        
        # Add deductions
        for d in deductions:
            investments.append({
                'date': d.get('created_at', datetime.now()),
                'amount': d['amount'],
                'type': f"Deduction - {d['section']}",
                'category': 'Deduction'
            })
        
        # Add capital gains
        for g in gains:
            investments.append({
                'date': g['purchase_date'],
                'amount': g['purchase_price'],
                'type': f"Investment - {g['asset_type']}",
                'category': 'Capital'
            })
        
        # Add crypto transactions
        for t in crypto_transactions:
            if t['transaction_type'] == 'buy':
                investments.append({
                    'date': t['date'],
                    'amount': t['amount'],
                    'type': 'Crypto Investment',
                    'category': 'Crypto'
                })
        
        if not investments:
            st.warning('No investment data found')
            return
            
        # Create DataFrame
        df = pd.DataFrame(investments)
        
        # Create timeline
        fig = px.scatter(
            df,
            x='date',
            y='amount',
            color='category',
            size='amount',
            hover_name='type',
            title='Investment Timeline',
            labels={
                'date': 'Date',
                'amount': 'Amount (₹)',
                'category': 'Category'
            }
        )
        
        st.plotly_chart(fig)

    @staticmethod
    def generate_tax_planning_recommendations(
        income_data: Dict[str, Any],
        deductions: List[Dict[str, Any]]
    ) -> None:
        """Generate tax planning recommendations"""
        # Calculate current tax liability
        total_income = income_data['salary_amount'] + income_data.get('other_income', 0)
        total_deductions = sum(d['amount'] for d in deductions)
        taxable_income = total_income - total_deductions
        
        # Get tax slabs
        from utils.constants import get_tax_slabs
        tax_slabs = get_tax_slabs()
        
        # Find current tax slab
        current_slab = None
        for lower, upper, rate in tax_slabs:
            if lower <= taxable_income < upper:
                current_slab = (lower, upper, rate)
                break
        
        if current_slab:
            # Calculate potential savings
            remaining_limit = current_slab[1] - taxable_income
            potential_savings = remaining_limit * current_slab[2]
            
            # Display recommendations
            st.subheader('Tax Planning Recommendations')
            st.write(f'Current Taxable Income: ₹{taxable_income:,.2f}')
            st.write(f'Current Tax Slab: {current_slab[2]*100}%')
            st.write(f'Remaining Limit in Current Slab: ₹{remaining_limit:,.2f}')
            st.write(f'Potential Tax Savings: ₹{potential_savings:,.2f}')
            
            # Suggest investment options
            st.write('\nSuggested Investment Options:')
            from utils.constants import TAX_SAVING_OPTIONS
            for section, options in TAX_SAVING_OPTIONS.items():
                st.write(f'\n**{section} Options:**')
                for option in options:
                    st.write(f'- {option}')
        else:
            st.warning('Unable to determine current tax slab') 