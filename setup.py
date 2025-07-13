#!/usr/bin/env python3
"""
Setup script for pokemon-randbats package.
Includes custom build command to download latest data during package build.
"""

import os
import json
import shutil
import urllib.request
from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py
import zipfile
import tempfile

# Package metadata
PACKAGE_NAME = "pokemon-randbats"
VERSION = "0.1.0"
DESCRIPTION = "Offline Pokemon random battle data with auto-updates"
LONG_DESCRIPTION = """
A Python package providing offline access to Pokemon random battle data 
with automatic updates from the official source repository.
"""

# GitHub data source
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/pkmn/randbats/main/data"
GITHUB_API_BASE = "https://api.github.com/repos/pkmn/randbats/contents/data"

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

# Extras mapping
EXTRAS_REQUIRE = {
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


class DownloadDataCommand(Command):
    """Custom command to download data files during build."""
    
    description = "Download Pokemon random battle data files"
    user_options = []
    
    def initialize_options(self):
        pass
    
    def finalize_options(self):
        pass
    
    def run(self):
        """Download data files from GitHub."""
        print("Downloading Pokemon random battle data...")
        
        # Create data directory
        data_dir = os.path.join("pokemon_randbats", "data")
        metadata_dir = os.path.join("pokemon_randbats", "metadata")
        
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(metadata_dir, exist_ok=True)
        
        # Download each format
        for format_name in FORMATS:
            try:
                print(f"Downloading {format_name}.json...")
                
                # Download data file
                data_url = f"{GITHUB_RAW_BASE}/{format_name}.json"
                data_file = os.path.join(data_dir, f"{format_name}.json")
                
                with urllib.request.urlopen(data_url) as response:
                    with open(data_file, 'wb') as f:
                        f.write(response.read())
                
                # Get metadata from GitHub API
                metadata_url = f"{GITHUB_API_BASE}/{format_name}.json"
                with urllib.request.urlopen(metadata_url) as response:
                    metadata = json.loads(response.read().decode())
                
                # Save metadata
                metadata_file = os.path.join(metadata_dir, f"{format_name}_metadata.json")
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
                
                print(f"✓ Downloaded {format_name}.json")
                
            except Exception as e:
                print(f"✗ Failed to download {format_name}.json: {e}")
                # Create empty file as fallback
                data_file = os.path.join(data_dir, f"{format_name}.json")
                with open(data_file, 'w') as f:
                    json.dump({}, f)
        
        print("Data download complete!")


class BuildPyCommand(build_py):
    """Custom build command that includes data download."""
    
    def run(self):
        # Download data first
        self.run_command('download_data')
        # Then run normal build
        super().run()


setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Pokemon RandBats Team",
    author_email="",
    url="https://github.com/pkmn/randbats",
    packages=find_packages(include=['pokemon_randbats', 'pokemon_randbats.*']),
    include_package_data=True,
    package_data={
        'pokemon_randbats': [
            'data/*.json',
            'metadata/*.json',
        ],
    },
    install_requires=[
        'requests>=2.25.0',
        'click>=8.0.0',
        'rich>=10.0.0',
        'appdirs>=1.4.0',
    ],
    extras_require=EXTRAS_REQUIRE,
    entry_points={
        'console_scripts': [
            'pokemon-randbats=pokemon_randbats.cli:main',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'download_data': DownloadDataCommand,
        'build_py': BuildPyCommand,
    },
) 