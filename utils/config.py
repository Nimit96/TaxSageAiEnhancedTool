"""
Configuration Module
Contains functions for handling configuration settings
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

class TaxConfig:
    def __init__(self, config_file: str = 'config.json'):
        """Initialize configuration with file path"""
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self._create_default_config()
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {str(e)}")
            self._create_default_config()

    def _create_default_config(self) -> None:
        """Create default configuration"""
        self.config = {
            'app': {
                'name': 'TaxSage',
                'version': '1.0.0',
                'debug': False,
                'log_level': 'INFO'
            },
            'database': {
                'type': 'sqlite',
                'path': 'tax_data.db'
            },
            'api': {
                'base_url': 'https://api.incometaxindia.gov.in',
                'timeout': 30,
                'retry_count': 3
            },
            'storage': {
                'base_dir': 'tax_data',
                'backup_dir': 'backups',
                'cache_dir': 'cache'
            },
            'logging': {
                'log_dir': 'logs',
                'max_file_size': 10485760,  # 10 MB
                'backup_count': 5
            },
            'security': {
                'encryption_key': '',
                'session_timeout': 3600  # 1 hour
            },
            'ui': {
                'theme': 'light',
                'language': 'en',
                'date_format': '%d-%m-%Y'
            },
            'tax': {
                'financial_year': '2025-26',
                'assessment_year': '2026-27',
                'currency': 'INR',
                'decimal_places': 2
            }
        }
        self._save_config()

    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {str(e)}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        try:
            keys = key.split('.')
            value = self.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by key"""
        try:
            keys = key.split('.')
            config = self.config
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            config[keys[-1]] = value
            self._save_config()
        except Exception as e:
            self.logger.error(f"Failed to set configuration: {str(e)}")

    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple configuration values"""
        try:
            for key, value in updates.items():
                self.set(key, value)
        except Exception as e:
            self.logger.error(f"Failed to update configuration: {str(e)}")

    def reset(self) -> None:
        """Reset configuration to defaults"""
        self._create_default_config()

    def get_app_config(self) -> Dict[str, Any]:
        """Get application configuration"""
        return self.get('app', {})

    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return self.get('database', {})

    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self.get('api', {})

    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage configuration"""
        return self.get('storage', {})

    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return self.get('logging', {})

    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return self.get('security', {})

    def get_ui_config(self) -> Dict[str, Any]:
        """Get UI configuration"""
        return self.get('ui', {})

    def get_tax_config(self) -> Dict[str, Any]:
        """Get tax configuration"""
        return self.get('tax', {})

    def set_app_config(self, config: Dict[str, Any]) -> None:
        """Set application configuration"""
        self.set('app', config)

    def set_database_config(self, config: Dict[str, Any]) -> None:
        """Set database configuration"""
        self.set('database', config)

    def set_api_config(self, config: Dict[str, Any]) -> None:
        """Set API configuration"""
        self.set('api', config)

    def set_storage_config(self, config: Dict[str, Any]) -> None:
        """Set storage configuration"""
        self.set('storage', config)

    def set_logging_config(self, config: Dict[str, Any]) -> None:
        """Set logging configuration"""
        self.set('logging', config)

    def set_security_config(self, config: Dict[str, Any]) -> None:
        """Set security configuration"""
        self.set('security', config)

    def set_ui_config(self, config: Dict[str, Any]) -> None:
        """Set UI configuration"""
        self.set('ui', config)

    def set_tax_config(self, config: Dict[str, Any]) -> None:
        """Set tax configuration"""
        self.set('tax', config)

    def validate_config(self) -> bool:
        """Validate configuration values"""
        try:
            # Validate required fields
            required_fields = [
                'app.name',
                'app.version',
                'database.type',
                'database.path',
                'api.base_url',
                'storage.base_dir',
                'logging.log_dir',
                'tax.financial_year'
            ]
            
            for field in required_fields:
                if not self.get(field):
                    self.logger.error(f"Missing required configuration field: {field}")
                    return False
            
            # Validate data types
            if not isinstance(self.get('app.debug'), bool):
                self.logger.error("Invalid data type for app.debug")
                return False
                
            if not isinstance(self.get('api.timeout'), int):
                self.logger.error("Invalid data type for api.timeout")
                return False
                
            if not isinstance(self.get('security.session_timeout'), int):
                self.logger.error("Invalid data type for security.session_timeout")
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            return False

    def backup_config(self, backup_dir: str = 'backups') -> bool:
        """Create backup of configuration"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = backup_path / f"config_backup_{timestamp}.json"
            
            with open(backup_file, 'w') as f:
                json.dump(self.config, f, indent=4)
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to backup configuration: {str(e)}")
            return False

    def restore_config(self, backup_file: str) -> bool:
        """Restore configuration from backup"""
        try:
            backup_path = Path(backup_file)
            
            if not backup_path.exists():
                return False
                
            with open(backup_path, 'r') as f:
                self.config = json.load(f)
                
            self._save_config()
            return True
        except Exception as e:
            self.logger.error(f"Failed to restore configuration: {str(e)}")
            return False 