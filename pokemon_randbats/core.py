"""
Core PokemonData class for managing Pokemon random battle data.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import requests
from appdirs import user_cache_dir

from .updater import DataUpdater
from .formats import FORMATS, FORMAT_MAPPINGS

logger = logging.getLogger(__name__)


class RandBatsData:
    """
    Main class for managing Pokemon random battle data.
    
    Provides methods to load, cache, and update Pokemon data from various
    battle formats and generations.
    """
    
    def __init__(self, formats: Optional[List[str]] = None, 
                 cache_dir: Optional[str] = None,
                 auto_update: bool = True):
        """
        Initialize PokemonData instance.
        
        Args:
            formats: List of format names to load. If None, loads all available.
            cache_dir: Directory to store cached data. If None, uses default.
            auto_update: Whether to automatically check for updates.
        """
        self.formats = formats or FORMATS
        self.cache_dir = Path(cache_dir or user_cache_dir('pokemon-randbats'))
        self.auto_update = auto_update
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Data storage
        self._data: Dict[str, Dict] = {}
        self._metadata: Dict[str, Dict] = {}
        self._loaded_formats: set = set()
        
        # Initialize updater
        self.updater = DataUpdater(self.cache_dir)
        
        # Load data
        self._load_data()
        
        # Auto-update if enabled
        if self.auto_update:
            self._check_updates()
    
    def _load_data(self):
        """Load data for all specified formats."""
        for format_name in self.formats:
            if format_name not in self._loaded_formats:
                self._load_format(format_name)
    
    def _load_format(self, format_name: str):
        """Load data for a specific format."""
        try:
            # Try cache first
            cache_file = self.cache_dir / f"{format_name}.json"
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self._data[format_name] = json.load(f)
                self._loaded_formats.add(format_name)
                logger.debug(f"Loaded {format_name} from cache")
                return
            
            # Fall back to bundled data
            bundled_file = Path(__file__).parent / "data" / f"{format_name}.json"
            if bundled_file.exists():
                with open(bundled_file, 'r', encoding='utf-8') as f:
                    self._data[format_name] = json.load(f)
                self._loaded_formats.add(format_name)
                logger.debug(f"Loaded {format_name} from bundled data")
                return
            
            # Create empty data if nothing available
            self._data[format_name] = {}
            self._loaded_formats.add(format_name)
            logger.warning(f"No data available for {format_name}")
            
        except Exception as e:
            logger.error(f"Failed to load {format_name}: {e}")
            self._data[format_name] = {}
            self._loaded_formats.add(format_name)
    
    def _check_updates(self):
        """Check for updates if needed."""
        try:
            # Check if update is needed (24 hour interval)
            last_update_file = self.cache_dir / "last_update"
            if last_update_file.exists():
                with open(last_update_file, 'r') as f:
                    last_update = datetime.fromisoformat(f.read().strip())
                if datetime.now() - last_update < timedelta(hours=24):
                    return  # No update needed
            
            # Perform update
            self.update_all()
            
        except Exception as e:
            logger.warning(f"Auto-update check failed: {e}")
    
    def get_pokemon(self, pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get Pokemon data for a specific Pokemon and format.
        
        Args:
            pokemon_name: Name of the Pokemon (case-insensitive)
            format_name: Battle format. If None, tries to auto-detect.
            
        Returns:
            Pokemon data dictionary or None if not found
        """
        if format_name is None:
            format_name = self._detect_format(pokemon_name)
        
        if format_name not in self._data:
            logger.warning(f"Format {format_name} not available")
            return None
        
        # Normalize Pokemon name
        pokemon_name = self._normalize_name(pokemon_name)
        
        # Search in format data
        format_data = self._data[format_name]
        if pokemon_name in format_data:
            return format_data[pokemon_name]
        
        # Try fuzzy matching
        for key in format_data.keys():
            if self._normalize_name(key) == pokemon_name:
                return format_data[key]
        
        return None
    
    def list_pokemon(self, format_name: str) -> List[str]:
        """
        List all Pokemon available in a specific format.
        
        Args:
            format_name: Battle format name
            
        Returns:
            List of Pokemon names
        """
        if format_name not in self._data:
            logger.warning(f"Format {format_name} not available")
            return []
        
        return list(self._data[format_name].keys())
    
    def get_formats(self) -> List[str]:
        """Get list of available formats."""
        return list(self._loaded_formats)
    
    def update(self, formats: Optional[List[str]] = None):
        """
        Update data for specific formats.
        
        Args:
            formats: List of formats to update. If None, updates all loaded formats.
        """
        formats_to_update = formats or list(self._loaded_formats)
        
        try:
            updated_formats = self.updater.update_formats(formats_to_update)
            
            # Reload updated formats
            for format_name in updated_formats:
                if format_name in self._loaded_formats:
                    self._load_format(format_name)
            
            # Update last update timestamp
            last_update_file = self.cache_dir / "last_update"
            with open(last_update_file, 'w') as f:
                f.write(datetime.now().isoformat())
            
            logger.info(f"Updated {len(updated_formats)} formats")
            
        except Exception as e:
            logger.error(f"Update failed: {e}")
    
    def update_all(self):
        """Update data for all available formats."""
        self.update(FORMATS)
    
    def _detect_format(self, pokemon_name: str) -> str:
        """
        Auto-detect the best format for a Pokemon.
        
        Args:
            pokemon_name: Name of the Pokemon
            
        Returns:
            Best matching format name
        """
        # Simple heuristic: try most recent formats first
        recent_formats = ['gen9randombattle', 'gen8randombattle', 'gen7randombattle']
        
        for format_name in recent_formats:
            if format_name in self._data:
                pokemon_data = self.get_pokemon(pokemon_name, format_name)
                if pokemon_data:
                    return format_name
        
        # Fall back to first available format
        return next(iter(self._loaded_formats), 'gen9randombattle')
    
    def _normalize_name(self, name: str) -> str:
        """
        Normalize Pokemon name for comparison.
        
        Args:
            name: Pokemon name
            
        Returns:
            Normalized name
        """
        # Remove all non-alphanumeric characters
        return ''.join(c for c in name.lower() if c.isalnum())
    
    def get_metadata(self, format_name: str) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific format.
        
        Args:
            format_name: Battle format name
            
        Returns:
            Metadata dictionary or None
        """
        try:
            metadata_file = self.cache_dir / f"{format_name}_metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    return json.load(f)
            
            # Try bundled metadata
            bundled_metadata = Path(__file__).parent / "metadata" / f"{format_name}_metadata.json"
            if bundled_metadata.exists():
                with open(bundled_metadata, 'r') as f:
                    return json.load(f)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to load metadata for {format_name}: {e}")
            return None
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about cached data.
        
        Returns:
            Dictionary with cache information
        """
        info = {
            'cache_dir': str(self.cache_dir),
            'loaded_formats': list(self._loaded_formats),
            'total_pokemon': sum(len(data) for data in self._data.values()),
            'format_counts': {fmt: len(data) for fmt, data in self._data.items()}
        }
        
        # Add last update info
        last_update_file = self.cache_dir / "last_update"
        if last_update_file.exists():
            with open(last_update_file, 'r') as f:
                info['last_update'] = f.read().strip()
        
        return info 