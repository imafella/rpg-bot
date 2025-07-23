
def load_character_config(character: str) -> dict:
    """
    Load character configuration from a JSON file.
    
    Args:
        character (str): The name of the character.
        
    Returns:
        dict: The character configuration.
    """
    import json
    import os

    config_path = os.path.join(os.path.dirname(__file__), 'character_configs', f'{character}.json')
    
    with open(config_path, 'r') as file:
        return json.load(file)