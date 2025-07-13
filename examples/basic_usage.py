#!/usr/bin/env python3
"""
Basic usage example for localsets package.
"""

from localsets import RandBatsData, get_pokemon, list_pokemon

def main():
    """Demonstrate basic package usage."""
    print("Pokemon Random Battle Data - Basic Usage Example")
    print("=" * 50)
    
    # Initialize with specific formats
    print("\n1. Initializing PokemonData with specific formats...")
    data = RandBatsData(randbats_formats=['gen9randombattle', 'gen8randombattle'], auto_update=False)
    
    # Get available formats
    print(f"Available formats: {data.get_formats()}")
    
    # Get Pokemon data
    print("\n2. Getting Pokemon data...")
    pokemon_name = "pikachu"
    
    # Try to get Pokemon from different formats
    for format_name in data.get_formats():
        pokemon = data.get_pokemon(pokemon_name, format_name)
        if pokemon:
            print(f"Found {pokemon_name} in {format_name}")
            print(f"  Data keys: {list(pokemon.keys())}")
        else:
            print(f"{pokemon_name} not found in {format_name}")
    
    # List Pokemon in a format
    print("\n3. Listing Pokemon in gen9randombattle...")
    pokemon_list = data.list_pokemon('gen9randombattle')
    if pokemon_list:
        print(f"Found {len(pokemon_list)} Pokemon in gen9randombattle")
        print(f"First 10 Pokemon: {pokemon_list[:10]}")
    else:
        print("No Pokemon found in gen9randombattle")
    
    # Quick access functions
    print("\n4. Using quick access functions...")
    quick_pokemon = get_pokemon(pokemon_name)
    if quick_pokemon:
        print(f"Quick access found {pokemon_name}")
    else:
        print(f"Quick access did not find {pokemon_name}")
    
    # Cache information
    print("\n5. Cache information...")
    cache_info = data.get_cache_info()
    print(f"Cache directory: {cache_info['cache_dir']}")
    print(f"Loaded RandBats formats: {len(cache_info['randbats_formats'])}")
    print(f"Total RandBats Pokemon: {cache_info['total_randbats_pokemon']}")
    
    print("\nExample completed!")

if __name__ == "__main__":
    main() 