#Prison Escape Game
#Start in cell
#Can go to: Cafeteria, Yard, Laundry, Kitchen(Shift for money)
#Inventory starts empty
#Items are randomly scattered around rooms
#Hold a maximum of 3 items, hide item under bed to get rid of item or use it
#Rooms that you can only get to with specific items, such as vents with a screwdriver

import os

#VARIABLES
INSTRUCTIONS = "\nWelcome to PRISON ESCAPE \n" \
               "Your goal is to escape the prison! \n" \
               "Each playthrough the items to help you escape are randomly littered throughout the rooms \n" \
               "Type restart at anytime to restart \n" \
               "Type quit at anytime to stop playing \n" \
               "Good Luck!!! \n"

STARTING_MAP = "Workshop \n" \
        "|       \\ \n" \
        f"CELL --- Bathroom \n" \
        "| \n" \
        f"Cafeteria --- Kitchen \n" \
        "        \\    / \n" \
        f"         yard \n"


#CLASSES
class Room:
    def __init__(self, name, description, actions, items, exits, npc):
        self.name = name
        self.description = description
        self.actions = actions
        self.items = items
        self.exits = exits
        self.npc = npc

    def show_description(self):
        print(self.description)


class Player:
    def __init__(self, player_location, all_rooms):
        self.rooms = all_rooms

        self.player_location = player_location

        self.already_spoken_derek = False


    def action(self):
        while True:
            for index, action in enumerate(self.player_location.actions):
                print(f"{index + 1}: {action}")

            try:
                choice = int(input("Choose action: "))

            except ValueError:
                print("Please input a valid number")
                continue

            if choice == 1:
                print("You chose to look around\n")
                self.look_around()
            elif choice == 2:
                print("You chose to move room \n")
                self.move_room()
            elif choice == 3:
                print("You chose talk to prisoner\n")
                self.talk_to_npc()
            else:
                print()
                continue

            break


    def look_around(self):
        if len(self.player_location.items) > 1:
            joined_items = ", ".join(self.player_location.items[:-1]) + ' and ' + self.player_location.items[-1] #Displays items found in Enlgish
            print(f"\nYou see a {joined_items}")

        elif self.player_location.items:
            print(f"\nYou see a {self.player_location.items[0]}")

        else:
            print("\nYou don't find anything")

        print() #Add space for readability


    def move_room(self):
        print() #Add space for readability

        while True:
            print("----Prison Map----")
            show_map()

            for index, value in enumerate(self.player_location.exits):
                print(f"{index + 1}: {value.capitalize()}")
            print("or")
            print(f"{len(self.player_location.exits) + 1}: Stay in {player.player_location.name} \n")

            try:
                choice = int(input("Choose a room to go to: "))

                if 1 <= choice <= len(self.player_location.exits):
                    index_choice = choice - 1 #Get the index of users choice

                    chosen_room = self.player_location.exits[index_choice]
                    print(f"You chose {chosen_room.capitalize()}") #Print chosen room

                    self.player_location = self.rooms[chosen_room] #Update player location
                    break

                elif choice == 4:
                    break

                else:
                    print(f"Choose option between 1 and {len(self.player_location.exits)}")

            except ValueError:
                print("Please input a valid number")
                continue

        show_map()
        print() #Add space for readability
        print(self.player_location.description) #Print new location to terminal


    def talk_to_npc(self):
        #Check if player has already spoken to NPC
        if self.already_spoken_derek:
            print(self.player_location.npc["dialogue"][1])
        else:
            print(self.player_location.npc["dialogue"][0])

        self.already_spoken_derek = True
        print() #Add space for readability



cell = Room(
    "Cell",
    "You are in your Cell. \nIt's a small, dimly lit room with two hard beds and a window. You have a cellmate, you don't talk often. \n", #Description
    ["Check room for items", "Move room", "Talk to cellmate"], #Actions
    ["Sword", "Fork", "Knife"], #Items
    ["workshop", "bathroom", "cafeteria"], #Exits
    {
        "name": "Derek",
        "dialogue": ["Yo, Derek is me. I got a mission for you. If you get me some cash i'll give you a screwdriver. Get money from doing a shift in the Kitchen then get back to me.", "I already told you go get me money from a shift in the Kitchen and you can have the screwdriver. "],
        "item": "screwdriver"
    }
)

cafeteria = Room(
    "Cafeteria",
    "You are in the Cafeteria. \nIt's a loud place with", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cell", "yard", "kitchen"], #Exits
    {}
)

yard = Room(
    "Yard",
    "You are in the Yard. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cafeteria", "kitchen"], #Exits
    {} #Exits
)

kitchen = Room(
    "Kitchen",
    "You are in the Kitchen. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cafeteria", "yard"], #Exits
    {} #Exits
)

bathroom = Room(
    "Bathroom",
    "You are in the Bathroom. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cell", "workshop"], #Exits
    {} #Exits
)

workshop = Room(
    "Workshop",
    "You are in the Workshop. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cell", "bathroom"], #Exits
    {}
)

rooms = {
    "cell": cell,
    "cafeteria": cafeteria,
    "yard": yard,
    "kitchen": kitchen,
    "bathroom": bathroom,
    "workshop": workshop
}

player = Player(rooms["cell"], rooms)


#FUNCTIONS
def show_map():
    #Creating strings for the locations on the map which are mutable. The room you are in shows as ALL CAPS.
    w_name = workshop.name
    cell_name = cell.name
    b_name = bathroom.name
    cafeteria_name = cafeteria.name
    k_name = kitchen.name
    y_name = yard.name

    print(  f'{w_name.upper() if player.player_location.name == w_name else w_name} \n'
            "|       \\ \n"
            f"{cell_name.upper() if player.player_location.name == cell_name else cell_name} --- {b_name.upper() if player.player_location.name == b_name else b_name} \n"
            "| \n"
            f"{cafeteria_name.upper() if player.player_location.name == cafeteria_name else cafeteria_name} --- {k_name.upper() if player.player_location.name == k_name else k_name} \n"
            "        \\    / \n"
            f"         {y_name.upper() if player.player_location.name == y_name else y_name} \n"
    )

def clear_screen():
    # Check the operating system name
    if os.name == 'nt':
        # Command for Windows
        _ = os.system('cls')
    else:
        # Command for Linux, Mac, and other systems
        _ = os.system('clear')

#----Game Loop----
clear_screen()
print(INSTRUCTIONS) #Give user game instructions
print(STARTING_MAP)
print(player.player_location.description) #Starting room description


while True:
    player.action()

    # player.look_around()
    # player.move_room()


