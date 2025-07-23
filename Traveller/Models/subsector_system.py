from Traveller import traveller_utils as utils
class Subsector_System:

    
    def __init__(self, location:str = None):
        self.name  = None
        self.location = location
        self.starport = None
        self.size  = None
        self.atmosphere  = None
        self.temperature  = None
        self.hydrographics  = None
        self.population  = None
        self.government  = None
        self.factions = []
        self.cultural_differences = None
        self.law_level  = None
        self.tech_level  = None
        self.bases = []
        self.alert_level = None
        self.trade_codes = []

    def __repr__(self):
        return f"Subsector_System(name={self.name}, hex_code={self.hex_code})"
    
    def generate_world(self):
        ''' Generate a world with random attributes '''
        # Generate size of world
        self.size = utils.d6()+utils.d6() - 2
        
        # Generate Atmosphere of world
        self.atmosphere = utils.d6() + utils.d6() - 7 + self.size
        if self.atmosphere < 0:
            self.atmosphere = 0

        # Generate Temperature of world
        atmosphere_mods = {
            (2, 3): -2,
            (4, 5, 14): -1,
            (8, 9): 1,
            (10, 13, 15): 2,
            (11, 12): 6,
        }
        mod = 0
        for keys, value in atmosphere_mods.items():
            if self.atmosphere in keys:
                mod = value
                break
        temperature_roll = utils.d6() + utils.d6() + mod
        if temperature_roll < 2:
            self.temperature = "Frozen"
        elif temperature_roll < 5:
            self.temperature = "Cold"
        elif temperature_roll < 10:
            self.temperature = "Temperate"
        elif temperature_roll < 12:
            self.temperature = "Hot"
        elif temperature_roll > 11:
            self.temperature = "Boiling"
        else:
            self.temperature = "Temperate"
        
        # Generate Hydrographics of world
        if self.size < 2:
            self.hydrographics = 0
        else:
            mod = 0
            if self.atmosphere < 2 or (self.atmosphere > 9 and self.atmosphere < 13):
                mod = -4
            self.hydrographics = utils.d6() + utils.d6() - 7 + self.atmosphere + mod
        if self.hydrographics < 0:
            self.hydrographics = 0

        # Generate Population of world
        self.population = utils.d6() + utils.d6() - 2

        # Generate Government of world
        if self.population == 0:
            self.government = 0
        else:
            self.government = utils.d6() + utils.d6() - 7 + self.population
            if self.government < 0:
                self.government = 0

            # Populate factions
            mod = 0
            if self.government == 0 or self.government == 7:
                mod = 1
            elif self.government > 9:
                mod - 1
            for _ in range(self.population + mod):
                faction = Faction()
                faction.generate_faction(world=self)
                self.factions.append(faction)

            # Generate cultural differences
            self.cultural_differences = f"{utils.d6()}{utils.d6()}"

        # Generate Law Level of world
        if self.population == 0:
            self.law_level = 0
        else:
            self.law_level = utils.d6() + utils.d6() - 7 + self.government
            if self.law_level < 0:
                self.law_level = 0

        # Generate Starport of world
        starport_roll = utils.d6() + utils.d6()
        if self.population > 10:
            starport_roll += 2
        elif self.population > 8:
            starport_roll += 1
        elif self.population < 3:
            starport_roll -= 2
        elif self.population < 5:
            starport_roll -= 1
        starport_map = {
            (0,1,2): "X",
            (3,4): "E",
            (5,6): "D",
            (7,8): "C",
            (9,10): "B",
            (11,12,13,14): "A"
        }
        for keys, value in starport_map.items():
            if starport_roll in keys:
                self.starport = value
                break

        # Generate Tech Level of world
        if self.population == 0:
            self.tech_level = 0
        else:
            self.tech_level = self.generate_tech_level()

        # Generate Bases of world
        starport_details = utils.get_starport_details()
        starport_details = starport_details.get(self.starport, {})
        for key in starport_details['bases'].keys():
            roll = utils.d6() + utils.d6()
            if roll >= starport_details['bases'][key]:
                self.bases.append(key)
        roll = utils.d6() + utils.d6()
        if roll < 10:
            self.bases.append("Gas_Giant")

        # Generate Alert Level of world
        if self.atmosphere >= 10 or self.government in [0,7,10] or self.law_level == 0 or self.law_level >= 9:
            self.alert_level = "AMBER"

        # Generate Trade Codes of world
        self.trade_codes = self.generate_trade_codes()

    def generate_tech_level(self):
        """ Generate Tech Level"""
        tech_level = utils.d6()
        
        if self.starport == "X":
            tech_level -= 4
        elif self.starport == "C":
            tech_level += 2
        elif self.starport == "B":
            tech_level += 4
        elif self.starport == "A":
            tech_level += 6

        if self.size < 2:
            tech_level += 2
        elif 1 < self.size < 5:
            tech_level += 1

        if self.atmosphere < 4 or self.atmosphere > 9:
            tech_level += 1

        if self.hydrographics == 0 or self.hydrographics == 9:
            tech_level += 1
        elif self.hydrographics == 10:
            tech_level += 2

        if (6 > self.population > 0) or self.population == 8:
            tech_level += 1
        elif self.population == 9:
            tech_level += 2
        elif self.population == 10:
            tech_level += 4

        if self.government == 0 or self.government == 5:
            tech_level += 1
        elif self.government == 7:
            tech_level += 2
        elif self.government == 13 or self.government == 14:
            tech_level -=2

        return tech_level
    def generate_trade_codes(self):
        """ Generate Trade Codes for the world """
        trade_codes = []
        
        if 3 < self.atmosphere < 10 and 3 < self.hydrographics < 9 and 4 < self.population < 8:
            trade_codes.append("Ag")
        
        if self.size == 0 and self.atmosphere == 0 and self.hydrographics == 0:
            trade_codes.append("As")
        
        if self.population == 0 and self.government == 0 and self.law_level == 0:
            trade_codes.append("Ba")

        if self.atmosphere > 1 and self.hydrographics == 0:
            trade_codes.append("De")
        
        if self.atmosphere > 9 and self.hydrographics > 0:
            trade_codes.append("Fl")
        
        if 5 < self.size < 9 and self.atmosphere in [5,6,8] and 4 < self.hydrographics < 8:
            trade_codes.append("Ga")
        
        if self.population > 8:
            trade_codes.append("Hi")
        
        if self.tech_level > 11:
            trade_codes.append("Ht")

        if (self.atmosphere == 0 or self.atmosphere == 1) and self.hydrographics > 0:
            trade_codes.append("Ic")

        if self.atmosphere in [0,1,2,4,7,9] and self.population > 8:
            trade_codes.append("In")
        
        if self.population < 4:
            trade_codes.append("Lo")

        if self.tech_level < 6:
            trade_codes.append("Lt")
        
        if self.atmosphere < 4 and self.hydrographics < 4 and self.population > 5:
            trade_codes.append("Na")
        
        if self.population < 7:
            trade_codes.append("Ni")

        if self.atmosphere in [2,3,4,5] and self.hydrographics < 4:
            trade_codes.append("Po")

        if self.atmosphere in [6,8] and self.population in [6,7,8] and self.government in [4,5,6,7,8,9]:
            trade_codes.append("Ri")

        if self.atmosphere == 0:
            trade_codes.append("Va")

        if self.hydrographics >=10:
            trade_codes.append("Wa")
        
        return trade_codes
    def get_hex_value(self, number: int):
        """ Get the hex code of the world """
        if number < 10:
            return str(number)
        else:
            if number == 10:
                return "A"
            elif number == 11:
                return "B"
            elif number == 12:
                return "C"          
            elif number == 13:
                return "D"
            elif number == 14:
                return "E"
            elif number == 15:
                return "F"  
            
    def to_string(self):
        """ Return a string representation of the subsector system """
        return (f"{self.location} {self.starport}{self.get_hex_value(self.size)}{self.get_hex_value(self.atmosphere)}{self.get_hex_value(self.hydrographics)}{self.get_hex_value(self.population)}{self.get_hex_value(self.government)}{self.get_hex_value(self.law_level)}-{self.tech_level} {' '.join(self.bases)} {' '.join(self.trade_codes)} {self.alert_level}")

class Faction:
    def __init__(self):
        self.name = None
        self.strength = None
        self.gov = None

    def generate_faction(self, world:Subsector_System):
        """ Generate a faction with random attributes """
        self.gov = utils.d6() + utils.d6() - 7 + world.population
        if self.gov < 0:
            self.gov = 0

        # Generate strength of faction
        strength_roll = utils.d6() + utils.d6()
        if strength_roll < 4:
            self.strength = "obscure"
        elif strength_roll < 6:
            self.strength = "fringe"
        elif strength_roll < 8:
            self.strength = "minor"
        elif strength_roll < 10:
            self.strength = "notable"
        elif strength_roll < 12:
            self.strength = "significant"
        else:
            self.strength = "overwhelming"
    
    def to_string(self):
        """ Return a string representation of the faction """
        return f"Faction(name={self.name}, strength={self.strength}, government={self.gov})"