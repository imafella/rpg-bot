from Traveller.Models.subsector_system import Subsector_System as world
from Traveller import traveller_utils as utils


for _ in range(1000):
    print(f"\nGenerating Subsector {_+1}:\n")
    for i in range (8):
        if i+1 < 10:
            x = f"0{i+1}"
        else:
            x = str(i+1)
        for j in range (10):
            if j+1 < 10:
                y = f"0{j+1}"
            else:
                y = str(j+1)
            
            if utils.d6() > 3:
                continue
            new_world = world(location=f"{x}{y}")
            new_world.generate_world()
            print(new_world.to_string()) 