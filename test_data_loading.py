#!/usr/bin/env python3
"""
Test script to verify data loading functionality.
"""

import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from localsets.core import PokemonData
from localsets.formats import RANDBATS_FORMATS

def test_data_loading():
    """Test data loading for all formats."""
    print("Testing data loading...")
    
    # Initialize PokemonData
    data = PokemonData()
    
    # Check which formats were loaded
    loaded_formats = data.get_randbats_formats()
    print(f"Loaded formats: {loaded_formats}")
    
    # Check data for each format
    for format_name in RANDBATS_FORMATS:
        pokemon_list = data.list_randbats_pokemon(format_name)
        print(f"{format_name}: {len(pokemon_list)} Pokemon")
        
        if len(pokemon_list) == 0:
            print(f"  WARNING: No Pokemon data for {format_name}")
        else:
            print(f"  Sample Pokemon: {pokemon_list[:3]}")

if __name__ == "__main__":
    test_data_loading() 