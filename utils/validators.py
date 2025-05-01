"""
Data Validation and Formatting Module
Contains functions for validating and formatting tax-related data
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import re
import pandas as pd

class TaxValidator:
    @staticmethod
    def validate_pan(pan: str) -> bool:
        """Validate PAN number format"""
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pattern, pan))

    @staticmethod
    def validate_aadhaar(aadhaar: str) -> bool:
        """Validate Aadhaar number format"""
        pattern = r'^[0-9]{12}$'
        return bool(re.match(pattern, aadhaar))

    @staticmethod
    def validate_ifsc(ifsc: str) -> bool:
        """Validate IFSC code format"""
        pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
        return bool(re.match(pattern, ifsc))

    @staticmethod
    def validate_mobile(mobile: str) -> bool:
        """Validate mobile number format"""
        pattern = r'^[6-9][0-9]{9}$'
        return bool(re.match(pattern, mobile))

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_amount(amount: Union[str, float]) -> bool:
        """Validate amount format"""
        try:
            float(amount)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
        """Validate date format"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False

    @staticmethod
    def format_currency(amount: float) -> str:
        """Format amount as Indian currency"""
        return f'₹{amount:,.2f}'

    @staticmethod
    def format_percentage(value: float) -> str:
        """Format value as percentage"""
        return f'{value:.2f}%'

    @staticmethod
    def format_date(date: datetime, format: str = '%d-%b-%Y') -> str:
        """Format date in specified format"""
        return date.strftime(format)

    @staticmethod
    def validate_deduction_limits(
        claimed_amount: float,
        max_limit: float,
        section: str
    ) -> Dict[str, Any]:
        """Validate deduction claim against limits"""
        if claimed_amount > max_limit:
            return {
                'is_valid': False,
                'message': f'Claimed amount exceeds maximum limit of {max_limit} for section {section}',
                'allowed_amount': max_limit
            }
        return {
            'is_valid': True,
            'message': 'Claim is within limits',
            'allowed_amount': claimed_amount
        }

    @staticmethod
    def validate_tax_slabs(income: float) -> Dict[str, Any]:
        """Validate income against tax slabs"""
        if income < 0:
            return {
                'is_valid': False,
                'message': 'Income cannot be negative',
                'slab': None
            }
        return {
            'is_valid': True,
            'message': 'Income is valid',
            'slab': 'Applicable slab will be determined during calculation'
        }

    @staticmethod
    def validate_capital_gains(
        purchase_price: float,
        sale_price: float,
        purchase_date: datetime,
        sale_date: datetime
    ) -> Dict[str, Any]:
        """Validate capital gains calculation inputs"""
        errors = []
        
        if purchase_price < 0:
            errors.append('Purchase price cannot be negative')
        if sale_price < 0:
            errors.append('Sale price cannot be negative')
        if sale_date < purchase_date:
            errors.append('Sale date cannot be before purchase date')
            
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    @staticmethod
    def validate_crypto_transaction(
        amount: float,
        date: datetime,
        transaction_type: str
    ) -> Dict[str, Any]:
        """Validate crypto transaction inputs"""
        errors = []
        
        if amount <= 0:
            errors.append('Amount must be positive')
        if date > datetime.now():
            errors.append('Transaction date cannot be in the future')
        if transaction_type not in ['buy', 'sell', 'transfer']:
            errors.append('Invalid transaction type')
            
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    @staticmethod
    def validate_rent_receipts(
        receipts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate rent receipts data"""
        errors = []
        
        for receipt in receipts:
            if not TaxValidator.validate_amount(receipt.get('amount', 0)):
                errors.append(f'Invalid amount in receipt for {receipt.get("month")}')
            if not TaxValidator.validate_date(receipt.get('date', '')):
                errors.append(f'Invalid date in receipt for {receipt.get("month")}')
            if not receipt.get('landlord_pan'):
                errors.append(f'Missing landlord PAN for {receipt.get("month")}')
                
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    @staticmethod
    def validate_investment_proofs(
        proofs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Validate investment proofs data"""
        errors = []
        
        for proof in proofs:
            if not TaxValidator.validate_amount(proof.get('amount', 0)):
                errors.append(f'Invalid amount in proof for {proof.get("type")}')
            if not TaxValidator.validate_date(proof.get('date', '')):
                errors.append(f'Invalid date in proof for {proof.get("type")}')
            if not proof.get('document_number'):
                errors.append(f'Missing document number for {proof.get("type")}')
                
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }

    @staticmethod
    def format_tax_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Format tax data for display"""
        formatted_data = {}
        
        for key, value in data.items():
            if isinstance(value, (int, float)):
                if 'amount' in key.lower() or 'tax' in key.lower():
                    formatted_data[key] = TaxValidator.format_currency(value)
                elif 'rate' in key.lower() or 'percentage' in key.lower():
                    formatted_data[key] = TaxValidator.format_percentage(value)
                else:
                    formatted_data[key] = value
            elif isinstance(value, datetime):
                formatted_data[key] = TaxValidator.format_date(value)
            else:
                formatted_data[key] = value
                
        return formatted_data 