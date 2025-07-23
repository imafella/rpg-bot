import random
def d6():
    """Roll a six-sided die."""
    return random.randint(1, 6)
def d3_roll():
    """Roll a three-sided die."""
    return random.randint(1, 3)

def load_json(file_path):
    """Load a JSON file."""
    import json
    with open(file_path, 'r') as file:
        return json.load(file)
    
_faction_strengths_cache = None
def get_faction_strength(strength:str):
    """Get faction strength from a predefined JSON configuration."""
    global _faction_strengths_cache
    if _faction_strengths_cache is None:
        _faction_strengths_cache = load_json('Traveller/Configs/faction_strength.json')
    return _faction_strengths_cache.get(strength, "Unknown strength")

_starport_cache = None
def get_starport_details():
    """Get starport details from a predefined JSON configuration."""
    global _starport_cache
    if _starport_cache is None:
        _starport_cache = load_json('Traveller/Configs/starport_details.json')
    return _starport_cache