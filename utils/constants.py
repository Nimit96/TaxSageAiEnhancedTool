"""
Tax Constants Module
Contains tax-related constants and configurations
"""

from typing import List, Tuple

def get_tax_slabs() -> List[Tuple[float, float, float]]:
    """Get income tax slabs for FY 2025-26"""
    return [
        (0, 300000, 0.0),        # No tax up to ₹3 lakh
        (300000, 600000, 0.05),  # 5% for ₹3-6 lakh
        (600000, 900000, 0.10),  # 10% for ₹6-9 lakh
        (900000, 1200000, 0.15), # 15% for ₹9-12 lakh
        (1200000, 1500000, 0.20),# 20% for ₹12-15 lakh
        (1500000, float('inf'), 0.30) # 30% above ₹15 lakh
    ]

# Deduction limits
DEDUCTION_LIMITS = {
    '80C': 150000,      # Life insurance, PPF, etc.
    '80D': 25000,       # Health insurance (₹50,000 for senior citizens)
    '80E': 150000,      # Education loan interest
    '80G': 100000,      # Charitable donations
    '80TTA': 10000,     # Savings account interest
    '80TTB': 50000,     # Senior citizen savings interest
    '80GG': 60000,      # Rent paid (if HRA not received)
    '80GGA': 100000,    # Scientific research donations
    '80GGC': 100000,    # Political party donations
    '80U': 125000,      # Disability deduction
    '80RRB': 300000,    # Patent royalty
    '80QQB': 300000,    # Book royalty
}

# Capital gains tax rates
CAPITAL_GAINS_TAX = {
    'equity': {
        'stcg': 0.15,   # Short-term capital gains
        'ltcg': 0.10,   # Long-term capital gains
        'exemption': 100000  # ₹1 lakh exemption for LTCG
    },
    'debt': {
        'stcg': 0.30,   # Short-term capital gains
        'ltcg': 0.20,   # Long-term capital gains (with indexation)
        'exemption': 0
    },
    'crypto': {
        'tax_rate': 0.30,  # 30% flat rate
        'tds_rate': 0.01   # 1% TDS
    }
}

# Holding periods (in days)
HOLDING_PERIODS = {
    'equity': 365,      # 1 year for equity
    'debt': 730,        # 2 years for debt
    'real_estate': 730, # 2 years for real estate
    'crypto': 365       # 1 year for crypto
}

# Metro cities for HRA calculation
METRO_CITIES = [
    'Mumbai',
    'Delhi',
    'Kolkata',
    'Chennai',
    'Bangalore',
    'Hyderabad',
    'Ahmedabad',
    'Pune'
]

# Tax saving investment options
TAX_SAVING_OPTIONS = {
    '80C': [
        'Public Provident Fund (PPF)',
        'Employee Provident Fund (EPF)',
        'National Savings Certificate (NSC)',
        'Tax Saving Fixed Deposit',
        'Equity Linked Savings Scheme (ELSS)',
        'Life Insurance Premium',
        'Sukanya Samriddhi Yojana',
        'Senior Citizen Savings Scheme',
        'National Pension System (NPS)',
        'Home Loan Principal Repayment'
    ],
    '80D': [
        'Health Insurance Premium',
        'Preventive Health Check-up',
        'Medical Expenses for Senior Citizens'
    ],
    '80E': [
        'Education Loan Interest'
    ],
    '80G': [
        'Charitable Donations',
        'Relief Funds',
        'Scientific Research'
    ]
}

# Tax filing due dates
DUE_DATES = {
    'advance_tax': [
        ('15-Jun', 0.15),  # 15% of estimated tax
        ('15-Sep', 0.45),  # 45% of estimated tax
        ('15-Dec', 0.75),  # 75% of estimated tax
        ('15-Mar', 1.00)   # 100% of estimated tax
    ],
    'return_filing': '31-Jul',  # For individuals
    'belated_return': '31-Dec', # Last date for belated return
    'revised_return': '31-Mar'  # Last date for revised return
}

# Tax audit thresholds
AUDIT_THRESHOLDS = {
    'business': 10000000,  # ₹1 crore for business
    'profession': 5000000, # ₹50 lakh for profession
    'presumptive': 2000000 # ₹20 lakh for presumptive taxation
}

# Tax rates for different types of income
TAX_RATES = {
    'salary': {
        'standard_deduction': 50000,  # ₹50,000 standard deduction
        'professional_tax': 2500,     # Maximum professional tax
        'gratuity_exemption': 2000000 # ₹20 lakh gratuity exemption
    },
    'house_property': {
        'standard_deduction': 0.30,   # 30% standard deduction
        'interest_deduction': 200000  # ₹2 lakh interest deduction
    },
    'business': {
        'presumptive_rate': 0.06,     # 6% presumptive rate
        'higher_rate': 0.08           # 8% for digital transactions
    }
} 