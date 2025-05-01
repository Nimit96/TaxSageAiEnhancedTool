"""
File Handler Module
Contains functions for handling file operations
"""

import os
import shutil
import pandas as pd
from typing import Dict, List, Optional, Union
from pathlib import Path
import logging
from datetime import datetime
import json

class TaxFileHandler:
    def __init__(self, base_dir: str = 'tax_data'):
        """Initialize file handler with base directory"""
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save_dataframe(self, df: pd.DataFrame, filename: str, subdir: Optional[str] = None) -> bool:
        """Save DataFrame to file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if filename.endswith('.csv'):
                df.to_csv(file_path, index=False)
            elif filename.endswith('.xlsx'):
                df.to_excel(file_path, index=False)
            elif filename.endswith('.json'):
                df.to_json(file_path, orient='records')
            else:
                raise ValueError(f"Unsupported file format: {filename}")
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to save DataFrame: {str(e)}")
            return False

    def load_dataframe(self, filename: str, subdir: Optional[str] = None) -> Optional[pd.DataFrame]:
        """Load DataFrame from file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            if not file_path.exists():
                return None
                
            if filename.endswith('.csv'):
                return pd.read_csv(file_path)
            elif filename.endswith('.xlsx'):
                return pd.read_excel(file_path)
            elif filename.endswith('.json'):
                return pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file format: {filename}")
        except Exception as e:
            self.logger.error(f"Failed to load DataFrame: {str(e)}")
            return None

    def save_json(self, data: Union[Dict, List], filename: str, subdir: Optional[str] = None) -> bool:
        """Save data to JSON file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to save JSON: {str(e)}")
            return False

    def load_json(self, filename: str, subdir: Optional[str] = None) -> Optional[Union[Dict, List]]:
        """Load data from JSON file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            if not file_path.exists():
                return None
                
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load JSON: {str(e)}")
            return None

    def save_text(self, text: str, filename: str, subdir: Optional[str] = None) -> bool:
        """Save text to file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                f.write(text)
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to save text: {str(e)}")
            return False

    def load_text(self, filename: str, subdir: Optional[str] = None) -> Optional[str]:
        """Load text from file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            if not file_path.exists():
                return None
                
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to load text: {str(e)}")
            return None

    def list_files(self, subdir: Optional[str] = None, pattern: str = '*') -> List[str]:
        """List files in directory"""
        try:
            dir_path = self._get_dir_path(subdir)
            return [f.name for f in dir_path.glob(pattern)]
        except Exception as e:
            self.logger.error(f"Failed to list files: {str(e)}")
            return []

    def delete_file(self, filename: str, subdir: Optional[str] = None) -> bool:
        """Delete file"""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            if file_path.exists():
                file_path.unlink()
                
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete file: {str(e)}")
            return False

    def create_backup(self, backup_dir: str = 'backups') -> bool:
        """Create backup of data directory"""
        try:
            backup_path = Path(backup_dir)
            backup_path.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"tax_data_backup_{timestamp}"
            
            shutil.copytree(
                self.base_dir,
                backup_path / backup_name,
                dirs_exist_ok=True
            )
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to create backup: {str(e)}")
            return False

    def restore_backup(self, backup_name: str, backup_dir: str = 'backups') -> bool:
        """Restore data from backup"""
        try:
            backup_path = Path(backup_dir) / backup_name
            
            if not backup_path.exists():
                return False
                
            # Clear current data directory
            shutil.rmtree(self.base_dir)
            
            # Restore from backup
            shutil.copytree(backup_path, self.base_dir)
            
            return True
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {str(e)}")
            return False

    def _get_file_path(self, filename: str, subdir: Optional[str] = None) -> Path:
        """Get full file path"""
        if subdir:
            return self.base_dir / subdir / filename
        return self.base_dir / filename

    def _get_dir_path(self, subdir: Optional[str] = None) -> Path:
        """Get full directory path"""
        if subdir:
            return self.base_dir / subdir
        return self.base_dir

    def cleanup_old_files(self, days: int = 30) -> bool:
        """Clean up files older than specified days"""
        try:
            current_time = datetime.now()
            
            for file_path in self.base_dir.rglob('*'):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if (current_time - file_time).days > days:
                        file_path.unlink()
                        
            return True
        except Exception as e:
            self.logger.error(f"Failed to cleanup old files: {str(e)}")
            return False

    def get_file_size(self, filename: str, subdir: Optional[str] = None) -> Optional[int]:
        """Get file size in bytes"""
        try:
            file_path = self._get_file_path(filename, subdir)
            
            if file_path.exists():
                return file_path.stat().st_size
            return None
        except Exception as e:
            self.logger.error(f"Failed to get file size: {str(e)}")
            return None

    def get_directory_size(self, subdir: Optional[str] = None) -> int:
        """Get directory size in bytes"""
        try:
            dir_path = self._get_dir_path(subdir)
            return sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
        except Exception as e:
            self.logger.error(f"Failed to get directory size: {str(e)}")
            return 0 