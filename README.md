# Pokemon Random Battle Data Package

A Python package providing offline access to Pokemon random battle data with automatic updates from the official source repository.

## Features

- **Offline Access**: Bundle data files within the package for immediate use
- **Auto-Updates**: Automatically check for updates every 24 hours (configurable)
- **Modular Installation**: Install only the generations/formats you need
- **Clean API**: Simple programmatic access to Pokemon data
- **Rich CLI**: Beautiful command-line interface with colored output
- **Multiple Formats**: Support for all Pokemon generations and battle formats
- **Graceful Fallbacks**: Robust error handling and network failure recovery

## Installation

### Full Installation (All Formats)
```bash
pip install localrandbats[all]
```

### Specific Generations
```bash
# Individual generations
pip install localrandbats[gen1,gen2,gen3]

# Classic generations (1-4)
pip install localrandbats[classic]

# Modern generations (8-9)
pip install localrandbats[modern]
```

### Specific Formats
```bash
# Doubles battle formats
pip install localrandbats[doubles]

# Let's Go format
pip install localrandbats[letsgo]

# Brilliant Diamond/Shining Pearl format
pip install localrandbats[bdsp]

# Baby Pokemon format
pip install localrandbats[baby]
```

## Quick Start

### Programmatic Usage

```python
from localrandbats import RandbatsData, get_pokemon

# Initialize with specific formats
data = RandbatsData(formats=['gen9randombattle', 'gen8randombattle'])

# Get Pokemon data
pikachu_gen9 = data.get_pokemon('pikachu', format='gen9randombattle')
pikachu_gen8 = data.get_pokemon('pikachu', format='gen8randombattle')

# List available Pokemon in format
pokemon_list = data.list_pokemon('gen9randombattle')

# Update data
data.update(formats=['gen9randombattle'])  # specific format
data.update_all()  # all installed formats

# Quick access functions
get_pokemon('pikachu', format='gen9randombattle')
```

### Command Line Interface

```bash
# Update data
localrandbats update
localrandbats update --format gen9randombattle
localrandbats update --all

# Pokemon lookup
localrandbats get pikachu
localrandbats get pikachu --format gen9randombattle
localrandbats get pikachu --format gen8randombattle

# List Pokemon
localrandbats list
localrandbats list --format gen9randombattle

# Package info
localrandbats info
localrandbats formats  # show installed formats
```

## Supported Formats

| Format | Generation | Type | Description |
|--------|------------|------|-------------|
| `gen1randombattle` | 1 | Singles | Generation 1 random battle |
| `gen2randombattle` | 2 | Singles | Generation 2 random battle |
| `gen3randombattle` | 3 | Singles | Generation 3 random battle |
| `gen4randombattle` | 4 | Singles | Generation 4 random battle |
| `gen5randombattle` | 5 | Singles | Generation 5 random battle |
| `gen6randombattle` | 6 | Singles | Generation 6 random battle |
| `gen7randombattle` | 7 | Singles | Generation 7 random battle |
| `gen7letsgorandombattle` | 7 | Let's Go | Let's Go Pikachu/Eevee format |
| `gen8randombattle` | 8 | Singles | Generation 8 random battle |
| `gen8bdsprandombattle` | 8 | BDSP | Brilliant Diamond/Shining Pearl |
| `gen8randomdoublesbattle` | 8 | Doubles | Generation 8 doubles battle |
| `gen9randombattle` | 9 | Singles | Generation 9 random battle |
| `gen9randomdoublesbattle` | 9 | Doubles | Generation 9 doubles battle |
| `gen9babyrandombattle` | 9 | Baby | Baby Pokemon format |

## Installation Extras

| Extra | Formats Included |
|-------|------------------|
| `gen1` | `gen1randombattle` |
| `gen2` | `gen2randombattle` |
| `gen3` | `gen3randombattle` |
| `gen4` | `gen4randombattle` |
| `gen5` | `gen5randombattle` |
| `gen6` | `gen6randombattle` |
| `gen7` | `gen7randombattle` |
| `gen8` | `gen8randombattle` |
| `gen9` | `gen9randombattle` |
| `classic` | `gen1randombattle`, `gen2randombattle`, `gen3randombattle`, `gen4randombattle` |
| `modern` | `gen8randombattle`, `gen9randombattle` |
| `doubles` | `gen8randomdoublesbattle`, `gen9randomdoublesbattle` |
| `letsgo` | `gen7letsgorandombattle` |
| `bdsp` | `gen8bdsprandombattle` |
| `baby` | `gen9babyrandombattle` |
| `all` | All formats |

## API Reference

### PokemonData Class

The main class for managing Pokemon random battle data.

#### Constructor
```python
PokemonData(formats=None, cache_dir=None, auto_update=True)
```

- `formats`: List of format names to load (default: all available)
- `cache_dir`: Directory to store cached data (default: system cache)
- `auto_update`: Whether to automatically check for updates (default: True)

#### Methods

- `get_pokemon(pokemon_name, format_name=None)`: Get Pokemon data
- `list_pokemon(format_name)`: List all Pokemon in a format
- `get_formats()`: Get list of available formats
- `update(formats=None)`: Update data for specific formats
- `update_all()`: Update data for all available formats
- `get_metadata(format_name)`: Get metadata for a format
- `get_cache_info()`: Get information about cached data

### Quick Access Functions

- `get_pokemon(pokemon_name, format_name=None)`: Quick Pokemon lookup
- `list_pokemon(format_name)`: Quick format listing
- `update_data(formats=None)`: Quick data update

## Configuration

The package uses a JSON configuration file located at `~/.cache/localrandbats/config.json`:

```json
{
    "update_interval_hours": 24,
    "enabled_formats": ["gen9randombattle", "gen8randombattle"],
    "auto_update": true,
    "cache_dir": "~/.cache/localrandbats"
}
```

## Data Sources

All data is sourced from the official [pkmn/randbats](https://github.com/pkmn/randbats) repository:

- **Raw Data**: `https://raw.githubusercontent.com/pkmn/randbats/main/data/`
- **API Metadata**: `https://api.github.com/repos/pkmn/randbats/contents/data`

## Caching

- **Cache Directory**: `~/.cache/localrandbats/` (configurable)
- **Data Files**: `{format_name}.json`
- **Metadata Files**: `{format_name}_metadata.json`
- **Update Tracking**: `last_update` timestamp file

## Error Handling

The package includes robust error handling:

- **Network Failures**: Graceful fallback to bundled data
- **Invalid JSON**: Skip corrupted files and continue
- **Missing Data**: Create empty data structures
- **Update Failures**: Continue with existing data

## Performance

- **Lazy Loading**: Only load requested formats into memory
- **Caching**: Store updated data locally for fast access
- **Efficient Updates**: Only download changed files
- **Memory Management**: Automatic cleanup of unused data

## Development

### Building from Source

```bash
git clone <repository>
cd localrandbats
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

### Building Package

```bash
python setup.py build
python setup.py sdist bdist_wheel
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Data sourced from [pkmn/randbats](https://github.com/pkmn/randbats)
- Built with Python 3.8+ compatibility
- Uses Click for CLI and Rich for beautiful output 
