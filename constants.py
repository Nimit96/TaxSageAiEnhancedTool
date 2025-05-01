"""
TaxSageAiEnhanced - Constants Module
Contains all tax-related constants, slabs, and configurations for FY 2024-25 and 2025-26
"""

from typing import Dict, List, Tuple
from datetime import datetime

# Tax Slabs for FY 2024-25 (AY 2025-26)
TAX_SLABS_2024_25: List[Tuple[float, float, float]] = [
    (0, 300000, 0),  # No tax
    (300001, 600000, 0.05),  # 5%
    (600001, 900000, 0.10),  # 10%
    (900001, 1200000, 0.15),  # 15%
    (1200001, 1500000, 0.20),  # 20%
    (1500001, float('inf'), 0.30),  # 30%
]

# Tax Slabs for FY 2025-26 (AY 2026-27)
# Note: These will be updated when Budget 2025 is announced
TAX_SLABS_2025_26: List[Tuple[float, float, float]] = [
    (0, 300000, 0),  # No tax
    (300001, 600000, 0.05),  # 5%
    (600001, 900000, 0.10),  # 10%
    (900001, 1200000, 0.15),  # 15%
    (1200001, 1500000, 0.20),  # 20%
    (1500001, float('inf'), 0.30),  # 30%
]

# Standard Deduction
STANDARD_DEDUCTION: float = 50000

# Section 80C Deductions
MAX_80C_DEDUCTION: float = 150000

# Section 80D Deductions (Health Insurance)
MAX_80D_DEDUCTION: Dict[str, float] = {
    'self': 25000,
    'parents': 25000,
    'senior_citizen': 50000,
    'preventive_health_checkup': 5000
}

# Section 24(b) - Home Loan Interest
MAX_HOME_LOAN_INTEREST: float = 200000

# Section 80E - Education Loan Interest
MAX_EDUCATION_LOAN_INTEREST: float = float('inf')  # No upper limit

# Section 80TTA - Savings Account Interest
MAX_80TTA_DEDUCTION: float = 10000

# Section 80CCD(1B) - NPS Additional Deduction
MAX_NPS_ADDITIONAL_DEDUCTION: float = 50000

# Capital Gains
LTCG_TAX_RATE: float = 0.10  # 10% for equity
STCG_TAX_RATE: float = 0.15  # 15% for equity
LTCG_EXEMPTION_LIMIT: float = 100000  # ₹1 lakh exemption

# Crypto Tax
CRYPTO_TAX_RATE: float = 0.30  # 30% flat rate
CRYPTO_TDS_RATE: float = 0.01  # 1% TDS

# HRA Exemption
HRA_EXEMPTION_RULES: Dict[str, float] = {
    'metro_cities': 0.50,  # 50% of basic salary
    'non_metro_cities': 0.40  # 40% of basic salary
}

# Metro Cities List
METRO_CITIES: List[str] = [
    'Mumbai',
    'Delhi',
    'Kolkata',
    'Chennai',
    'Bangalore',
    'Hyderabad',
    'Ahmedabad',
    'Pune'
]

# Salary Components
SALARY_COMPONENTS: List[str] = [
    'Basic',
    'HRA',
    'LTA',
    'Bonus',
    'Special Allowance',
    'Meal Card',
    'Car Lease',
    'Gratuity',
    'Phone Bill',
    'Fuel'
]

# Auto Update Configuration
UPDATE_SOURCES: Dict[str, str] = {
    'income_tax_portal': 'https://www.incometaxindia.gov.in/',
    'pib': 'https://pib.gov.in/',
    'budget': 'https://www.indiabudget.gov.in/'
}

# Update Frequency (in hours)
UPDATE_FREQUENCY: int = 24

def get_current_fy() -> str:
    """Returns the current financial year in format 'YYYY-YY'"""
    current_date = datetime.now()
    if current_date.month >= 4:
        return f"{current_date.year}-{str(current_date.year + 1)[-2:]}"
    else:
        return f"{current_date.year - 1}-{str(current_date.year)[-2:]}"

def get_tax_slabs() -> List[Tuple[float, float, float]]:
    """Returns the appropriate tax slabs based on current FY"""
    current_fy = get_current_fy()
    if current_fy == "2024-25":
        return TAX_SLABS_2024_25
    else:
        return TAX_SLABS_2025_26 