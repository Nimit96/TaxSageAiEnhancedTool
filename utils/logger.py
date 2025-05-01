"""
Logger Module
Contains functions for handling logging and error tracking
"""

import logging
import sys
from typing import Optional
from pathlib import Path
from datetime import datetime
import traceback
import json

class TaxLogger:
    def __init__(
        self,
        log_dir: str = 'logs',
        log_level: int = logging.INFO,
        max_file_size: int = 10 * 1024 * 1024,  # 10 MB
        backup_count: int = 5
    ):
        """Initialize logger with configuration"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        self.logger = logging.getLogger('tax_sage')
        self.logger.setLevel(log_level)
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # Add console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Add file handler
        log_file = self.log_dir / 'tax_sage.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs) -> None:
        """Log info message"""
        self.logger.info(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        """Log warning message"""
        self.logger.warning(message, **kwargs)

    def error(self, message: str, exc_info: Optional[Exception] = None, **kwargs) -> None:
        """Log error message with exception info"""
        if exc_info:
            self.logger.error(message, exc_info=exc_info, **kwargs)
        else:
            self.logger.error(message, **kwargs)

    def debug(self, message: str, **kwargs) -> None:
        """Log debug message"""
        self.logger.debug(message, **kwargs)

    def critical(self, message: str, exc_info: Optional[Exception] = None, **kwargs) -> None:
        """Log critical message with exception info"""
        if exc_info:
            self.logger.critical(message, exc_info=exc_info, **kwargs)
        else:
            self.logger.critical(message, **kwargs)

    def log_api_request(
        self,
        method: str,
        url: str,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        response: Optional[dict] = None,
        status_code: Optional[int] = None,
        duration: Optional[float] = None
    ) -> None:
        """Log API request details"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'method': method,
            'url': url,
            'params': params,
            'data': data,
            'response': response,
            'status_code': status_code,
            'duration': duration
        }
        
        self.info(f"API Request: {json.dumps(log_data)}")

    def log_error_event(
        self,
        error_type: str,
        error_message: str,
        stack_trace: Optional[str] = None,
        context: Optional[dict] = None
    ) -> None:
        """Log error event with context"""
        error_data = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type,
            'error_message': error_message,
            'stack_trace': stack_trace,
            'context': context
        }
        
        self.error(f"Error Event: {json.dumps(error_data)}")

    def log_user_action(
        self,
        user_id: str,
        action: str,
        details: Optional[dict] = None
    ) -> None:
        """Log user action with details"""
        action_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'action': action,
            'details': details
        }
        
        self.info(f"User Action: {json.dumps(action_data)}")

    def log_tax_calculation(
        self,
        user_id: str,
        calculation_type: str,
        inputs: dict,
        results: dict
    ) -> None:
        """Log tax calculation details"""
        calculation_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'calculation_type': calculation_type,
            'inputs': inputs,
            'results': results
        }
        
        self.info(f"Tax Calculation: {json.dumps(calculation_data)}")

    def get_log_file_path(self) -> Path:
        """Get path to current log file"""
        return self.log_dir / 'tax_sage.log'

    def get_archived_log_files(self) -> list:
        """Get list of archived log files"""
        return sorted(self.log_dir.glob('tax_sage.log.*'))

    def clear_logs(self) -> None:
        """Clear all log files"""
        for log_file in self.log_dir.glob('tax_sage.log*'):
            log_file.unlink()

    def set_log_level(self, level: int) -> None:
        """Set log level for all handlers"""
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)

    def add_file_handler(
        self,
        filename: str,
        level: int = logging.INFO,
        max_file_size: int = 10 * 1024 * 1024,
        backup_count: int = 5
    ) -> None:
        """Add additional file handler"""
        log_file = self.log_dir / filename
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

    def remove_file_handler(self, filename: str) -> None:
        """Remove file handler by filename"""
        for handler in self.logger.handlers:
            if isinstance(handler, logging.handlers.RotatingFileHandler):
                if handler.baseFilename == str(self.log_dir / filename):
                    self.logger.removeHandler(handler)
                    break 