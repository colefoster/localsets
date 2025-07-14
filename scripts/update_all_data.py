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
        try:
            print(f"Downloading {format_name}.json...")
            # Download set data
            with urllib.request.urlopen(data_url) as response:
                set_data = json.loads(response.read().decode())
            # Download stats data (optional)
            try:
                with urllib.request.urlopen(stats_url) as stats_response:
                    stats_data = json.loads(stats_response.read().decode())
                # Merge stats into each set
                for poke, poke_stats in stats_data.items():
                    if poke in set_data:
                        set_data[poke]["stats"] = poke_stats
                print(f"[OK] Downloaded stats for {format_name}")
            except Exception as stats_e:
                print(f"[WARN] No stats for {format_name}: {stats_e}")
            # Save merged data
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(set_data, f, indent=2)
            # Download and save metadata
            with urllib.request.urlopen(metadata_url) as response:
                metadata = json.loads(response.read().decode())
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2)
            print(f"[OK] Downloaded {format_name}.json")
        except Exception as e:
            print(f"[ERROR] Failed to download {format_name}.json: {e}")
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump({}, f)

def download_smogon():
    smogon_data_dir = Path("localsets/smogon_data")
    ensure_dir(smogon_data_dir)
    for format_name in SMOGON_FORMATS:
        try:
            print(f"Downloading {format_name}.json...")
            data_url = f"{SMOGON_BASE_URL}/{format_name}.json"
            data_file = smogon_data_dir / f"{format_name}.json"
            with urllib.request.urlopen(data_url) as response:
                if response.status == 200:
                    with open(data_file, 'wb') as f:
                        f.write(response.read())
                    print(f"[OK] Downloaded {format_name}.json")
                else:
                    print(f"[ERROR] {format_name}.json not available (404)")
        except Exception as e:
            print(f"[ERROR] Failed to download {format_name}.json: {e}")

def main():
    download_randbats()
    download_smogon()
    print("All data update complete!")

if __name__ == "__main__":
    main() 