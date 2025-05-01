"""
Salary Architect Module
Handles salary structure optimization and tax planning
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import Dict, List, Tuple
from datetime import datetime

from constants import (
    SALARY_COMPONENTS,
    HRA_EXEMPTION_RULES,
    METRO_CITIES,
    STANDARD_DEDUCTION
)

class SalaryArchitect:
    def __init__(self):
        self.salary_components = SALARY_COMPONENTS
        self.hra_exemption_rules = HRA_EXEMPTION_RULES
        self.metro_cities = METRO_CITIES

    def calculate_hra_exemption(
        self,
        basic_salary: float,
        hra_received: float,
        rent_paid: float,
        is_metro: bool
    ) -> float:
        """Calculate HRA exemption based on the three rules"""
        # Rule 1: Actual HRA received
        rule1 = hra_received

        # Rule 2: 50% of basic salary for metro, 40% for non-metro
        percentage = self.hra_exemption_rules['metro_cities' if is_metro else 'non_metro_cities']
        rule2 = basic_salary * percentage

        # Rule 3: Rent paid minus 10% of basic salary
        rule3 = max(0, rent_paid - (basic_salary * 0.10))

        # HRA exemption is the minimum of the three rules
        return min(rule1, rule2, rule3)

    def optimize_salary_structure(
        self,
        annual_ctc: float,
        bonus_percentage: float,
        rent_paid: float,
        city: str,
        selected_components: List[str]
    ) -> Dict[str, float]:
        """Optimize salary structure for maximum tax benefits"""
        is_metro = city in self.metro_cities
        
        # Initialize salary structure
        salary_structure = {component: 0.0 for component in self.salary_components}
        
        # Calculate bonus
        bonus = annual_ctc * (bonus_percentage / 100)
        salary_structure['Bonus'] = bonus
        
        # Calculate basic salary (40% of CTC)
        basic_salary = annual_ctc * 0.40
        salary_structure['Basic'] = basic_salary
        
        # Calculate HRA (20% of CTC)
        hra = annual_ctc * 0.20
        salary_structure['HRA'] = hra
        
        # Calculate HRA exemption
        hra_exemption = self.calculate_hra_exemption(
            basic_salary, hra, rent_paid, is_metro
        )
        
        # Calculate remaining components
        remaining_amount = annual_ctc - (basic_salary + hra + bonus)
        
        # Distribute remaining amount among selected components
        if remaining_amount > 0:
            num_components = len(selected_components)
            if num_components > 0:
                per_component = remaining_amount / num_components
                for component in selected_components:
                    if component not in ['Basic', 'HRA', 'Bonus']:
                        salary_structure[component] = per_component
        
        return salary_structure

    def render(self):
        """Render the Salary Architect interface"""
        st.title("Salary Architect")
        st.markdown("""
            Optimize your salary structure for maximum tax benefits.
            Enter your details below to get personalized recommendations.
        """)

        # Input form
        col1, col2 = st.columns(2)
        
        with col1:
            annual_ctc = st.number_input(
                "Annual CTC (₹)",
                min_value=0.0,
                value=1000000.0,
                step=10000.0
            )
            
            bonus_percentage = st.number_input(
                "Bonus Percentage (%)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.5
            )
            
            rent_paid = st.number_input(
                "Monthly Rent Paid (₹)",
                min_value=0.0,
                value=20000.0,
                step=1000.0
            ) * 12  # Convert to annual

        with col2:
            city = st.selectbox(
                "City of Residence",
                options=["Select City"] + self.metro_cities + ["Other"]
            )
            
            selected_components = st.multiselect(
                "Select Additional Components",
                options=[c for c in self.salary_components if c not in ['Basic', 'HRA', 'Bonus']],
                default=['LTA', 'Special Allowance', 'Meal Card']
            )

        # Calculate and display results
        if st.button("Optimize Salary Structure"):
            if city == "Select City":
                st.error("Please select your city of residence")
                return

            is_metro = city in self.metro_cities
            salary_structure = self.optimize_salary_structure(
                annual_ctc,
                bonus_percentage,
                rent_paid,
                city,
                selected_components
            )

            # Display results
            st.subheader("Optimized Salary Structure")
            
            # Create DataFrame for display
            df = pd.DataFrame(
                salary_structure.items(),
                columns=['Component', 'Amount (₹)']
            )
            df['Amount (₹)'] = df['Amount (₹)'].round(2)
            
            # Display table
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            # Calculate tax benefits
            hra_exemption = self.calculate_hra_exemption(
                salary_structure['Basic'],
                salary_structure['HRA'],
                rent_paid,
                is_metro
            )
            
            # Display tax benefits
            st.subheader("Tax Benefits")
            benefits_df = pd.DataFrame({
                'Benefit': ['HRA Exemption', 'Standard Deduction'],
                'Amount (₹)': [hra_exemption, STANDARD_DEDUCTION]
            })
            
            st.dataframe(
                benefits_df,
                use_container_width=True,
                hide_index=True
            )

            # Display recommendations
            st.subheader("Recommendations")
            recommendations = [
                "1. Consider increasing HRA component if you're paying high rent",
                "2. Maximize LTA claims by planning vacations strategically",
                "3. Use meal card for daily expenses to save on tax",
                "4. Consider car lease if you need a vehicle for work"
            ]
            
            for rec in recommendations:
                st.markdown(f"- {rec}")

            # Download salary structure
            st.download_button(
                label="Download Salary Structure",
                data=df.to_csv(index=False),
                file_name="salary_structure.csv",
                mime="text/csv"
            ) 