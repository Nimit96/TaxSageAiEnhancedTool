"""
Tax Calculator Utility Module
Contains common tax calculation functions
"""

from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np

from constants import get_tax_slabs

class TaxCalculator:
    def __init__(self):
        self.tax_slabs = get_tax_slabs()

    def calculate_income_tax(self, taxable_income: float) -> Dict[str, float]:
        """Calculate income tax based on tax slabs"""
        tax = 0.0
        remaining_income = taxable_income
        
        for lower, upper, rate in self.tax_slabs:
            if remaining_income <= 0:
                break
                
            slab_amount = min(remaining_income, upper - lower)
            tax += slab_amount * rate
            remaining_income -= slab_amount
        
        # Add health and education cess (4%)
        cess = tax * 0.04
        total_tax = tax + cess
        
        return {
            'basic_tax': tax,
            'cess': cess,
            'total_tax': total_tax,
            'effective_rate': (total_tax / taxable_income) * 100 if taxable_income > 0 else 0
        }

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
        percentage = 0.50 if is_metro else 0.40
        rule2 = basic_salary * percentage

        # Rule 3: Rent paid minus 10% of basic salary
        rule3 = max(0, rent_paid - (basic_salary * 0.10))

        # HRA exemption is the minimum of the three rules
        return min(rule1, rule2, rule3)

    def calculate_capital_gains(
        self,
        purchase_price: float,
        sale_price: float,
        purchase_date: datetime,
        sale_date: datetime,
        expenses: float = 0.0,
        is_equity: bool = True
    ) -> Dict[str, float]:
        """Calculate capital gains and tax liability"""
        holding_period = (sale_date - purchase_date).days
        
        # Calculate capital gain
        capital_gain = sale_price - purchase_price - expenses
        
        # Determine if long-term
        is_long_term = holding_period >= 365 if is_equity else holding_period >= 24
        
        # Calculate tax
        if is_equity:
            if is_long_term:
                # Apply exemption limit
                taxable_gain = max(0, capital_gain - 100000)  # ₹1 lakh exemption
                tax = taxable_gain * 0.10  # 10% LTCG tax
                tax_type = "LTCG"
            else:
                tax = capital_gain * 0.15  # 15% STCG tax
                tax_type = "STCG"
        else:
            if is_long_term:
                tax = capital_gain * 0.20  # 20% LTCG tax with indexation
                tax_type = "LTCG"
            else:
                tax = capital_gain * 0.30  # 30% STCG tax
                tax_type = "STCG"
        
        return {
            'capital_gain': capital_gain,
            'tax': tax,
            'tax_type': tax_type,
            'holding_period_days': holding_period,
            'is_long_term': is_long_term
        }

    def calculate_crypto_tax(
        self,
        purchase_price: float,
        sale_price: float,
        expenses: float = 0.0
    ) -> Dict[str, float]:
        """Calculate crypto tax and TDS"""
        # Calculate capital gain
        capital_gain = sale_price - purchase_price - expenses
        
        # Calculate tax (30% flat rate)
        tax = capital_gain * 0.30
        
        # Calculate TDS (1% of sale price)
        tds = sale_price * 0.01
        
        return {
            'capital_gain': capital_gain,
            'tax': tax,
            'tds': tds,
            'total_liability': tax + tds
        }

    def calculate_deduction_utilization(
        self,
        claimed_amount: float,
        max_limit: float
    ) -> Dict[str, float]:
        """Calculate deduction utilization and remaining limit"""
        remaining = max(0, max_limit - claimed_amount)
        utilization = (claimed_amount / max_limit) * 100 if max_limit > 0 else 0
        
        return {
            'claimed': claimed_amount,
            'remaining': remaining,
            'utilization': utilization
        } 