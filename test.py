import random
from Traveller.Models.subsector_system import Subsector_System as world
from Traveller import traveller_utils as utils
from GPT.dialogue_engine import DialogueSystem

# Testing traveller_utils and subsector_system
# for _ in range(1000):
#     print(f"\nGenerating Subsector {_+1}:\n")
#     for i in range (8):
#         if i+1 < 10:
#             x = f"0{i+1}"
#         else:
#             x = str(i+1)
#         for j in range (10):
#             if j+1 < 10:
#                 y = f"0{j+1}"
#             else:
#                 y = str(j+1)
            
#             if utils.d6() > 3:
#                 continue
#             new_world = world(location=f"{x}{y}")
#             new_world.generate_world()
#             print(new_world.to_string()) 

#Testing dialogue engine
system = DialogueSystem(scene_location = "Outside the city of Cornelia's main gate.", 
                        present_characters = ["Zen", "Merp", "Theo","Rupert"], 
                        scene_history="Prior to this moment, you were somewhere else. The power of the handheld dark crystal that you possessed, teleporting you here. Now you stand near 3 strangers whom also possess a handheld dark crystal, LIKE YOU.", scene_goal="Present are the 4 warriors of light, yet they do not know each other. They are introduce themselves to each other and discover that they have been chosen to be the 4 Warriors of Light by the dark crystals. Then they are to go and try to see the King of Cornelia, who is waiting for the 4 Warriors of Light to help with a great evil that is threatening the land.")
system.ask(character_name="Zen", user_input="You find yourself standing outside the city of Cornelia's main gate. You see 3 stranger's who are unknown to you. Your present goal is to go and meet the King of Cornelia. What do you think of the situation?")
system.ask(character_name="Theo")
system.ask(character_name="Rupert")
system.ask(character_name="Merp")
last_character = "Merp"
next_character = "Merp"
for x in range(6):
    while next_character == last_character:
        next_character = random.choice(system.engine.convo.present_characters) 
    system.ask(character_name=next_character)
    last_character = next_character
print("\n\nDialogue History:\n")
for message in system.engine.convo.messages:
    print(f"\n{message['role']}: {message['content']}")