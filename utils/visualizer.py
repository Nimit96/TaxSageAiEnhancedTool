"""
Data Visualization Module
Contains functions for creating tax-related charts and visualizations
"""

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Union
import numpy as np
from datetime import datetime

class TaxVisualizer:
    def __init__(self):
        """Initialize visualization settings"""
        self.color_scheme = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'warning': '#ffd700',
            'danger': '#d62728',
            'info': '#17becf'
        }

    def plot_tax_slabs(self, taxable_income: float, tax_liability: Dict[str, float]) -> None:
        """Plot tax slabs and liability"""
        # Create data for tax slabs
        slabs = [
            (0, 300000, 0),
            (300001, 600000, 0.05),
            (600001, 900000, 0.10),
            (900001, 1200000, 0.15),
            (1200001, 1500000, 0.20),
            (1500001, float('inf'), 0.30)
        ]
        
        data = []
        for lower, upper, rate in slabs:
            if upper == float('inf'):
                upper = max(taxable_income, 2000000)  # Cap at 20L for visualization
            data.append({
                'Slab': f'₹{lower:,.0f} - ₹{upper:,.0f}',
                'Rate': f'{rate*100}%',
                'Amount': min(upper - lower, max(0, taxable_income - lower))
            })
        
        df = pd.DataFrame(data)
        
        # Create stacked bar chart
        chart = alt.Chart(df).mark_bar().encode(
            x='Slab',
            y='Amount',
            color='Rate',
            tooltip=['Slab', 'Rate', 'Amount']
        ).properties(
            title='Tax Slabs and Liability',
            width=600,
            height=400
        )
        
        st.altair_chart(chart, use_container_width=True)

    def plot_deduction_utilization(self, deductions: Dict[str, Dict[str, float]]) -> None:
        """Plot deduction utilization"""
        data = []
        for section, details in deductions.items():
            data.append({
                'Section': section,
                'Claimed': details['claimed'],
                'Remaining': details['remaining']
            })
        
        df = pd.DataFrame(data)
        
        # Create stacked bar chart
        chart = alt.Chart(df).mark_bar().encode(
            x='Section',
            y='Claimed',
            color=alt.value(self.color_scheme['success'])
        ) + alt.Chart(df).mark_bar().encode(
            x='Section',
            y='Remaining',
            color=alt.value(self.color_scheme['warning'])
        )
        
        st.altair_chart(chart, use_container_width=True)

    def plot_capital_gains_timeline(self, transactions: List[Dict[str, Any]]) -> None:
        """Plot capital gains timeline"""
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # Create line chart
        fig = px.line(
            df,
            x='date',
            y='capital_gain',
            color='type',
            title='Capital Gains Timeline',
            labels={'capital_gain': 'Capital Gain (₹)', 'date': 'Date', 'type': 'Transaction Type'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def plot_tax_savings_analysis(self, savings_data: Dict[str, float]) -> None:
        """Plot tax savings analysis"""
        df = pd.DataFrame({
            'Category': list(savings_data.keys()),
            'Amount': list(savings_data.values())
        })
        
        # Create pie chart
        fig = px.pie(
            df,
            values='Amount',
            names='Category',
            title='Tax Savings Analysis',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def plot_investment_timeline(self, investments: List[Dict[str, Any]]) -> None:
        """Plot investment timeline"""
        df = pd.DataFrame(investments)
        df['date'] = pd.to_datetime(df['date'])
        
        # Create area chart
        fig = px.area(
            df,
            x='date',
            y='amount',
            color='type',
            title='Investment Timeline',
            labels={'amount': 'Amount (₹)', 'date': 'Date', 'type': 'Investment Type'}
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def plot_tax_comparison(self, current_tax: float, optimized_tax: float) -> None:
        """Plot tax comparison"""
        data = {
            'Scenario': ['Current Tax', 'Optimized Tax'],
            'Amount': [current_tax, optimized_tax]
        }
        df = pd.DataFrame(data)
        
        # Create bar chart
        chart = alt.Chart(df).mark_bar().encode(
            x='Scenario',
            y='Amount',
            color=alt.condition(
                alt.datum.Scenario == 'Current Tax',
                alt.value(self.color_scheme['danger']),
                alt.value(self.color_scheme['success'])
            )
        ).properties(
            title='Tax Optimization Comparison',
            width=400,
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)

    def plot_income_distribution(self, income_data: Dict[str, float]) -> None:
        """Plot income distribution"""
        df = pd.DataFrame({
            'Category': list(income_data.keys()),
            'Amount': list(income_data.values())
        })
        
        # Create treemap
        fig = px.treemap(
            df,
            path=['Category'],
            values='Amount',
            title='Income Distribution',
            color='Amount',
            color_continuous_scale='RdYlBu'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def plot_tax_planning_recommendations(self, recommendations: List[Dict[str, Any]]) -> None:
        """Plot tax planning recommendations"""
        df = pd.DataFrame(recommendations)
        
        # Create horizontal bar chart
        chart = alt.Chart(df).mark_bar().encode(
            x='potential_savings',
            y='strategy',
            color=alt.value(self.color_scheme['info']),
            tooltip=['strategy', 'potential_savings', 'risk_level']
        ).properties(
            title='Tax Planning Recommendations',
            width=600,
            height=400
        )
        
        st.altair_chart(chart, use_container_width=True)

    def plot_crypto_tax_analysis(self, crypto_data: List[Dict[str, Any]]) -> None:
        """Plot crypto tax analysis"""
        df = pd.DataFrame(crypto_data)
        
        # Create candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=df['date'],
            open=df['open_price'],
            high=df['high_price'],
            low=df['low_price'],
            close=df['close_price']
        )])
        
        fig.update_layout(
            title='Crypto Price Analysis',
            xaxis_title='Date',
            yaxis_title='Price (₹)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def plot_tax_forecast(self, historical_data: List[Dict[str, Any]], forecast_data: List[Dict[str, Any]]) -> None:
        """Plot tax forecast"""
        historical_df = pd.DataFrame(historical_data)
        forecast_df = pd.DataFrame(forecast_data)
        
        # Create line chart with confidence interval
        fig = go.Figure()
        
        # Add historical data
        fig.add_trace(go.Scatter(
            x=historical_df['year'],
            y=historical_df['tax'],
            name='Historical',
            line=dict(color=self.color_scheme['primary'])
        ))
        
        # Add forecast data
        fig.add_trace(go.Scatter(
            x=forecast_df['year'],
            y=forecast_df['tax'],
            name='Forecast',
            line=dict(color=self.color_scheme['secondary'])
        ))
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_df['year'].tolist() + forecast_df['year'].tolist()[::-1],
            y=forecast_df['upper_bound'].tolist() + forecast_df['lower_bound'].tolist()[::-1],
            fill='toself',
            fillcolor='rgba(255,127,14,0.2)',
            line=dict(color='rgba(255,127,14,0)'),
            name='Confidence Interval'
        ))
        
        fig.update_layout(
            title='Tax Liability Forecast',
            xaxis_title='Year',
            yaxis_title='Tax Liability (₹)'
        )
        
        st.plotly_chart(fig, use_container_width=True) 