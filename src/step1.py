"""
DS4300 Homework 3 - Step 1
Shawn Tribuce

Fetches data for the first 151 Pokemon from the PokeAPI,
including their species and evolution chain information.
"""

import requests
import json
import time

OUTPUT_FILE = "pokemon.json"
TOTAL_POKEMON = 151  # Limit to avoid hitting API rate limits

# Fetch data from PokeAPI for a given Pokemon ID
def get_pokemon(pokemon_id):
    resp = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    resp.raise_for_status() # Raise an error for failed requests
    return resp.json()

# Fetch species data for each Pokemon
def get_species(pokemon_id):
    resp = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}")
    resp.raise_for_status() # Raise an error for failed requests
    return resp.json()

# Fetch the evolution chain data using the URL from the species endpoint
def get_evolution_chain(url):
    resp = requests.get(url)
    resp.raise_for_status() # Raise an error for failed requests
    return resp.json()

# Structured the evolution chain data into a clean nested format
def parse_evolution_chain(chain):
    result = {
        "species": chain["species"]["name"], # The first stage of evolution
        "evolves_to": [parse_evolution_chain(e) for e in chain["evolves_to"]] # Final stage of evolution
    }
    return result
# Build a clean Pokemon document with all the relevant fields and nested structures for MondongoDB
def build_pokemon(raw, species, evo_chain):
    return {
        "pokemon_id":      raw["id"],
        "name":            raw["name"],
        "base_experience": raw["base_experience"],
        "height":          raw["height"],
        "weight":          raw["weight"],

        # Array of types of Pokemon
        "types": [
            t["type"]["name"] for t in raw["types"]
        ],

        # Ability objects for each Pokemon
        "abilities": [
            {
                "name":      a["ability"]["name"],
                "is_hidden": a["is_hidden"]
            }
            for a in raw["abilities"]
        ],

        # Base stats for each Pokemon in a dictionary format
        "stats": {
            s["stat"]["name"]: s["base_stat"] for s in raw["stats"]
        },

        "sprite": raw["sprites"]["front_default"],

        # Category and other metadata from the species endpoint
        "generation":   species["generation"]["name"],
        "is_legendary": species["is_legendary"],
        "is_mythical":  species["is_mythical"],
        "habitat":      species["habitat"]["name"] if species["habitat"] else None,
        "growth_rate":  species["growth_rate"]["name"],
        "capture_rate": species["capture_rate"],

        # Evolution chain
        "evolution_chain": evo_chain,
    }

# Main function to fetch data for the first 151 Pokemon and save to JSON
def fetch():
    pokemon_list = []

    # Loop through the first 151 Pokemon, fetch their data, and build structured documents
    for i in range(1, TOTAL_POKEMON + 1):
        try:
            raw     = get_pokemon(i)
            species = get_species(i)
            evo_url = species["evolution_chain"]["url"]
            evo_raw = get_evolution_chain(evo_url)
            evo     = parse_evolution_chain(evo_raw["chain"])

            document = build_pokemon(raw, species, evo) # Build a clean document for MongoDB
            pokemon_list.append(document)

            time.sleep(0.1)  # Sleep to avoid hitting API rate limits (100 requests per 60 seconds)

        # Handle any HTTP errors
        except requests.HTTPError as e:
            print(f"Error for Pokemon {i}: {e}")
            continue # Skip to the next Pokemon if there's an error
    # Save the list of Pokemon to a JSON file with pretty formatting for MongoDB import
    with open(OUTPUT_FILE, "w") as f:
        json.dump(pokemon_list, f)

    print(f"Pokemon saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    fetch()