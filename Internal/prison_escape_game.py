#Prison Escape Game
#Start in cell
#Can go to: Cafeteria, Yard, Laundry, Kitchen(Shift for money)
#Inventory starts empty
#Items are randomly scattered around rooms
#Hold a maximum of 3 items, hide item under bed to get rid of item or use it
#Rooms that you can only get to with specific items, such as vents with a screwdriver

#LIBRARIES
import random
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

#Constant variables for players actions
CHECK = "Check room for items"
MOVE = "Move room"
TALK = "Talk to prisoner"
SHIFT = "Start shift"

#CLASSES
class Room:
    def __init__(self, name, description, actions, items, exits, npcs=None):
        self.name = name
        self.description = description
        self.actions = actions
        self.items = items
        self.exits = exits
        self.npcs = npcs if npcs else []

    def show_description(self):
        print(self.description)


class Player:
    def __init__(self, player_location, all_rooms):
        self.rooms = all_rooms

        self.player_location = player_location
        self.action_functions = {
            CHECK: self.look_around,
            MOVE: self.move_room,
            TALK: self.talk_to_prisoner,
            SHIFT: self.do_shift
        }

        self.already_spoken_derek = False


    def action(self):
        while True:
            for index, action in enumerate(self.player_location.actions):
                print(f"{index + 1}: {action}")

            try:
                choice = int(input("Choose action: "))

                if 1 <= choice <= len(self.player_location.actions): #Check if user's choice is one of avaliable options
                    action_name = self.player_location.actions[choice - 1]
                    action_function = self.action_functions[action_name]
                    action_function()

                else:
                    print(f"Please choose valid number between 1 - {len(player.player_location.actions)} \n")

            except ValueError:
                print("Please input a valid number")
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
            print(f"{len(self.player_location.exits) + 1}: Stay in {self.player_location.name} \n")

            try:
                choice = int(input("Choose a room to go to: "))

                if 1 <= choice <= len(self.player_location.exits):
                    index_choice = choice - 1 #Get the index of users choice

                    chosen_room = self.player_location.exits[index_choice]
                    print(f"You chose {chosen_room.capitalize()}") #Print chosen room

                    self.player_location = self.rooms[chosen_room] #Update player location
                    break

                elif choice == len(self.player_location.exits) + 1:
                    break

                else:
                    print(f"Choose option between 1 and {len(self.player_location.exits)}")

            except ValueError:
                print("Please input a valid number")
                continue

        show_map()
        print() #Add space for readability
        print(self.player_location.description) #Print new location to terminal


    def talk_to_prisoner(self):
        dialogue = self.player_location.npcs.dialogue
        already_spoken_to = self.player_location.npcs.already_spoken_to

        print() #Add space for readability
        if already_spoken_to:
            print(dialogue[1]) # Print second script if user has already spoken to npc
        else:
            print(dialogue[0]) # Print first dialogue if first time talking to npc

        self.player_location.npcs.already_spoken_to = True


    def do_shift(self):
        print() #Add space for readibility
        print("You started your shift in the Kitchen")

        #MINI GAME to complete kitchen shift
        anagram_foods = ["TOMATO", "CHEESE", "APPLE", "MILK", "POTATO", "BREAD"] #All possible foods for anagrams
        chosen_food = random.choice(anagram_foods) #Choose random food from list
        list_food = list(chosen_food) #Turn the immutable string into a list
        random.shuffle(list_food) #Shuffle characters in list
        anagram = "".join(list_food) #Join shuffled list into string



        while True:
            try:
                print(anagram)
                guess = input("Guess the food \n>")
                if guess.isdigit():
                    raise ValueError
                elif guess.lower() == chosen_food.lower():
                    print("You guessed correct")
                else:
                    print("You guessed incorrect! ")
                
                

            except ValueError:
                print("Please enter a valid word")
                continue




class NPC:
    def __init__(self, name, dialogue, item):
        self.name = name
        self.dialogue = dialogue
        self.required_item = item
        self.already_spoken_to = False


#NPC CLASS OBJECTS
Derek_NPC = NPC(
    "Derek",
    ["Yo, Derek is me. I got a mission for you. If you get me some cash i'll give you a screwdriver. Get money from doing a shift in the Kitchen then get back to me. \n",
     "I already told you go get me money from a shift in the Kitchen and you can have the screwdriver. \n"],
    "screwdriver"
)

Joel_NPC = NPC(
    "Joel",
    ["Hey man, I'm Joel. Look, I'm super busy at the moment and have a little task for you. I left my toothbrush in the bathroom, if you go and get it for me, i'll give you a piece of scrap metal which is great for crafting items. \n",
     "Get back to me when you have my toothbrush and i'll give you the scrap metal. \n"],
    "scrap metal"
)

Bob_NPC = NPC(
    "Bob",
    ["Hello there! It's me BOB. Everyone hates me in the cafeteria, could you please please please go get me some food. If you do I'll give you this firework!!! \n",
     "I'm begging you man please get me some food I'm starving! Then you can have the firework. It's perfect for a good distraction. \n"],
    "fireworks"
)

#ROOM CLASS OBJECTS
cell = Room(
    "cell",
    "You are in your Cell. \nIt's a small, dimly lit room with two hard beds and a window. You have a cellmate, you don't talk often. \n", #Description
    [CHECK, MOVE, TALK, SHIFT], #Actions
    ["Sword", "Fork", "Knife"], #Items
    ["workshop", "bathroom", "cafeteria"], #Exits
    npcs=Derek_NPC
)

cafeteria = Room(
    "cafeteria",
    "You are in the Cafeteria. \nIt's a loud place with", #Description
    [CHECK, MOVE], #Actions
    [], #Items
    ["cell", "yard", "kitchen"] #Exits
)

yard = Room(
    "yard",
    "You are in the Yard. \n", #Description
    [CHECK, MOVE], #Actions
    [], #Items
    ["cafeteria", "kitchen"] #Exits
)

kitchen = Room(
    "kitchen",
    "You are in the Kitchen. \n", #Description
    [CHECK, MOVE], #Actions
    [], #Items
    ["cafeteria", "yard"] #Exits
)

bathroom = Room(
    "bathroom",
    "You are in the Bathroom. \n", #Description
    [CHECK, MOVE, TALK], #Actions
    [], #Items
    ["cell", "workshop"], #Exits
    npcs=Bob_NPC
)

workshop = Room(
    "workshop",
    "You are in the Workshop. \n", #Description
    [CHECK, MOVE, TALK], #Actions
    [], #Items
    ["cell", "bathroom"], #Exits
    npcs=Joel_NPC
)

rooms = {
    "cell": cell,
    "cafeteria": cafeteria,
    "yard": yard,
    "kitchen": kitchen,
    "bathroom": bathroom,
    "workshop": workshop
}


#PLAYER CLASS OBJECT
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


