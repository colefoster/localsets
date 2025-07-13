#!/usr/bin/env python3
"""
Example demonstrating the Smogon integration in the Pokemon data package.
"""

from localsets import PokemonData, get_smogon_sets, get_pokemon

def main():
    print("=== Pokemon Data Package - Smogon Integration Example ===\n")
    
    # Initialize with both RandBats and Smogon data
    data = PokemonData(
        randbats_formats=['gen9randombattle'],
        smogon_formats=['gen9ou', 'gen8ou']
    )
    
    print("1. RandBats Data (Random Battle)")
    print("-" * 40)
    
    # Get RandBats data
    pikachu_randbats = data.get_randbats('pikachu', 'gen9randombattle')
    if pikachu_randbats:
        print(f"Pikachu in gen9randombattle:")
        print(f"  Level: {pikachu_randbats.get('level', 'N/A')}")
        print(f"  Abilities: {', '.join(pikachu_randbats.get('abilities', []))}")
        print(f"  Items: {', '.join(pikachu_randbats.get('items', []))}")
        print(f"  Moves: {', '.join(pikachu_randbats.get('moves', []))}")
    else:
        print("Pikachu not found in gen9randombattle")
    
    print("\n2. Smogon Sets Data (Competitive)")
    print("-" * 40)
    
    # Get Smogon sets
    pikachu_sets = data.get_smogon_sets('pikachu', 'gen9ou')
    if pikachu_sets:
        print(f"Pikachu sets in gen9ou:")
        for set_name, set_data in pikachu_sets.items():
            print(f"\n  {set_name}:")
            print(f"    Item: {set_data.get('item', 'N/A')}")
            print(f"    Ability: {set_data.get('ability', 'N/A')}")
            print(f"    Nature: {set_data.get('nature', 'N/A')}")
            if 'evs' in set_data:
                evs = set_data['evs']
                ev_str = ', '.join([f"{stat}: {value}" for stat, value in evs.items()])
                print(f"    EVs: {ev_str}")
            print(f"    Moves: {', '.join(set_data.get('moves', []))}")
    else:
        print("Pikachu not found in gen9ou")
    
    print("\n3. Unified Search")
    print("-" * 40)
    
    # Search across both sources
    all_results = data.search_all('pikachu')
    
    if all_results.get('randbats'):
        print("RandBats results:")
        for format_name, pokemon_data in all_results['randbats'].items():
            print(f"  {format_name}: Found")
    
    if all_results.get('smogon'):
        print("Smogon results:")
        for format_name, sets_data in all_results['smogon'].items():
            set_count = len(sets_data)
            print(f"  {format_name}: {set_count} sets")
    
    print("\n4. Quick Access Functions")
    print("-" * 40)
    
    # Quick access to RandBats data
    quick_randbats = get_pokemon('pikachu', 'gen9randombattle')
    if quick_randbats:
        print("Quick RandBats access: Success")
    
    # Quick access to Smogon sets
    quick_smogon = get_smogon_sets('pikachu', 'gen9ou')
    if quick_smogon:
        print("Quick Smogon access: Success")
    
    print("\n5. Available Formats")
    print("-" * 40)
    
    all_formats = data.get_all_formats()
    print(f"RandBats formats: {len(all_formats['randbats'])}")
    print(f"Smogon formats: {len(all_formats['smogon'])}")
    
    print("\n=== Example Complete ===")

if __name__ == "__main__":
    main() 