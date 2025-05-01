"""
Deduction Scanner Module
Tracks and maximizes tax deductions under various sections
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, List, Tuple
from datetime import datetime

from constants import (
    MAX_80C_DEDUCTION,
    MAX_80D_DEDUCTION,
    MAX_HOME_LOAN_INTEREST,
    MAX_EDUCATION_LOAN_INTEREST,
    MAX_80TTA_DEDUCTION,
    MAX_NPS_ADDITIONAL_DEDUCTION
)

class DeductionScanner:
    def __init__(self):
        self.deduction_limits = {
            '80C': MAX_80C_DEDUCTION,
            '80D': sum(MAX_80D_DEDUCTION.values()),
            '24(b)': MAX_HOME_LOAN_INTEREST,
            '80E': MAX_EDUCATION_LOAN_INTEREST,
            '80TTA': MAX_80TTA_DEDUCTION,
            '80CCD(1B)': MAX_NPS_ADDITIONAL_DEDUCTION
        }

        self.deduction_descriptions = {
            '80C': {
                'description': 'Investments and Expenses',
                'items': [
                    'Life Insurance Premium',
                    'ELSS Mutual Funds',
                    'PPF',
                    'NSC',
                    '5-year FD',
                    'Tuition Fees',
                    'Home Loan Principal',
                    'Sukanya Samriddhi'
                ]
            },
            '80D': {
                'description': 'Health Insurance Premium',
                'items': [
                    'Self',
                    'Spouse',
                    'Children',
                    'Parents',
                    'Senior Citizen Parents',
                    'Preventive Health Checkup'
                ]
            },
            '24(b)': {
                'description': 'Home Loan Interest',
                'items': [
                    'Self-occupied Property',
                    'Let-out Property'
                ]
            },
            '80E': {
                'description': 'Education Loan Interest',
                'items': [
                    'Higher Education',
                    'Vocational Course'
                ]
            },
            '80TTA': {
                'description': 'Savings Account Interest',
                'items': [
                    'Bank Interest',
                    'Post Office Interest'
                ]
            },
            '80CCD(1B)': {
                'description': 'NPS Additional Contribution',
                'items': [
                    'Tier 1 Account',
                    'Tier 2 Account'
                ]
            }
        }

    def calculate_deductions(self, user_inputs: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """Calculate deductions and remaining limits"""
        results = {}
        
        for section, limit in self.deduction_limits.items():
            claimed = user_inputs.get(section, 0.0)
            remaining = max(0, limit - claimed)
            utilization = (claimed / limit) * 100 if limit > 0 else 0
            
            results[section] = {
                'claimed': claimed,
                'limit': limit,
                'remaining': remaining,
                'utilization': utilization
            }
        
        return results

    def get_document_checklist(self, section: str) -> List[str]:
        """Get document checklist for a specific section"""
        checklists = {
            '80C': [
                'Life Insurance premium receipts',
                'ELSS investment statements',
                'PPF passbook',
                'NSC certificates',
                'FD interest certificates',
                'Tuition fee receipts',
                'Home loan principal statement',
                'Sukanya Samriddhi passbook'
            ],
            '80D': [
                'Health insurance premium receipts',
                'Policy documents',
                'Health checkup bills'
            ],
            '24(b)': [
                'Home loan interest certificate',
                'Property registration documents',
                'Rent agreement (if applicable)'
            ],
            '80E': [
                'Education loan interest certificate',
                'Course admission proof',
                'Loan sanction letter'
            ],
            '80TTA': [
                'Bank interest certificate',
                'Post office interest certificate'
            ],
            '80CCD(1B)': [
                'NPS contribution statement',
                'PRAN card copy'
            ]
        }
        
        return checklists.get(section, [])

    def render(self):
        """Render the Deduction Scanner interface"""
        st.title("Deduction Scanner")
        st.markdown("""
            Track and maximize your tax deductions under various sections.
            Enter your claimed amounts to see utilization and remaining limits.
        """)

        # Initialize session state for user inputs
        if 'deduction_inputs' not in st.session_state:
            st.session_state.deduction_inputs = {
                section: 0.0 for section in self.deduction_limits.keys()
            }

        # Input form
        st.subheader("Enter Your Deductions")
        
        # Create two columns for input fields
        col1, col2 = st.columns(2)
        
        with col1:
            for section in list(self.deduction_limits.keys())[:3]:
                st.number_input(
                    f"Section {section} - {self.deduction_descriptions[section]['description']} (₹)",
                    min_value=0.0,
                    max_value=self.deduction_limits[section],
                    value=st.session_state.deduction_inputs[section],
                    key=f"input_{section}",
                    on_change=lambda s=section: self.update_input(s)
                )

        with col2:
            for section in list(self.deduction_limits.keys())[3:]:
                st.number_input(
                    f"Section {section} - {self.deduction_descriptions[section]['description']} (₹)",
                    min_value=0.0,
                    max_value=self.deduction_limits[section],
                    value=st.session_state.deduction_inputs[section],
                    key=f"input_{section}",
                    on_change=lambda s=section: self.update_input(s)
                )

        # Calculate and display results
        if st.button("Calculate Deductions"):
            results = self.calculate_deductions(st.session_state.deduction_inputs)
            
            # Display utilization chart
            st.subheader("Deduction Utilization")
            
            # Prepare data for chart
            chart_data = pd.DataFrame([
                {
                    'Section': section,
                    'Claimed': data['claimed'],
                    'Remaining': data['remaining']
                }
                for section, data in results.items()
            ])
            
            # Create stacked bar chart
            chart = alt.Chart(chart_data).mark_bar().encode(
                x='Section',
                y='Claimed',
                color=alt.value('green')
            ) + alt.Chart(chart_data).mark_bar().encode(
                x='Section',
                y='Remaining',
                color=alt.value('red')
            )
            
            st.altair_chart(chart, use_container_width=True)
            
            # Display detailed results
            st.subheader("Detailed Breakdown")
            
            for section, data in results.items():
                with st.expander(f"Section {section} - {self.deduction_descriptions[section]['description']}"):
                    # Display utilization
                    st.metric(
                        "Utilization",
                        f"{data['utilization']:.1f}%",
                        f"₹{data['claimed']:,.0f} of ₹{data['limit']:,.0f}"
                    )
                    
                    # Display document checklist
                    st.subheader("Required Documents")
                    for doc in self.get_document_checklist(section):
                        st.markdown(f"- {doc}")
                    
                    # Display eligible items
                    st.subheader("Eligible Items")
                    for item in self.deduction_descriptions[section]['items']:
                        st.markdown(f"- {item}")

    def update_input(self, section: str):
        """Update session state with new input value"""
        st.session_state.deduction_inputs[section] = st.session_state[f"input_{section}"] 