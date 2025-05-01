"""
Data Storage and Retrieval Module
Contains functions for storing and retrieving tax-related data
"""

import os
import json
import pandas as pd
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import sqlite3
from pathlib import Path

class TaxStorage:
    def __init__(self, db_path: str = 'tax_data.db'):
        """Initialize storage with database path"""
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pan TEXT UNIQUE,
                    name TEXT,
                    email TEXT,
                    mobile TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create income table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS income (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    financial_year TEXT,
                    salary_amount REAL,
                    other_income REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create deductions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deductions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    financial_year TEXT,
                    section TEXT,
                    amount REAL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create capital gains table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS capital_gains (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    financial_year TEXT,
                    asset_type TEXT,
                    purchase_price REAL,
                    sale_price REAL,
                    purchase_date DATE,
                    sale_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Create crypto transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS crypto_transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    financial_year TEXT,
                    transaction_type TEXT,
                    amount REAL,
                    date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()

    def save_user_data(self, user_data: Dict[str, Any]) -> int:
        """Save user data and return user ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO users (pan, name, email, mobile)
                VALUES (?, ?, ?, ?)
            ''', (
                user_data['pan'],
                user_data['name'],
                user_data['email'],
                user_data['mobile']
            ))
            user_id = cursor.lastrowid
            conn.commit()
            return user_id

    def save_income_data(self, user_id: int, income_data: Dict[str, Any]) -> int:
        """Save income data and return income ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO income (user_id, financial_year, salary_amount, other_income)
                VALUES (?, ?, ?, ?)
            ''', (
                user_id,
                income_data['financial_year'],
                income_data['salary_amount'],
                income_data.get('other_income', 0)
            ))
            income_id = cursor.lastrowid
            conn.commit()
            return income_id

    def save_deduction_data(self, user_id: int, deduction_data: Dict[str, Any]) -> int:
        """Save deduction data and return deduction ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO deductions (user_id, financial_year, section, amount, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                deduction_data['financial_year'],
                deduction_data['section'],
                deduction_data['amount'],
                deduction_data.get('description', '')
            ))
            deduction_id = cursor.lastrowid
            conn.commit()
            return deduction_id

    def save_capital_gains_data(self, user_id: int, gains_data: Dict[str, Any]) -> int:
        """Save capital gains data and return gains ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO capital_gains (
                    user_id, financial_year, asset_type,
                    purchase_price, sale_price, purchase_date, sale_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                gains_data['financial_year'],
                gains_data['asset_type'],
                gains_data['purchase_price'],
                gains_data['sale_price'],
                gains_data['purchase_date'],
                gains_data['sale_date']
            ))
            gains_id = cursor.lastrowid
            conn.commit()
            return gains_id

    def save_crypto_transaction(self, user_id: int, transaction_data: Dict[str, Any]) -> int:
        """Save crypto transaction data and return transaction ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO crypto_transactions (
                    user_id, financial_year, transaction_type, amount, date
                )
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_id,
                transaction_data['financial_year'],
                transaction_data['transaction_type'],
                transaction_data['amount'],
                transaction_data['date']
            ))
            transaction_id = cursor.lastrowid
            conn.commit()
            return transaction_id

    def get_user_data(self, pan: str) -> Optional[Dict[str, Any]]:
        """Get user data by PAN"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE pan = ?', (pan,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'pan': row[1],
                    'name': row[2],
                    'email': row[3],
                    'mobile': row[4],
                    'created_at': row[5]
                }
            return None

    def get_income_data(self, user_id: int, financial_year: str) -> Optional[Dict[str, Any]]:
        """Get income data for user and financial year"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM income
                WHERE user_id = ? AND financial_year = ?
            ''', (user_id, financial_year))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'user_id': row[1],
                    'financial_year': row[2],
                    'salary_amount': row[3],
                    'other_income': row[4],
                    'created_at': row[5]
                }
            return None

    def get_deductions(self, user_id: int, financial_year: str) -> List[Dict[str, Any]]:
        """Get all deductions for user and financial year"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM deductions
                WHERE user_id = ? AND financial_year = ?
            ''', (user_id, financial_year))
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'user_id': row[1],
                'financial_year': row[2],
                'section': row[3],
                'amount': row[4],
                'description': row[5],
                'created_at': row[6]
            } for row in rows]

    def get_capital_gains(self, user_id: int, financial_year: str) -> List[Dict[str, Any]]:
        """Get all capital gains for user and financial year"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM capital_gains
                WHERE user_id = ? AND financial_year = ?
            ''', (user_id, financial_year))
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'user_id': row[1],
                'financial_year': row[2],
                'asset_type': row[3],
                'purchase_price': row[4],
                'sale_price': row[5],
                'purchase_date': row[6],
                'sale_date': row[7],
                'created_at': row[8]
            } for row in rows]

    def get_crypto_transactions(self, user_id: int, financial_year: str) -> List[Dict[str, Any]]:
        """Get all crypto transactions for user and financial year"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM crypto_transactions
                WHERE user_id = ? AND financial_year = ?
            ''', (user_id, financial_year))
            rows = cursor.fetchall()
            return [{
                'id': row[0],
                'user_id': row[1],
                'financial_year': row[2],
                'transaction_type': row[3],
                'amount': row[4],
                'date': row[5],
                'created_at': row[6]
            } for row in rows]

    def export_to_excel(self, user_id: int, financial_year: str, output_path: str) -> None:
        """Export user's tax data to Excel file"""
        # Create DataFrames for each table
        income_df = pd.DataFrame([self.get_income_data(user_id, financial_year)])
        deductions_df = pd.DataFrame(self.get_deductions(user_id, financial_year))
        gains_df = pd.DataFrame(self.get_capital_gains(user_id, financial_year))
        crypto_df = pd.DataFrame(self.get_crypto_transactions(user_id, financial_year))
        
        # Create Excel writer
        with pd.ExcelWriter(output_path) as writer:
            if not income_df.empty:
                income_df.to_excel(writer, sheet_name='Income', index=False)
            if not deductions_df.empty:
                deductions_df.to_excel(writer, sheet_name='Deductions', index=False)
            if not gains_df.empty:
                gains_df.to_excel(writer, sheet_name='Capital Gains', index=False)
            if not crypto_df.empty:
                crypto_df.to_excel(writer, sheet_name='Crypto Transactions', index=False)

    def backup_database(self, backup_path: str) -> None:
        """Create a backup of the database"""
        import shutil
        shutil.copy2(self.db_path, backup_path)

    def restore_database(self, backup_path: str) -> None:
        """Restore database from backup"""
        import shutil
        shutil.copy2(backup_path, self.db_path) 