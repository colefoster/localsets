#!/usr/bin/env python3
"""
Comprehensive example demonstrating both RandBats and Smogon integration.
"""

from localsets import PokemonData, get_pokemon, get_smogon_sets

def main():
    """Demonstrate comprehensive package usage."""
    print("Pokemon Data Package - Comprehensive Example")
    print("=" * 50)
    
    # Initialize Pokemon data with both RandBats and Smogon
    print("\n1. RandBats Data (Random Battle)")
    print("-" * 30)
    data = PokemonData(randbats_formats=['gen9randombattle'], smogon_formats=['gen9ou'], auto_update=False)
    
    # Get Pokemon from RandBats
    pokemon_name = "pikachu"
    randbats_pokemon = data.get_randbats(pokemon_name, 'gen9randombattle')
    if randbats_pokemon:
        print(f"Found {pokemon_name} in gen9randombattle:")
        print(f"  Level: {randbats_pokemon.get('level', 'N/A')}")
        print(f"  Abilities: {', '.join(randbats_pokemon.get('abilities', []))}")
        print(f"  Items: {', '.join(randbats_pokemon.get('items', []))}")
        print(f"  Moves: {', '.join(randbats_pokemon.get('moves', []))}")
    
    # Quick access to RandBats
    quick_randbats = get_pokemon(pokemon_name)
    if quick_randbats:
        print(f"Quick access: Found {pokemon_name}")
    
    print("\n2. Smogon Sets Data (Competitive)")
    print("-" * 30)
    
    # Get Smogon competitive sets
    smogon_sets = data.get_smogon_sets(pokemon_name, 'gen9ou')
    if smogon_sets:
        print(f"Found {len(smogon_sets)} competitive sets for {pokemon_name}:")
        for set_name, set_data in list(smogon_sets.items())[:2]:  # Show first 2 sets
            print(f"\n  {set_name}:")
            print(f"    Item: {set_data.get('item', 'N/A')}")
            print(f"    Ability: {set_data.get('ability', 'N/A')}")
            print(f"    Nature: {set_data.get('nature', 'N/A')}")
            if 'evs' in set_data:
                evs = set_data['evs']
                ev_str = ', '.join([f"{stat}: {value}" for stat, value in evs.items()])
                print(f"    EVs: {ev_str}")
            print(f"    Moves: {', '.join(set_data.get('moves', []))}")
    
    print("\n3. Package Information")
    print("-" * 30)
    
    # Cache and format information
    cache_info = data.get_cache_info()
    print(f"Cache directory: {cache_info['cache_dir']}")
    print(f"RandBats formats: {len(cache_info['randbats_formats'])}")
    print(f"Smogon formats: {len(cache_info['smogon_formats'])}")
    print(f"Total RandBats Pokemon: {cache_info['total_randbats_pokemon']}")
    
    # List available Pokemon
    pokemon_list = data.list_randbats_pokemon('gen9randombattle')
    if pokemon_list:
        print(f"Available Pokemon in gen9randombattle: {len(pokemon_list)}")
        print(f"Sample: {pokemon_list[:5]}")
    
    print("\nExample completed!")

if __name__ == "__main__":
    main() 