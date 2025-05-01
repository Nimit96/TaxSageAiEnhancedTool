"""
Master Playbook Module
Contains advanced tax planning strategies and recommendations
"""

import streamlit as st
from typing import Dict, List, Tuple
import pandas as pd

class MasterPlaybook:
    def __init__(self):
        self.strategies = {
            'HUF Formation': {
                'description': 'Create a Hindu Undivided Family to split income and reduce tax liability',
                'risk_level': 'Low',
                'legal_reference': 'Section 2(31) of Income Tax Act',
                'when_to_use': [
                    'You have significant family income',
                    'You want to create a separate tax entity',
                    'You have ancestral property'
                ],
                'when_to_avoid': [
                    'Single member family',
                    'No significant assets to transfer',
                    'Complex family structure'
                ],
                'steps': [
                    'Create HUF deed',
                    'Open HUF bank account',
                    'Transfer assets to HUF',
                    'File separate tax returns'
                ]
            },
            'Income Splitting': {
                'description': 'Split income among family members to utilize lower tax brackets',
                'risk_level': 'Low',
                'legal_reference': 'Section 64 of Income Tax Act',
                'when_to_use': [
                    'Spouse has no income',
                    'Children are above 18 years',
                    'Parents are senior citizens'
                ],
                'when_to_avoid': [
                    'Minor children',
                    'Clubbing provisions apply',
                    'Artificial income splitting'
                ],
                'steps': [
                    'Identify eligible family members',
                    'Create income-generating assets',
                    'Transfer assets legally',
                    'Maintain proper documentation'
                ]
            },
            'Family Salary': {
                'description': 'Pay salary to family members for genuine work in family business',
                'risk_level': 'Medium',
                'legal_reference': 'Section 15 of Income Tax Act',
                'when_to_use': [
                    'Running a family business',
                    'Family members contribute to business',
                    'Need to reduce business profits'
                ],
                'when_to_avoid': [
                    'No genuine work contribution',
                    'Excessive salary payments',
                    'No proper documentation'
                ],
                'steps': [
                    'Define job roles',
                    'Set reasonable salaries',
                    'Maintain attendance records',
                    'Issue Form 16'
                ]
            },
            'Rent to Parents': {
                'description': 'Pay rent to parents for using their property for business',
                'risk_level': 'Low',
                'legal_reference': 'Section 10(13A) of Income Tax Act',
                'when_to_use': [
                    'Parents own property',
                    'Property used for business',
                    'Need to reduce business income'
                ],
                'when_to_avoid': [
                    'No genuine business use',
                    'Excessive rent payments',
                    'No proper documentation'
                ],
                'steps': [
                    'Execute rent agreement',
                    'Pay rent through bank',
                    'Deduct TDS if applicable',
                    'Maintain property documents'
                ]
            },
            'Capital Gains Harvesting': {
                'description': 'Strategically realize capital gains to utilize exemptions and lower tax rates',
                'risk_level': 'Low',
                'legal_reference': 'Section 54, 54EC, 54F of Income Tax Act',
                'when_to_use': [
                    'Planning to sell assets',
                    'Have capital losses to offset',
                    'Want to utilize exemptions'
                ],
                'when_to_avoid': [
                    'Short-term trading',
                    'Market volatility',
                    'No proper planning'
                ],
                'steps': [
                    'Review asset portfolio',
                    'Plan sale timing',
                    'Calculate tax implications',
                    'Execute transactions'
                ]
            }
        }

    def get_strategy_details(self, strategy_name: str) -> Dict:
        """Get detailed information about a specific strategy"""
        return self.strategies.get(strategy_name, {})

    def filter_strategies(self, criteria: Dict[str, List[str]]) -> List[str]:
        """Filter strategies based on user criteria"""
        filtered = []
        
        for name, details in self.strategies.items():
            matches = True
            
            for criterion, values in criteria.items():
                if criterion in details and not any(v in details[criterion] for v in values):
                    matches = False
                    break
            
            if matches:
                filtered.append(name)
        
        return filtered

    def render(self):
        """Render the Master Playbook interface"""
        st.title("Master Playbook")
        st.markdown("""
            Access advanced tax planning strategies used by professionals.
            Each strategy includes detailed implementation steps and risk assessment.
        """)

        # Strategy selection
        selected_strategy = st.selectbox(
            "Select a Strategy",
            options=["Select Strategy"] + list(self.strategies.keys())
        )

        if selected_strategy != "Select Strategy":
            # Display strategy details
            details = self.get_strategy_details(selected_strategy)
            
            st.subheader(selected_strategy)
            st.markdown(f"**Description:** {details['description']}")
            
            # Risk level with color coding
            risk_color = {
                'Low': 'green',
                'Medium': 'orange',
                'High': 'red'
            }.get(details['risk_level'], 'gray')
            
            st.markdown(f"**Risk Level:** :{risk_color}[{details['risk_level']}]")
            st.markdown(f"**Legal Reference:** {details['legal_reference']}")
            
            # When to use/avoid
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("When to Use")
                for point in details['when_to_use']:
                    st.markdown(f"✓ {point}")
            
            with col2:
                st.subheader("When to Avoid")
                for point in details['when_to_avoid']:
                    st.markdown(f"✗ {point}")
            
            # Implementation steps
            st.subheader("Implementation Steps")
            for i, step in enumerate(details['steps'], 1):
                st.markdown(f"{i}. {step}")
            
            # Additional resources
            st.subheader("Additional Resources")
            st.markdown("""
                - Consult a tax professional before implementation
                - Maintain proper documentation
                - Review strategy annually
                - Stay updated with tax law changes
            """)

        # Strategy finder
        st.sidebar.subheader("Strategy Finder")
        
        # Filter criteria
        risk_preference = st.sidebar.multiselect(
            "Risk Level",
            options=['Low', 'Medium', 'High'],
            default=['Low']
        )
        
        situation = st.sidebar.multiselect(
            "Your Situation",
            options=[
                'Family Business',
                'Property Owner',
                'Investor',
                'Salaried',
                'Business Owner'
            ]
        )
        
        if st.sidebar.button("Find Strategies"):
            criteria = {
                'risk_level': risk_preference,
                'when_to_use': situation
            }
            
            matching_strategies = self.filter_strategies(criteria)
            
            if matching_strategies:
                st.sidebar.success("Matching Strategies:")
                for strategy in matching_strategies:
                    st.sidebar.markdown(f"- {strategy}")
            else:
                st.sidebar.info("No matching strategies found. Try adjusting your criteria.") 