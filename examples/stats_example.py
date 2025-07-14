#!/usr/bin/env python3
"""
Example script demonstrating the new stats functionality in localsets.

This script shows how to:
1. Load Pokemon data with stats
2. Retrieve stats for specific Pokemon
3. Get format-wide stats summaries
4. Analyze probability distributions
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from localsets import PokemonData

def main():
    print("=== Localsets Stats Functionality Demo ===\n")
    
    # Initialize PokemonData with stats support
    print("Initializing PokemonData...")
    pokemon_data = PokemonData(
        randbats_formats=['gen9randombattle', 'gen8randombattle'],
        auto_update=False  # Disable auto-update for demo
    )
    
    print(f"Loaded formats: {pokemon_data.get_randbats_formats()}\n")
    
    # Example 1: Get Pokemon data with stats
    print("1. Getting Pokemon data with stats:")
    pokemon_name = "Charizard"
    format_name = "gen9randombattle"
    
    result = pokemon_data.get_randbats_with_stats(pokemon_name, format_name)
    if result:
        data = result["data"]
        stats = result.get("stats", {})
        
        print(f"   Pokemon: {pokemon_name}")
        print(f"   Format: {format_name}")
        print(f"   Level: {data.get('level', 'N/A')}")
        
        # Show ability probabilities
        if 'abilities' in stats:
            print(f"   Abilities:")
            for ability, prob in stats['abilities'].items():
                print(f"     {ability}: {prob:.1%}")
        
        # Show item probabilities
        if 'items' in stats:
            print(f"   Items:")
            for item, prob in stats['items'].items():
                print(f"     {item}: {prob:.1%}")
        
        # Show role probabilities
        if 'roles' in stats:
            print(f"   Roles:")
            for role, role_data in stats['roles'].items():
                weight = role_data.get('weight', 1.0)
                print(f"     {role}: {weight:.1%}")
        
        print()
    
    # Example 2: Get stats summary for a format
    print("2. Format stats summary:")
    summary = pokemon_data.get_stats_summary(format_name)
    if summary:
        print(f"   Format: {summary['format']}")
        print(f"   Total Pokemon: {summary['total_pokemon']}")
        print(f"   Pokemon with stats: {summary['pokemon_with_stats']}")
        print(f"   Field coverage:")
        for field, count in summary['field_coverage'].items():
            percentage = (count / summary['total_pokemon']) * 100
            print(f"     {field}: {count}/{summary['total_pokemon']} ({percentage:.1f}%)")
        print()
    
    # Example 3: Analyze specific field probabilities
    print("3. Analyzing move probabilities for a Pokemon:")
    pokemon_name = "Pikachu"
    stats = pokemon_data.get_randbats_stats(pokemon_name, format_name)
    
    if stats and 'roles' in stats:
        print(f"   Pokemon: {pokemon_name}")
        for role_name, role_stats in stats['roles'].items():
            print(f"   Role: {role_name}")
            if 'moves' in role_stats:
                moves = role_stats['moves']
                # Sort moves by probability
                sorted_moves = sorted(moves.items(), key=lambda x: x[1], reverse=True)
                for move, prob in sorted_moves[:5]:  # Show top 5 moves
                    print(f"     {move}: {prob:.1%}")
            print()
    
    # Example 4: Compare two Pokemon's item usage
    print("4. Comparing item usage between Pokemon:")
    pokemon1, pokemon2 = "Blissey", "Chansey"
    
    for pokemon in [pokemon1, pokemon2]:
        stats = pokemon_data.get_randbats_stats(pokemon, format_name)
        if stats and 'items' in stats:
            print(f"   {pokemon} items:")
            items = stats['items']
            sorted_items = sorted(items.items(), key=lambda x: x[1], reverse=True)
            for item, prob in sorted_items:
                print(f"     {item}: {prob:.1%}")
            print()
    
    # Example 5: Find Pokemon with highest probability for specific items
    print("5. Finding Pokemon with highest Leftovers usage:")
    format_stats = pokemon_data.get_format_stats(format_name)
    if format_stats:
        leftovers_users = []
        for pokemon, pokemon_stats in format_stats.items():
            if 'items' in pokemon_stats and 'Leftovers' in pokemon_stats['items']:
                prob = pokemon_stats['items']['Leftovers']
                leftovers_users.append((pokemon, prob))
        
        # Sort by probability
        leftovers_users.sort(key=lambda x: x[1], reverse=True)
        print("   Top 10 Leftovers users:")
        for pokemon, prob in leftovers_users[:10]:
            print(f"     {pokemon}: {prob:.1%}")
        print()
    
    print("=== Demo Complete ===")

if __name__ == "__main__":
    main() 