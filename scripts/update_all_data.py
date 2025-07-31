import os
import json
import urllib.request
from pathlib import Path

GITHUB_RAW_BASE = "https://raw.githubusercontent.com/pkmn/randbats/main/data"
GITHUB_STATS_BASE = "https://raw.githubusercontent.com/pkmn/randbats/main/data/stats"
GITHUB_API_BASE = "https://api.github.com/repos/pkmn/randbats/contents/data"
SMOGON_BASE_URL = "https://pkmn.github.io/smogon/data/sets"

RANDBATS_FORMATS = [
    "gen1randombattle", "gen2randombattle", "gen3randombattle", "gen4randombattle", "gen5randombattle", "gen6randombattle",
    "gen7letsgorandombattle", "gen7randombattle", "gen8bdsprandombattle", "gen8randombattle", "gen8randomdoublesbattle",
    "gen9babyrandombattle", "gen9randombattle", "gen9randomdoublesbattle"
]

SMOGON_FORMATS = [
    "gen9ou", "gen9uu", "gen9ru", "gen9nu", "gen9pu", "gen9ubers", "gen9doublesou", "gen9vgc2024",
    "gen8ou", "gen8uu", "gen8ru", "gen8nu", "gen8pu", "gen8ubers", "gen8doublesou", "gen8vgc2022", "gen8vgc2023",
    "gen7ou", "gen7uu", "gen7ru", "gen7nu", "gen7pu", "gen7ubers", "gen7doublesou", "gen7vgc2017", "gen7vgc2018", "gen7vgc2019",
    "gen6ou", "gen6uu", "gen6ru", "gen6nu", "gen6pu", "gen6ubers", "gen6doublesou", "gen6vgc2014", "gen6vgc2015", "gen6vgc2016",
    "gen5ou", "gen5uu", "gen5ru", "gen5nu", "gen5pu", "gen5ubers", "gen5doublesou", "gen5vgc2011", "gen5vgc2012", "gen5vgc2013",
    "gen4ou", "gen4uu", "gen4nu", "gen4pu", "gen4ubers", "gen4doublesou", "gen4vgc2009", "gen4vgc2010",
    "gen3ou", "gen3uu", "gen3nu", "gen3pu", "gen3ubers", "gen3doublesou",
    "gen2ou", "gen2uu", "gen2nu", "gen2pu", "gen2ubers", "gen2doublesou",
    "gen1ou", "gen1uu", "gen1nu", "gen1pu", "gen1ubers", "gen1doublesou"
]

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def load_existing_data(file_path):
    """Load existing data from file if it exists, return empty dict if not"""
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"[WARN] Failed to load existing data from {file_path}: {e}")
    return {}

def download_randbats():
    data_dir = Path("localsets/randbattle_data")
    metadata_dir = Path("localsets/metadata")
    ensure_dir(data_dir)
    ensure_dir(metadata_dir)
    
    for format_name in RANDBATS_FORMATS:
        data_url = f"{GITHUB_RAW_BASE}/{format_name}.json"
        stats_url = f"{GITHUB_STATS_BASE}/{format_name}.json"
        data_file = data_dir / f"{format_name}.json"
        metadata_url = f"{GITHUB_API_BASE}/{format_name}.json"
        metadata_file = metadata_dir / f"{format_name}_metadata.json"
        
        # Load existing data as backup
        existing_data = load_existing_data(data_file)
        
        try:
            print(f"Downloading {format_name}.json...")
            
            # Download set data
            with urllib.request.urlopen(data_url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}: {response.reason}")
                set_data = json.loads(response.read().decode())
            
            # Download stats data (optional)
            try:
                with urllib.request.urlopen(stats_url) as stats_response:
                    if stats_response.status == 200:
                        stats_data = json.loads(stats_response.read().decode())
                        # Merge stats into each set
                        for poke, poke_stats in stats_data.items():
                            if poke in set_data:
                                set_data[poke]["stats"] = poke_stats
                        print(f"[OK] Downloaded stats for {format_name}")
                    else:
                        print(f"[WARN] Stats not available for {format_name} (HTTP {stats_response.status})")
            except Exception as stats_e:
                print(f"[WARN] No stats for {format_name}: {stats_e}")
            
            # Save merged data
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(set_data, f, indent=2)
            
            # Download and save metadata
            try:
                with urllib.request.urlopen(metadata_url) as response:
                    if response.status == 200:
                        metadata = json.loads(response.read().decode())
                        with open(metadata_file, 'w', encoding='utf-8') as f:
                            json.dump(metadata, f, indent=2)
                        print(f"[OK] Downloaded metadata for {format_name}")
                    else:
                        print(f"[WARN] Metadata not available for {format_name} (HTTP {response.status})")
            except Exception as metadata_e:
                print(f"[WARN] Failed to download metadata for {format_name}: {metadata_e}")
            
            print(f"[OK] Downloaded {format_name}.json")
            
        except Exception as e:
            print(f"[ERROR] Failed to download {format_name}.json: {e}")
            print(f"[INFO] Preserving existing data for {format_name}")
            
            # Only write empty data if we don't have existing data
            if not existing_data:
                print(f"[WARN] No existing data found for {format_name}, creating empty file")
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
            else:
                print(f"[INFO] Keeping existing data for {format_name} ({len(existing_data)} entries)")
                # Verify the existing data is still valid and not empty
                if len(existing_data) == 0:
                    print(f"[WARN] Existing data for {format_name} is empty, but keeping it to avoid data loss")

def download_smogon():
    smogon_data_dir = Path("localsets/smogon_data")
    ensure_dir(smogon_data_dir)
    for format_name in SMOGON_FORMATS:
        data_url = f"{SMOGON_BASE_URL}/{format_name}.json"
        data_file = smogon_data_dir / f"{format_name}.json"
        
        # Load existing data as backup
        existing_data = load_existing_data(data_file)
        
        try:
            print(f"Downloading {format_name}.json...")
            with urllib.request.urlopen(data_url) as response:
                if response.status == 200:
                    with open(data_file, 'wb') as f:
                        f.write(response.read())
                    print(f"[OK] Downloaded {format_name}.json")
                else:
                    print(f"[ERROR] {format_name}.json not available (HTTP {response.status})")
                    # Preserve existing data if download fails
                    if existing_data:
                        print(f"[INFO] Preserving existing data for {format_name} ({len(existing_data)} entries)")
                    else:
                        print(f"[WARN] No existing data found for {format_name}")
        except Exception as e:
            print(f"[ERROR] Failed to download {format_name}.json: {e}")
            # Preserve existing data if download fails
            if existing_data:
                print(f"[INFO] Preserving existing data for {format_name} ({len(existing_data)} entries)")
            else:
                print(f"[WARN] No existing data found for {format_name}")

def main():
    print("Starting data update process...")
    print("=" * 50)
    
    download_randbats()
    print("-" * 30)
    download_smogon()
    
    print("=" * 50)
    print("All data update complete!")
    
    # Print summary of updated files
    data_dir = Path("localsets/randbattle_data")
    smogon_dir = Path("localsets/smogon_data")
    
    if data_dir.exists():
        randbats_files = list(data_dir.glob("*.json"))
        print(f"Random Battle files: {len(randbats_files)}")
    
    if smogon_dir.exists():
        smogon_files = list(smogon_dir.glob("*.json"))
        print(f"Smogon files: {len(smogon_files)}")

if __name__ == "__main__":
    main() 