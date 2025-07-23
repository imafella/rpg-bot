
class character:
    def __init__(self, name:str = None, level: int = 1, class_name: str = None,  race: str = None):
        
        self.name = name
        self.level = level
        self.class_name = class_name
        self.race = race
        self.abilities = base_abilities()

    def display_info(self):
        return f"Character Name: {self.name}, Level: {self.level}"

    def level_up(self):
        self.level += 1
        return f"{self.name} has leveled up to level {self.level}!"
    
class base_abilities:
    ''' Base abilities for the character '''
    def __init__(self):
        self.vig = 0 # Vigor
        self.agi = 0 # Agility
        self.vit = 0 # Vitality
        self.mnd = 0 # Mind
        self.spr = 0 # Spirit
        self.psa = 0 # Persona


    def display_abilities(self):
        ''' Display the character's abilities as a string '''
        return f"Abilities: Vigor: {self.vig}, Agility: {self.agi}, Vitality: {self.vit}, Mind: {self.mnd}, Spirit: {self.spr}, Persona: {self.psa}"
