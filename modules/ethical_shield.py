"""
Ethical Shield Module
Warns users about unethical tax practices and provides legal alternatives
"""

import streamlit as st
from typing import Dict, List, Tuple
import pandas as pd

class EthicalShield:
    def __init__(self):
        self.unethical_practices = {
            'Fake Rent Receipts': {
                'description': 'Creating fake rent receipts to claim HRA exemption',
                'risk_level': 'High',
                'consequences': [
                    'Tax evasion charges',
                    'Penalties up to 300% of tax evaded',
                    'Criminal prosecution',
                    'Damage to credit score'
                ],
                'legal_alternative': 'Use genuine rent agreement and actual rent payments',
                'documentation': [
                    'Rent agreement',
                    'Bank statements showing rent payments',
                    'Landlord PAN card',
                    'Property ownership proof'
                ]
            },
            'Fake Donation Bills': {
                'description': 'Using fake donation receipts to claim deductions',
                'risk_level': 'High',
                'consequences': [
                    'Tax evasion charges',
                    'Penalties and interest',
                    'Blacklisting of donor',
                    'Legal action against charity'
                ],
                'legal_alternative': 'Donate to registered charities and maintain proper receipts',
                'documentation': [
                    'Donation receipt with 80G number',
                    'Charity registration certificate',
                    'Bank transfer proof',
                    'Donation acknowledgment'
                ]
            },
            'Benami Transactions': {
                'description': 'Holding assets in someone else\'s name to evade taxes',
                'risk_level': 'Critical',
                'consequences': [
                    'Asset confiscation',
                    'Heavy penalties',
                    'Criminal prosecution',
                    'Blacklisting'
                ],
                'legal_alternative': 'Use legal structures like HUF or family partnerships',
                'documentation': [
                    'Property documents',
                    'Bank statements',
                    'Income tax returns',
                    'Family partnership deed'
                ]
            },
            'Undisclosed Income': {
                'description': 'Not reporting cash income or foreign assets',
                'risk_level': 'Critical',
                'consequences': [
                    'Tax evasion charges',
                    'Black money penalties',
                    'Asset seizure',
                    'Criminal prosecution'
                ],
                'legal_alternative': 'Use income disclosure schemes and report all income',
                'documentation': [
                    'Bank statements',
                    'Income tax returns',
                    'Foreign asset declarations',
                    'Income proofs'
                ]
            },
            'Round Tripping': {
                'description': 'Converting black money to white through fake transactions',
                'risk_level': 'Critical',
                'consequences': [
                    'Money laundering charges',
                    'Asset seizure',
                    'Criminal prosecution',
                    'International blacklisting'
                ],
                'legal_alternative': 'Use legal investment options and report all income',
                'documentation': [
                    'Bank statements',
                    'Investment proofs',
                    'Income tax returns',
                    'Transaction records'
                ]
            }
        }

    def get_practice_details(self, practice_name: str) -> Dict:
        """Get detailed information about a specific unethical practice"""
        return self.unethical_practices.get(practice_name, {})

    def render(self):
        """Render the Ethical Shield interface"""
        st.title("Ethical Shield")
        st.markdown("""
            Learn about unethical tax practices and their legal alternatives.
            Stay compliant and avoid penalties with proper documentation.
        """)

        # Warning banner
        st.warning("""
            ⚠️ **Important Notice**
            
            This section highlights common unethical tax practices that should be avoided.
            Engaging in these practices can lead to severe legal consequences.
            Always consult a qualified tax professional for advice.
        """)

        # Practice selection
        selected_practice = st.selectbox(
            "Select a Practice to Learn About",
            options=["Select Practice"] + list(self.unethical_practices.keys())
        )

        if selected_practice != "Select Practice":
            # Display practice details
            details = self.get_practice_details(selected_practice)
            
            st.subheader(selected_practice)
            st.markdown(f"**Description:** {details['description']}")
            
            # Risk level with color coding
            risk_color = {
                'High': 'red',
                'Critical': 'red',
                'Medium': 'orange',
                'Low': 'yellow'
            }.get(details['risk_level'], 'gray')
            
            st.markdown(f"**Risk Level:** :{risk_color}[{details['risk_level']}]")
            
            # Consequences
            st.subheader("Consequences")
            for consequence in details['consequences']:
                st.markdown(f"❌ {consequence}")
            
            # Legal alternative
            st.subheader("Legal Alternative")
            st.success(f"✅ {details['legal_alternative']}")
            
            # Required documentation
            st.subheader("Required Documentation")
            for doc in details['documentation']:
                st.markdown(f"📄 {doc}")
            
            # Additional warning
            st.error("""
                ⚠️ **Remember:**
                - Tax evasion is a criminal offense
                - Penalties can exceed the tax evaded
                - Legal consequences can affect your future
                - Always maintain proper documentation
            """)

        # Quick reference guide
        st.sidebar.subheader("Quick Reference Guide")
        
        # Risk levels
        st.sidebar.markdown("""
            **Risk Levels:**
            - :red[Critical]: Immediate legal action
            - :red[High]: Severe penalties
            - :orange[Medium]: Significant fines
            - :yellow[Low]: Warning or small fines
        """)
        
        # Common red flags
        st.sidebar.subheader("Red Flags to Watch For")
        st.sidebar.markdown("""
            - Unregistered tax consultants
            - Promises of guaranteed tax savings
            - Requests for cash payments
            - No documentation requirements
            - Pressure to sign blank forms
        """)
        
        # Legal alternatives
        st.sidebar.subheader("Legal Alternatives")
        st.sidebar.markdown("""
            - Use government-approved schemes
            - Maintain proper documentation
            - Consult registered tax professionals
            - File returns on time
            - Use digital payment methods
        """)
        
        # Report unethical practices
        st.sidebar.subheader("Report Unethical Practices")
        st.sidebar.markdown("""
            If you encounter unethical tax practices:
            
            1. Report to Income Tax Department
            2. Contact CBDT helpline
            3. Use the e-filing portal
            4. Maintain evidence
        """) 