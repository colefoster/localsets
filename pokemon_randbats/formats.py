"""
Format definitions and utility functions for Pokemon random battle data.
"""

from typing import Dict, List, Optional, Any

# Available formats
FORMATS = [
    "gen1randombattle",
    "gen2randombattle", 
    "gen3randombattle",
    "gen4randombattle",
    "gen5randombattle",
    "gen6randombattle",
    "gen7letsgorandombattle",
    "gen7randombattle",
    "gen8bdsprandombattle",
    "gen8randombattle",
    "gen8randomdoublesbattle",
    "gen9babyrandombattle",
    "gen9randombattle",
    "gen9randomdoublesbattle"
]

# Format mappings for extras
FORMAT_MAPPINGS = {
    'gen1': ['gen1randombattle'],
    'gen2': ['gen2randombattle'],
    'gen3': ['gen3randombattle'],
    'gen4': ['gen4randombattle'],
    'gen5': ['gen5randombattle'],
    'gen6': ['gen6randombattle'],
    'gen7': ['gen7randombattle'],
    'gen8': ['gen8randombattle'],
    'gen9': ['gen9randombattle'],
    'classic': ['gen1randombattle', 'gen2randombattle', 'gen3randombattle', 'gen4randombattle'],
    'modern': ['gen8randombattle', 'gen9randombattle'],
    'doubles': ['gen8randomdoublesbattle', 'gen9randomdoublesbattle'],
    'letsgo': ['gen7letsgorandombattle'],
    'bdsp': ['gen8bdsprandombattle'],
    'baby': ['gen9babyrandombattle'],
    'all': FORMATS
}

# Global PokemonData instance for quick access functions
_global_data = None


def _get_global_data():
    """Get or create global PokemonData instance."""
    global _global_data
    if _global_data is None:
        # Import here to avoid circular import
        from .core import RandBatsData
        _global_data = RandBatsData()
    return _global_data


def get_pokemon(pokemon_name: str, format_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Quick access function to get Pokemon data.
    
    Args:
        pokemon_name: Name of the Pokemon
        format_name: Battle format (optional)
        
    Returns:
        Pokemon data dictionary or None
    """
    data = _get_global_data()
    return data.get_pokemon(pokemon_name, format_name)


def list_pokemon(format_name: str) -> List[str]:
    """
    Quick access function to list Pokemon in a format.
    
    Args:
        format_name: Battle format name
        
    Returns:
        List of Pokemon names
    """
    data = _get_global_data()
    return data.list_pokemon(format_name)


def update_data(formats: Optional[List[str]] = None):
    """
    Quick access function to update data.
    
    Args:
        formats: List of formats to update (optional)
    """
    data = _get_global_data()
    data.update(formats)


def get_available_formats() -> List[str]:
    """
    Get list of all available formats.
    
    Returns:
        List of format names
    """
    return FORMATS.copy()


def get_format_mappings() -> Dict[str, List[str]]:
    """
    Get format mappings for extras.
    
    Returns:
        Dictionary mapping extra names to format lists
    """
    return FORMAT_MAPPINGS.copy()


def resolve_formats(formats: List[str]) -> List[str]:
    """
    Resolve format aliases to actual format names.
    
    Args:
        formats: List of format names or aliases
        
    Returns:
        List of resolved format names
    """
    resolved = []
    for fmt in formats:
        if fmt in FORMAT_MAPPINGS:
            resolved.extend(FORMAT_MAPPINGS[fmt])
        elif fmt in FORMATS:
            resolved.append(fmt)
        else:
            # Unknown format, skip
            continue
    return list(set(resolved))  # Remove duplicates


def get_format_info(format_name: str) -> Dict[str, Any]:
    """
    Get information about a specific format.
    
    Args:
        format_name: Battle format name
        
    Returns:
        Dictionary with format information
    """
    if format_name not in FORMATS:
        return {}
    
    info = {
        'name': format_name,
        'generation': _extract_generation(format_name),
        'type': _extract_type(format_name),
        'available': True
    }
    
    # Add Pokemon count if data is loaded
    data = _get_global_data()
    if format_name in data._data:
        info['pokemon_count'] = len(data._data[format_name])
    
    return info


def _extract_generation(format_name: str) -> str:
    """Extract generation from format name."""
    if format_name.startswith('gen'):
        return format_name[3:4]  # gen1 -> 1, gen9 -> 9
    return 'unknown'


def _extract_type(format_name: str) -> str:
    """Extract battle type from format name."""
    if 'doubles' in format_name:
        return 'doubles'
    elif 'letsgo' in format_name:
        return 'letsgo'
    elif 'bdsp' in format_name:
        return 'bdsp'
    elif 'baby' in format_name:
        return 'baby'
    else:
        return 'singles' 