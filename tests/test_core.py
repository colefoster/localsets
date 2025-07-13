"""
Tests for core PokemonData functionality.
"""

import pytest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

from pokemon_randbats.core import RandBatsData
from pokemon_randbats.formats import FORMATS


class TestPokemonData:
    """Test PokemonData class functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_init_default(self):
        """Test PokemonData initialization with defaults."""
        with patch('pokemon_randbats.core.user_cache_dir', return_value=self.temp_dir):
            data = RandBatsData(auto_update=False)
            assert data.formats == FORMATS
            assert data.cache_dir == Path(self.temp_dir)
            assert data.auto_update is False
    
    def test_init_custom_formats(self):
        """Test PokemonData initialization with custom formats."""
        custom_formats = ['gen9randombattle', 'gen8randombattle']
        with patch('pokemon_randbats.core.user_cache_dir', return_value=self.temp_dir):
            data = RandBatsData(formats=custom_formats, auto_update=False)
            assert data.formats == custom_formats
    
    def test_init_custom_cache_dir(self):
        """Test PokemonData initialization with custom cache directory."""
        custom_cache = Path(self.temp_dir) / "custom_cache"
        data = RandBatsData(cache_dir=str(custom_cache), auto_update=False)
        assert data.cache_dir == custom_cache
        assert custom_cache.exists()
    
    def test_normalize_name(self):
        """Test Pokemon name normalization."""
        data = RandBatsData(auto_update=False)
        
        # Test various name formats
        assert data._normalize_name("Pikachu") == "pikachu"
        assert data._normalize_name("Pikachu-EX") == "pikachuex"
        assert data._normalize_name("Mr. Mime") == "mrmime"
        assert data._normalize_name("Ho-Oh") == "hooh"
    
    def test_get_formats(self):
        """Test getting available formats."""
        data = RandBatsData(auto_update=False)
        formats = data.get_formats()
        assert isinstance(formats, list)
        assert len(formats) >= 0  # May be empty if no data loaded
    
    def test_get_cache_info(self):
        """Test getting cache information."""
        data = RandBatsData(auto_update=False)
        info = data.get_cache_info()
        
        assert 'cache_dir' in info
        assert 'loaded_formats' in info
        assert 'total_pokemon' in info
        assert 'format_counts' in info
        assert isinstance(info['cache_dir'], str)
        assert isinstance(info['loaded_formats'], list)
        assert isinstance(info['total_pokemon'], int)
        assert isinstance(info['format_counts'], dict)


class TestDataLoading:
    """Test data loading functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_load_format_from_cache(self):
        """Test loading format data from cache."""
        # Create mock cache data
        cache_file = self.cache_dir / "gen9randombattle.json"
        mock_data = {"pikachu": {"level": 50, "moves": ["thunderbolt"]}}
        
        with open(cache_file, 'w') as f:
            json.dump(mock_data, f)
        
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_format("gen9randombattle")
        
        assert "gen9randombattle" in data._data
        assert data._data["gen9randombattle"] == mock_data
    
    def test_load_format_from_bundled(self):
        """Test loading format data from bundled files."""
        # This test would require actual bundled data files
        # For now, just test that it doesn't crash
        data = RandBatsData(auto_update=False)
        data._load_format("gen9randombattle")
        
        # Should create empty data if no bundled file exists
        assert "gen9randombattle" in data._data
    
    def test_load_format_error_handling(self):
        """Test error handling during format loading."""
        # Create corrupted cache file
        cache_file = self.cache_dir / "gen9randombattle.json"
        with open(cache_file, 'w') as f:
            f.write("invalid json")
        
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_format("gen9randombattle")
        
        # Should create empty data on error
        assert "gen9randombattle" in data._data
        assert data._data["gen9randombattle"] == {}


class TestPokemonLookup:
    """Test Pokemon lookup functionality."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.cache_dir = Path(self.temp_dir)
        
        # Create mock data
        self.mock_data = {
            "gen9randombattle": {
                "pikachu": {"level": 50, "moves": ["thunderbolt", "quick attack"]},
                "charizard": {"level": 55, "moves": ["flamethrower", "dragon claw"]}
            }
        }
        
        # Write mock data to cache
        for format_name, data in self.mock_data.items():
            cache_file = self.cache_dir / f"{format_name}.json"
            with open(cache_file, 'w') as f:
                json.dump(data, f)
    
    def teardown_method(self):
        """Cleanup test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_get_pokemon_exact_match(self):
        """Test getting Pokemon with exact name match."""
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_format("gen9randombattle")
        
        pokemon = data.get_pokemon("pikachu", "gen9randombattle")
        assert pokemon is not None
        assert pokemon["level"] == 50
        assert "thunderbolt" in pokemon["moves"]
    
    def test_get_pokemon_case_insensitive(self):
        """Test getting Pokemon with case-insensitive matching."""
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_format("gen9randombattle")
        
        pokemon = data.get_pokemon("Pikachu", "gen9randombattle")
        assert pokemon is not None
        assert pokemon["level"] == 50
    
    def test_get_pokemon_not_found(self):
        """Test getting Pokemon that doesn't exist."""
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_format("gen9randombattle")
        
        pokemon = data.get_pokemon("nonexistent", "gen9randombattle")
        assert pokemon is None
    
    def test_get_pokemon_format_not_available(self):
        """Test getting Pokemon from unavailable format."""
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        
        pokemon = data.get_pokemon("pikachu", "nonexistent_format")
        assert pokemon is None
    
    def test_list_pokemon(self):
        """Test listing Pokemon in a format."""
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        data._load_format("gen9randombattle")
        
        pokemon_list = data.list_pokemon("gen9randombattle")
        assert isinstance(pokemon_list, list)
        assert "pikachu" in pokemon_list
        assert "charizard" in pokemon_list
        assert len(pokemon_list) == 2
    
    def test_list_pokemon_format_not_available(self):
        """Test listing Pokemon from unavailable format."""
        data = RandBatsData(cache_dir=str(self.cache_dir), auto_update=False)
        
        pokemon_list = data.list_pokemon("nonexistent_format")
        assert pokemon_list == [] 