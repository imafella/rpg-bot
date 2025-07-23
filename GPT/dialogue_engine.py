import os
import openai
from openai import *
from GPT.Models.conversation import conversation
import GPT.util as utils
import logging

# Character system message templates (minimal and reusable)
character_configs = {
    "Zen": "Expert_Zen",
    "Theo": "Warrior_Theo",
    "Merp": "Adept_Merp",
    "Rupert": "Mage_Rupert",
}

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more detail
    format='%(asctime)s %(levelname)s %(name)s %(message)s' 
)

class DialogueSceneEngine:
    def __init__(self, scene_history:str = None, scene_goal:str = None):
        openai.api_key = os.environ.get("gpt_api_key")
        self.model = os.environ.get("gpt_model")
        self.convo = conversation(max_history_length=int(os.environ.get("max_msg_length", 8)))
        self.scene_history = scene_history
        self.scene_goal = scene_goal
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)


    def generate_character_instructions(self, character: str) -> str:
        character_config = utils.load_character_config(character_configs[character])

        name = character_config["name"]
        pronouns = character_config["pronouns"]
        role = character_config["occupation_or_role"]
        personality = character_config.get("personality", {})
        appearance = character_config.get("appearance", {})
        background = character_config.get("background", {})
        
        # Build the instructions string
        instructions = f"""You are roleplaying as the following character. Stay fully in character in all responses. If at any time you wish to do an action as a character, state what you want to do. The results of the action attempt will be provided to you later.

Name: {name}
Pronouns: {pronouns}
Race: {character_config['race']}
Gender: {character_config['gender']}
Age: {character_config['age']}
Homeland: {character_config['homeland']}
Occupation: {role}
Social Class: {character_config['social_class']}

Appearance:
- Height: {appearance.get("height", "Unknown")}
- Build: {appearance.get("build", "Unknown")}
- Hair: {appearance.get("hair", "Unknown")}
- Eyes: {appearance.get("eyes", "Unknown")}
- Notable Features: {', '.join(appearance.get("notable_features", []))}

Personality:
- Traits: {', '.join(personality.get("traits", []))}
- Ideals: {', '.join(personality.get("ideals", []))}
- Flaws: {', '.join(personality.get("flaws", []))}
- Bond: {personality.get("bond", "N/A")}
- Motivation: {personality.get("motivation", "N/A")}

Background:
- Origin: {background.get("origin_story", "N/A")}
- Family: {', '.join(background.get("family", []))}
- Notable Events: {', '.join(background.get("notable_events", []))}
- Current Goal: {background.get("current_goal", "N/A")}

Likes: {', '.join(character_config.get("likes", []))}
Dislikes: {', '.join(character_config.get("dislikes", []))}
Fears: {', '.join(character_config.get("fears", []))}
Hobbies: {', '.join(character_config.get("hobbies", []))}

Beliefs: {character_config.get("religion_or_beliefs", "N/A")}
Languages: {', '.join(character_config.get("languages", []))}

Relationships:
- Allies: {', '.join(character_config["relationships"].get("allies", []))}
- Rivals: {', '.join(character_config["relationships"].get("rivals", []))}
- Romantic Interest: {character_config["relationships"].get("romantic_interest", "N/A")}

Inventory: {', '.join(character_config.get("inventory", []))}
Companions: {', '.join(character_config.get("pets_or_companions", []))}
Secrets: {', '.join(character_config.get("secrets", []))}
Common Quotes: {', '.join(character_config.get("quotes", []))}

TTRPG Details:
- Class: {character_config["rpg_details"].get("class", "N/A")}
- Jobs: {', '.join(character_config["rpg_details"].get("jobs", []))}

Respond to any user prompts as if you were {name}, using their voice, tone, and perspective. 
You are allowed to talk or take an action in character—but do not break character under any circumstance. 
You have no control over anything other than this character.

Do not make any assumptions or make things up. 
Stay in character. Respond briefly (1-2 sentences). Do not repeat yourself.

You are not a narrator, you are a character.
You also do not always need to respond to every user prompt. It is ok to just nod your head or shrug your shoulders, or even just say "I don't know" if you don't have an answer.
You are a real character, so act like one.
"""
        return instructions


    def generate_input_for_response(self,basic_prompt:str = None) -> str:
        # Generate the input prompt for the OpenAI API
        input = f"""
Location: {self.convo.location if self.convo.location else "No location provided."}
Characters: {', '.join(self.convo.present_characters)}
Description: {self.scene_history if self.scene_history else "No scene description provided."}
Goal: {self.scene_goal if self.scene_goal else "No scene goal provided."}
Recent: {"\n".join(self.convo.get_messsage_contents())}\n
{'basic_prompt' if basic_prompt else 'Respond to the situation at hand.'}
"""
        return input.strip()

    def get_character_response(self, character_name:str, response_prompt:str = None) -> str:

        instructions = self.generate_character_instructions(character_name)
        input = self.generate_input_for_response(basic_prompt=response_prompt)
        response = openai.responses.create(
            model=self.model,
            instructions=instructions,
            input=input,   
            temperature=0.6,
            max_output_tokens=200
        )

        self.logger.info(msg=f"\nInstructions for {character_name}: {instructions}\nInput: {input}\nResponse: {response.output_text.strip()}")
        return response.output_text.strip()


class DialogueSystem:
    def __init__(self, scene_location:str = None, present_characters:list = [], scene_history:str = None, scene_goal:str = None):
        self.engine = DialogueSceneEngine(scene_goal=scene_goal, scene_history=scene_history)
        self.engine.convo.location = scene_location
        self.engine.convo.present_characters = present_characters
        self.scene_history = scene_history
        self.scene_goal = scene_goal

    def ask(self, character_name:str, user_input:str = None) -> str:
        response = self.engine.get_character_response(character_name, user_input)
        self.engine.convo.add_message(role='user', content=f"{character_name}: {response}")
        return f"\n{character_name}:\n {response}"
    
    def change_location(self, new_location):
        self.engine.convo.location = new_location
        self.engine.convo.add_message(role='system', content=f"The scene has transitioned to a new location: {new_location}")
        return f"Location changed to: {new_location}"
    
    def add_character(self, character_name):
        if character_name not in self.engine.convo.present_characters:
            self.engine.convo.present_characters.append(character_name)
            self.engine.convo.add_message(role='system', content=f"{character_name} has joined the scene.")
            return f"{character_name} has been added to the scene."
        return f"{character_name} is already present in the scene."
    
    def remove_character(self, character_name):
        if character_name in self.engine.convo.present_characters:
            self.engine.convo.present_characters.remove(character_name)
            self.engine.convo.add_message(role='system', content=f"{character_name} has left the scene.")
            return f"{character_name} has been removed from the scene."
        return f"{character_name} is not present in the scene."


# === Example usage ===
# system = DialogueSystem(scene_location = "next to a merchant's stall", present_characters = ["Bill", "Ted", "Merchant"])
# print(system.ask("Zen", "What do you think of the merchant with the glowing staff?"))
