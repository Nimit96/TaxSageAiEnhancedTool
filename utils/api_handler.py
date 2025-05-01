"""
API Handler Module
Contains functions for handling API requests and data fetching
"""

import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
import json
import logging
from pathlib import Path

class TaxAPIHandler:
    def __init__(self, base_url: str = 'https://api.incometaxindia.gov.in'):
        """Initialize API handler with base URL"""
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)

    def _make_request(
        self,
        endpoint: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make API request with error handling"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return {'error': str(e)}

    def get_tax_slabs(self, financial_year: str) -> Dict[str, Any]:
        """Get tax slabs for a financial year"""
        return self._make_request(
            endpoint=f'taxslabs/{financial_year}',
            method='GET'
        )

    def get_deduction_limits(self, financial_year: str) -> Dict[str, Any]:
        """Get deduction limits for a financial year"""
        return self._make_request(
            endpoint=f'deductions/{financial_year}',
            method='GET'
        )

    def get_capital_gains_rules(self, asset_type: str) -> Dict[str, Any]:
        """Get capital gains rules for an asset type"""
        return self._make_request(
            endpoint=f'capitalgains/{asset_type}',
            method='GET'
        )

    def get_crypto_tax_rules(self) -> Dict[str, Any]:
        """Get crypto tax rules"""
        return self._make_request(
            endpoint='crypto/rules',
            method='GET'
        )

    def validate_pan(self, pan: str) -> Dict[str, Any]:
        """Validate PAN number"""
        return self._make_request(
            endpoint='validate/pan',
            method='POST',
            data={'pan': pan}
        )

    def get_tds_certificates(self, pan: str, financial_year: str) -> Dict[str, Any]:
        """Get TDS certificates for a PAN and financial year"""
        return self._make_request(
            endpoint=f'tds/certificates/{pan}/{financial_year}',
            method='GET'
        )

    def get_form26as(self, pan: str, financial_year: str) -> Dict[str, Any]:
        """Get Form 26AS for a PAN and financial year"""
        return self._make_request(
            endpoint=f'form26as/{pan}/{financial_year}',
            method='GET'
        )

    def get_itr_status(self, pan: str, financial_year: str) -> Dict[str, Any]:
        """Get ITR filing status"""
        return self._make_request(
            endpoint=f'itr/status/{pan}/{financial_year}',
            method='GET'
        )

    def get_refund_status(self, pan: str, financial_year: str) -> Dict[str, Any]:
        """Get tax refund status"""
        return self._make_request(
            endpoint=f'refund/status/{pan}/{financial_year}',
            method='GET'
        )

    def get_notices(self, pan: str) -> Dict[str, Any]:
        """Get tax notices for a PAN"""
        return self._make_request(
            endpoint=f'notices/{pan}',
            method='GET'
        )

    def get_circulars(self, year: int) -> Dict[str, Any]:
        """Get tax circulars for a year"""
        return self._make_request(
            endpoint=f'circulars/{year}',
            method='GET'
        )

    def get_budget_updates(self, year: int) -> Dict[str, Any]:
        """Get budget updates for a year"""
        return self._make_request(
            endpoint=f'budget/{year}',
            method='GET'
        )

    def get_exchange_rates(self, date: datetime) -> Dict[str, Any]:
        """Get exchange rates for a date"""
        return self._make_request(
            endpoint=f'exchange/rates/{date.strftime("%Y-%m-%d")}',
            method='GET'
        )

    def get_market_data(self, symbol: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get market data for a symbol"""
        return self._make_request(
            endpoint='market/data',
            method='GET',
            params={
                'symbol': symbol,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        )

    def get_crypto_prices(self, symbol: str, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Get crypto prices for a symbol"""
        return self._make_request(
            endpoint='crypto/prices',
            method='GET',
            params={
                'symbol': symbol,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d')
            }
        )

    def cache_response(self, key: str, data: Dict[str, Any], cache_dir: str = 'cache') -> None:
        """Cache API response"""
        cache_path = Path(cache_dir)
        cache_path.mkdir(exist_ok=True)
        
        file_path = cache_path / f"{key}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)

    def get_cached_response(self, key: str, cache_dir: str = 'cache') -> Optional[Dict[str, Any]]:
        """Get cached API response"""
        file_path = Path(cache_dir) / f"{key}.json"
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return None

    def clear_cache(self, cache_dir: str = 'cache') -> None:
        """Clear API response cache"""
        cache_path = Path(cache_dir)
        if cache_path.exists():
            for file in cache_path.glob('*.json'):
                file.unlink()

    def set_api_key(self, api_key: str) -> None:
        """Set API key for authentication"""
        self.session.headers.update({'Authorization': f'Bearer {api_key}'})

    def set_proxy(self, proxy: str) -> None:
        """Set proxy for API requests"""
        self.session.proxies = {
            'http': proxy,
            'https': proxy
        } 