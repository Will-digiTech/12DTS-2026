# This is my prison escape game. 
# The player must navigate through the prison, talk to NPCs, complete shifts which include minigames, collect items, craft items, and use all these things to escape the prison.
# There are three different escape routes.
# The easiest route is to get the screwdriver from Derek in the cell and use it to escape through the vent in the bathroom, but you must also complete a mini-game in the vent to successfully escape.
# The second route is to incapacitate a guard, steal their uniform and use it to walk out the front door
# The third route is to climb the wall in the yard using a grappling hook, this is the most difficult route as you need to have both the rope and scrap metal to craft a grappling hook, and you also need to have a firework to distract the guards while you climb the wall.
# You can get the rope from the workshop, the scrap metal from Joel in the workshop and the firework from Bob in the bathroom
# Good luck escaping the prison!


#LIBRARIES
import random
import os
import time
import sys

#CONSTANT VARIABLES
INSTRUCTIONS = "\nWelcome to PRISON ESCAPE \n" \
                "Your goal is to escape the prison! \n" \
                "There are three possible escape routes. Route 1 is the easiest, while Route 3 is the most difficult. \n" \
                "Type 'restart' at any input prompt to restart the game. \n" \
                "Good Luck!!! \n"

STARTING_MAP = "Workshop \n" \
        "|       \\ \n" \
        f"CELL --- Bathroom \n" \
        "| \n" \
        f"Cafeteria --- Kitchen \n" \
        "        \\    / \n" \
        f"         yard \n"

#Constant variables for players actions
SHOW_INVENTORY = "Check inventory"
CHECK = "Check room for items"
MOVE = "Move room"
TALK = "Talk to prisoner"
KITCHEN_SHIFT = "Start Kitchen shift"
WORKSHOP_SHIFT  = "Start Workshop shift"
STEAL_FOOD = "Steal food"
HIDE_ITEM = "Hide item under bed"
GET_ITEM_BED = "Get stored items from under bed"
TAKE_GUARD_UNIFORM = "Attempt to beat up guard"
CLIMB_WALL = "Attempt to climb wall"
VENT_ESCAPE = "Climb through vent"
CRAFT = "Craft an item"

#Store item names in constants to avoid typo errors and make more readable. Also makes it easy to add more items later.
ITEM_TOOTHBRUSH = "Toothbrush"
ITEM_SCRAP_METAL = "Scrap metal"
ITEM_SCREWDRIVER = "Screwdriver"
ITEM_ROPE = "Rope"
ITEM_FOOD = "Food"
ITEM_MAKESHIFT_WEAPON = "Makeshift Weapon"
ITEM_GRAPPLING_HOOK = "Grappling hook"
ITEM_FIREWORK = "Firework"


#CLASSES
class Room:
    def __init__(self, name, room_text, actions, items, exits, npc=None, has_visited=False):
        self.name = name
        self.room_text = room_text #Room description and location text stored in a dictionary
        self.actions = actions #List of actions that the player can do in the room
        self.items = items #List of items in the room
        self.exits = exits #All exits from the room
        self.npc = npc #NPC in the room, if there is one
        self.has_visited = has_visited #Flag to check if player has already visited the room, used to display different text based on if they have been there before or not

    def show_description(self):
        #Check if player has already visited the room, if not show location and description text, if they have show location text only
        if not self.has_visited:
            type_writer(self.room_text["location"] + "\n" + self.room_text["description"])
            self.has_visited = True
        else:
            type_writer(self.room_text["location"])


class Player:
    def __init__(self, player_location, all_rooms):
        self.rooms = all_rooms #Dictionary of all rooms in the game, used to update player location when moving rooms


        self.player_location = player_location #Current room player is in
        self.action_functions = { #Dictionary linking each action to its function
            SHOW_INVENTORY: lambda: self.show_inventory(self.inventory, "Inventory", clear_screen_at_start=True, show_money=True), #Lambda function used to avoid function being called immediately
            CHECK: self.look_around,
            MOVE: self.move_room,
            TALK: self.talk_to_prisoner,
            KITCHEN_SHIFT: self.kitchen_shift,
            WORKSHOP_SHIFT: self.workshop_shift,
            STEAL_FOOD: self.steal_food,
            HIDE_ITEM: self.hide_item,
            GET_ITEM_BED: self.get_item_from_bed,
            TAKE_GUARD_UNIFORM: self.knock_out_guard,
            CLIMB_WALL: self.climb_wall,
            VENT_ESCAPE: self.vent_escape,
            CRAFT: self.craft
        }

        self.inventory = [] #Player inventory
        self.max_inventory = 3 #Maximum number of items allowed in player inventory
        self.bed_inventory = ["Screwdriver"] #Inventory for items stored under bed
        self.money = 0 #Player starting money
        self.last_shift = None #Keep track of last shift to stop player doing same shift twice in a row

        #Stored as a variable instead of hard coded into the mini-game so the difficulty can be changed easily later.
        self.length_of_vent_sequence = 5 #Length of direction sequence in vent mini-game, can be changed to make mini-game easier or harder
        self.guard_id = random.randint(10000, 99999) #Random guard ID number for final escape


    def action(self):
        #MAIN GAME LOOP FUNCTION
        #Gives the player possible actions based on the room they are in
        while True:
            self.player_location.show_description()
        
            indexed_loop(self.player_location.actions)

            chosen_action = pick_from_choices("\nChoose action: ", self.player_location.actions)

            action_function = self.action_functions[chosen_action]
            action_function()
            


    def look_around(self):
        clear_screen()
        if len(self.player_location.items) > 1: #If there are multiple items in the room
            joined_items = ", ".join(self.player_location.items[:-1]) + ' and ' + self.player_location.items[-1] #Displays items found in English
            type_writer(f"You see a {joined_items}\n")

            self.pick_up_item()

        elif self.player_location.items: #If there is one item in the room
            type_writer(f"You see a {self.player_location.items[0]}\n", ask_for_input=False)

            self.pick_up_item()
        else: #No items in the room
            type_writer("You don't find anything")

        print() #Add space for readability


    def pick_up_item(self):
        print("Would you like to pick an item up?")

        while True:
            pick_item_choice = get_input("Yes/No \n> ").lower()
            print() #Add space for readability

            if pick_item_choice == "yes":

                options = self.player_location.items.copy() #Copy list of items in the room to manipulate without changing original list

                if len(options) == 1: #If there is only one item in the room, automatically pick it up
                    item = options[0]
                    try:
                        self.add_to_inventory(item, self.player_location.items)
                    except ValueError as e:
                        print(f"\n{e}\n")
                    self.show_inventory(self.inventory, "Inventory")
                    break
                else:
                    options.append("Pick up all items") #Add option to pick up all items if there are multiple items in the room

                indexed_loop(options) #Show options with an index number for the user to choose from

                choice = pick_from_choices("\nChoose item to pick up: ", options)
                
                if choice == "Pick up all items":
                    clear_screen()
                    for item in self.player_location.items[:]:
                        try:
                            self.add_to_inventory(item, self.player_location.items)
                        except ValueError as e: #If inventory is full, stop adding items and show error message
                            print(f"\n{e}\n")

                    self.show_inventory(self.inventory, "Inventory")
                    break
                    
                else: #If the user chooses one specific item, add it to the inventory
                    clear_screen()
                    try:
                        self.add_to_inventory(choice, self.player_location.items)
                    except ValueError as e: #If inventory is full, stop adding item and show error message
                        print(f"\n{e}\n")

                
                self.show_inventory(self.inventory, "Inventory")
                break
            elif pick_item_choice == "no":
                break
            else:
                print("Enter Yes or No")
                continue

    def has_inventory_space(self, slots_needed=1):
        #Using the inventory limit through one function avoids hard coding checks in multiple places.
        return len(self.inventory) + slots_needed <= self.max_inventory

    def add_to_inventory(self, item, remove_key=None, remove=True, show_as_added=True):
        #Raises error if user tries to add item when inventory is already full.
        if not self.has_inventory_space():
            raise ValueError(f"Inventory is full (max {self.max_inventory} items). Clear inventory by using items or hiding them under your bed.")
        
        self.inventory.append(item)
        #Only removes the item when remove=True. Used for room items, not crafted items.
        if remove:
            remove_key.remove(item)

        if show_as_added:
            print(f"+{item}")
        else:
            print(f"-{item}")


    def move_room(self):
        clear_screen()
        print("----Prison Map----")
        show_map(self.player_location)

        options = self.player_location.exits + ["Stay in current room"] #Add option to stay in current room

        indexed_loop(options)

        chosen_room = pick_from_choices("Choose a room to go to: ", options)

        if chosen_room != "Stay in current room":
            self.player_location = self.rooms[chosen_room] #Change player location to chosen room

        clear_screen()


    def talk_to_prisoner(self):
        clear_screen()
        npc = self.player_location.npc

        if npc is None:
            type_writer("There is no one here to talk to.")
            return

        dialogue = npc.dialogue
        already_spoken_to = npc.already_spoken_to
        has_given_reward = npc.has_given_reward

        requirement_type = npc.exchange["type"]
        requirement = npc.exchange["requirement"]
        reward = npc.exchange["reward"]

        if has_given_reward:
            type_writer(dialogue["after_exchange"]) #Print dialogue for if user has already spoken to npc and completed exchange
            return

        if already_spoken_to:
            #Check if user has required items NPC is requesting.
            if requirement_type == "money": #Check if npc wants money
                if self.money >= requirement:
                    if not self.has_inventory_space():
                        type_writer("You have enough money, but your inventory is full. Hide or use an item before collecting the reward.")
                        return
                    self.money -= requirement
                    type_writer(dialogue["exchange"]) #Print dialogue for when you give npc required item
                    print(f"-${requirement}")
                    self.add_to_inventory(reward, remove=False)
                    npc.has_given_reward = True #Set flag to true to show that npc has given reward
                    self.show_inventory(self.inventory, "Inventory")
                    return
                
            elif requirement_type == "item": #Check if npc wants an item
                if requirement in self.inventory:
                    self.inventory.remove(requirement)
                    type_writer(dialogue["exchange"]) #Print dialogue for when you give npc required item
                    print(f"-{requirement}")
                    self.add_to_inventory(reward, remove=False)
                    npc.has_given_reward = True #Set flag to true to show that npc has given reward
                    self.show_inventory(self.inventory, "Inventory")
                    return


            type_writer(dialogue["already_spoken"]) # Print dialogue for if user has already spoken to npc
        else:
            type_writer(dialogue["intro"]) # Print dialogue for npc opening script
            npc.already_spoken_to = True


    def hide_item(self):
        if self.inventory:
            options = self.inventory.copy()

            if len(options) > 1:
                options.append("Hide all items")

            indexed_loop(options)

            choice = pick_from_choices("\nChoose item to hide under the bed: ", options)
            clear_screen()

            if choice == "Hide all items":
                for item in self.inventory[:]:
                    self.bed_inventory.append(item)
                    self.inventory.remove(item)
                    print(f"-{item}")
                self.show_inventory(self.bed_inventory, "Bed inventory")

            else:
                self.bed_inventory.append(choice)
                self.inventory.remove(choice)
                print(f"-{choice}")
                self.show_inventory(self.bed_inventory, "Bed inventory")

        else:
            type_writer("You don't have anything to hide")
            return

    def get_item_from_bed(self):
        while True:
            clear_screen()
            if self.bed_inventory:

                options = self.bed_inventory.copy()

                if len(options) > 1:
                    options.append("Get all items from bed")

                indexed_loop(options)

                choice = pick_from_choices("\nChoose item to take: ", options)

                if choice == "Get all items from bed":
                    for item in self.bed_inventory[:]:
                        try:
                            self.add_to_inventory(item, self.bed_inventory)
                        except ValueError as e:
                            print(f"\n{e}\n")

                    self.show_inventory(self.inventory, "Inventory")
                    break

                else:
                    try:
                        self.add_to_inventory(choice, self.bed_inventory)
                    except ValueError as e:
                        print(f"\n{e}\n")

                self.show_inventory(self.inventory, "Inventory")
                break

            else:
                type_writer("There are no stored items under your bed")
                break


    def craft(self):
        while True:
            clear_screen()
            player_craftable_items = [
                item for item in craftable_items if self.check_craft_items(item)
            ]

            if not player_craftable_items:
                print("You can't craft anything \n")
                self.show_craftable_items()
                return

            print(f"You can craft: {', '.join(player_craftable_items)}\n")

            options = player_craftable_items.copy()
            options.append("View craftable items") #Add option to view craftable items and their required materials
            options.append("Don't craft anything") #Give player option to not craft anything

            indexed_loop(options)
            chosen_item = pick_from_choices("\nPick item to craft: ", options)

            if chosen_item == "View craftable items":
                clear_screen()
                self.show_craftable_items()
                continue

            if chosen_item == "Don't craft anything":
                return

            materials = craftable_items[chosen_item]

            #Remove the required material from player's inventory
            for material in materials:
                if material in self.inventory: #Backup line to protect accidental error
                    self.inventory.remove(material)

            try:
                clear_screen()
                self.add_to_inventory(chosen_item, None, remove=False)
                self.show_inventory(self.inventory, "Player Inventory")
                return
                
            except ValueError as e:
                print(f"\n{e}\n")


    def check_craft_items(self, item):
        for required_item in craftable_items[item]:
            if required_item not in self.inventory:
                return False
        return True

    def show_craftable_items(self):
        print("Craftable items: ")
        for item, materials in craftable_items.items():
            print(f"{item} --> {', '.join(materials)}")
        get_input("\nPress enter to continue: ")
        clear_screen()


    def kitchen_shift(self):
        if self.last_shift == KITCHEN_SHIFT:
            type_writer("You can't do the same shift twice in a row, instead complete the workshop shift")
            return

        # MINI GAME to complete kitchen shift
        correct_food_counter = 0
        #These values are stored in variables instead of being hard coded
        num_lives = 2 #Can be adjusted later to make the mini-game easier or harder
        anagram_foods = ["TOMATO", "CHEESE", "APPLE", "MILK", "POTATO", "BREAD"] #All possible foods for anagrams

        #Kitchen shift instructions
        type_writer("You started your shift in the Kitchen.\n" + "You must solve these anagrams by typing the correct food.\n" + "You must get 5 correct to finish your shift.\n" + f"You have {num_lives} lives, if you fail you get kicked off your shift and earn no money.\n")

    
        while correct_food_counter < 5:
            clear_screen()
            chosen_food = random.choice(anagram_foods) #Choose random food from list
            list_food = list(chosen_food) #Turn the immutable string into a list
            random.shuffle(list_food) #Shuffle characters in list
            anagram = "".join(list_food) #Join shuffled list into string

            if anagram == chosen_food: #If the anagram is the same as the original word, shuffle again
                continue

            #Repeat until valid user entry
            while True:
                try:
                    print(f"{correct_food_counter}/5 completed \n")
                    print(anagram)
                    guess = get_input("Guess the food \n>")
                    if guess.isdigit():
                        raise ValueError
                    else:
                        break   

                except ValueError:
                    print("Please enter a valid word")
                    continue

            #Mini-game logic
            if guess.lower() == chosen_food.lower():
                correct_food_counter += 1
                anagram_foods.remove(chosen_food)

                
                
            else:
                num_lives -= 1
                type_writer("You guessed incorrect!", ask_for_input=False)
                if num_lives == 0:
                    type_writer("You failed your shift!\n", clear_screen_at_start=False)
                    self.last_shift = KITCHEN_SHIFT #Update last shift to stop player doing same shift twice in a row
                    return
                else:
                    type_writer(f"You have used a life, you have {num_lives} remaining.", clear_screen_at_start=False)

        self.money += 5
        self.last_shift = KITCHEN_SHIFT #Update last shift to stop player doing same shift twice in a row
        type_writer("Congratulations you completed your shift and earned 5 dollars", ask_for_input=False)
        type_writer(f"You now have ${self.money} in total", clear_screen_at_start=False)

    def workshop_shift(self):
        if self.last_shift == WORKSHOP_SHIFT:
            type_writer("\nYou can't do the same shift twice in a row, instead complete the kitchen shift\n")
            return

        #MINI GAME to complete workshop shift
        completed_plates = 0
        #Using variables for these settings makes the workshop mini-game easier to rebalance and expand if needed.
        num_lives = 3
        allowed_time = 10
        plates_to_complete = 5

        print() #Add space for readability
        type_writer(f"You started your shift in the Workshop.\n" + "You will get given a number plate back to front and you must type it the correct way.\n" + "For example you might be given '321CBA' and you must type 'ABC123'.\n" + f"You have {allowed_time} seconds to type it or you fail your shift.\n" + f"Complete {plates_to_complete} number plates to complete your shift.\n" + f"You have {num_lives} lives good luck!\n")

        while completed_plates < plates_to_complete:
            countdown()

            number_plate_letters = "".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            number_plate_numbers = "".join(random.choices('1234567890', k=3))
            number_plate = number_plate_letters + number_plate_numbers

            print("Backwards number plate:")
            print(number_plate[::-1]) #Backwards number plate
            print("Correct number plate:")
            start = time.time()
            user_input = get_input("> ")
            end = time.time()
            elapsed_time = round(end - start, 2)

            if elapsed_time < allowed_time:
                if user_input.upper() == number_plate:
                    completed_plates += 1
                    clear_screen()
                    print("You got it")
                    print(f"It took you {elapsed_time} seconds")
                    print(f"Completed number plates : {completed_plates}/{plates_to_complete} \n")
                else:
                    num_lives -= 1
                    type_writer("You typed it out incorrectly", ask_for_input=False)
                    type_writer(f"You have {num_lives} lives remaining \n", clear_screen_at_start=False)
            else:
                num_lives -= 1
                type_writer("You ran out of time\n" + f"It took you {elapsed_time} seconds\n" + f"You have {num_lives} lives remaining \n")


            if num_lives == 0:
                type_writer("You failed your shift! \n")
                self.last_shift = WORKSHOP_SHIFT #Update last shift to stop player doing same shift twice in a row
                return
            
        self.money += 5
        self.last_shift = WORKSHOP_SHIFT #Update last shift to stop player doing same shift twice in a row
        type_writer("You successfully completed your shift and earned 5 dollars!\n" + f"You now have ${self.money} in total \n")


    def steal_food(self):
        if not self.has_inventory_space():
            type_writer("Your inventory is full. Hide or use an item before trying to steal food.")
            return

        type_writer("You are trying to take someone's food without getting caught. \n" + "To successfully take someone's food you must press the enter button within a given time frame. \n" + "Don't press enter too early or too late to take the food.\n" + "Good luck! \n", ask_for_input=False)
        get_input("Press enter to start\n")

        while True:
            countdown()
            time_frame_min = random.randrange(2, 10)
            time_frame_max = time_frame_min + 2

            start = time.time()
            stop_timer = get_input(f"Press enter between {time_frame_min} and {time_frame_max} seconds. \n>")
            if stop_timer != "":
                clear_screen()
                print("Only press enter \n")
                continue
            end = time.time()
            elapsed_time = round(end - start, 2)

            clear_screen()
            print(f"{elapsed_time} seconds")
            if time_frame_min <= elapsed_time <= time_frame_max:
                self.add_to_inventory(ITEM_FOOD, remove=False)
                type_writer("You successfully stole food!", clear_screen_at_start=False)
                self.show_inventory(self.inventory, "Inventory")

                return
            else:
                type_writer("You missed your opportunity", ask_for_input=False, clear_screen_at_start=False)
                type_writer("Try again \n", clear_screen_at_start=False)


    def vent_escape(self):
 
        if ITEM_SCREWDRIVER in self.inventory:
            type_writer(vent_escape_text["Correct item"]["True"])
        else:
            type_writer(vent_escape_text["Correct item"]["False"])
            return


        if self.vent_mini_game():
            type_writer(vent_escape_text["Mini game result"]["True"])
        else:
            type_writer(vent_escape_text["Mini game result"]["False"])
            game_over_lost()

        type_writer(vent_escape_text["Final escape text"].format(guard_id=self.guard_id))
        
        if self.id_check():
            game_over_won(1)
        else:
            game_over_lost()


    def vent_mini_game(self):
        directions = ["left", "right"]
        length_of_sequence = self.length_of_vent_sequence
        randomised_sequence = []

        type_writer(vent_escape_text["Mini game instructions"].format(length_of_sequence=self.length_of_vent_sequence))

        print("Remember the sequence: ")
        for i in range(length_of_sequence):
            randomised_sequence.append(random.choice(directions))
        sequence = " ".join(randomised_sequence)
        print(sequence)

        get_input("\nPress enter to type sequence")
        clear_screen()

        user_sequence = get_input("Enter sequence: \n").lower().strip()
        if user_sequence == sequence:
            return True
        else:
            return False



    def knock_out_guard(self):
        #Chance of escaping without a makeshift weapon (1% success rate)
        if ITEM_MAKESHIFT_WEAPON not in self.inventory:
            if random.random() > 0.01:
                type_writer(guard_disguise_text["Attack guard no weapon text"]["Unsuccessful"])
                game_over_lost()
            else:
                type_writer(guard_disguise_text["Attack guard no weapon text"]["Successful"])

        else:
            type_writer(guard_disguise_text["Attack guard text"])

        #Chance of taking the guard's clothes without getting caught (70% success rate)
        if random.random() > 0.3:
            type_writer(guard_disguise_text["Take uniform"]["success"])
        else:
            type_writer(guard_disguise_text["Take uniform"]["fail"])
            game_over_lost()

        type_writer(guard_disguise_text["In uniform text"].format(guard_id=self.guard_id))

        if self.id_check():
            game_over_won(2)
        else:
            game_over_lost()
        
    def id_check(self):
        clear_screen()
        type_writer(guard_disguise_text["Guard id check"], ask_for_input=False)

        try:
            user_input = int(get_input("\nEnter guard ID number : "))
            if user_input == self.guard_id:
                type_writer(guard_disguise_text["Correct Id"])
                return True
            else:
                type_writer(guard_disguise_text["Incorrect Id"])
                return False
        except ValueError:
            type_writer(guard_disguise_text["Incorrect Id"])
            return False


    def climb_wall(self):
        if ITEM_GRAPPLING_HOOK not in self.inventory:
            type_writer(wall_climb_escape_text["No grappling hook text"])
        elif ITEM_FIREWORK not in self.inventory:
            type_writer(wall_climb_escape_text["No firework text"])
        else:
            clear_screen()
            type_writer(wall_climb_escape_text["Win text"])
            game_over_won(3)



    def show_inventory(self, inventory, name, clear_screen_at_start=False, show_money=False):
        if clear_screen_at_start:
            clear_screen()

        if inventory:
            print(f"{name}: {', '.join(inventory)} \n")
        else:
            print(f"{name} empty \n")

        if show_money:
            print(f"Money: ${self.money} \n")

        get_input("Press enter to continue\n")
        clear_screen()




class NPC:
    def __init__(self, name, dialogue, exchange):
        self.name = name
        self.dialogue = dialogue
        self.exchange = exchange
        self.already_spoken_to = False
        self.has_given_reward = False #Flag to track if the NPC has given a reward


#NPC CLASS OBJECTS
Derek_NPC = NPC(
    "Derek",
    {"intro": "Yo, Derek is me. I got a mission for you. If you get me 10 dollars i'll give you a screwdriver. Get money from doing a shift in the Kitchen or Workshop then get back to me. \n",
     "already_spoken": "I already told you. Go get me money from a shift in the Kitchen or Workshop and you can have the screwdriver. \n",
     "exchange": "I appreciate it bro. Heres your screwdriver. \n",
     "after_exchange": "Thanks for the money man! \n"},

    {"type": "money",
     "requirement": 10,
     "reward": ITEM_SCREWDRIVER}
)

Joel_NPC = NPC(
    "Joel",
    {"intro": "Hey man, I'm Joel. Look, I'm super busy at the moment and have a little task for you. I left my toothbrush in the bathroom, if you go and get it for me, i'll give you a piece of scrap metal which is great for crafting items. \n",
     "already_spoken": "Get back to me when you have my toothbrush and i'll give you the scrap metal. \n",
     "exchange": "Thanks man! Here's the scrap metal. \n",
     "after_exchange": "Pleasure doing business with you! \n"},
    {"type": "item",
     "requirement": ITEM_TOOTHBRUSH,
     "reward": ITEM_SCRAP_METAL}
)

Bob_NPC = NPC(
    "Bob",
    {"intro": "Hello there! It's me BOB. Everyone hates me in the cafeteria, could you please please please go get me some food. If you do I'll give you this firework!!! \n",
     "already_spoken": "I'm begging you man please get me some food I'm starving! Then you can have the firework. It's perfect for a good distraction. \n",
     "exchange": "YAY, i've been starving for so long! Thanks so much, here's the firework!",
     "after_exchange": "Thanks again for the food! \n"},
    {"type": "item",
     "requirement": ITEM_FOOD,
     "reward": ITEM_FIREWORK}
)

#ROOM CLASS OBJECTS
cell = Room(
    "cell",
    {
        "location": "You are in your CELL",
        "description": "It's a small, dimly lit room with two hard beds and a window. You have a cellmate, you don't talk often. \n"
    },
    [SHOW_INVENTORY, CHECK, MOVE, TALK, HIDE_ITEM, GET_ITEM_BED], #Actions
    [], #Items
    ["WORKSHOP", "BATHROOM", "CAFETERIA"], #Exits
    npc=Derek_NPC
)

cafeteria = Room(
    "cafeteria",
    {
        "location": "You are in the CAFETERIA",
        "description": "It's a loud place with lots of prisoners. The food is terrible and the service is even worse. \n"
    },
    [SHOW_INVENTORY, CHECK, MOVE, STEAL_FOOD], #Actions
    [], #Items
    ["CELL", "YARD", "KITCHEN"] #Exits
)

yard = Room(
    "yard",
    {
        "location": "You are in the YARD",
        "description": "It's a long area that stretches from the West to East side of the prison. The walls look climbable with the right tools. \n"
    },
    [SHOW_INVENTORY, CHECK, MOVE, CLIMB_WALL], #Actions
    [], #Items
    ["CAFETERIA", "KITCHEN"] #Exits
)

kitchen = Room(
    "kitchen",
    {
        "location": "You are in the KITCHEN",
        "description": "It's a dirty room where prisoners can do shifts to earn money. There is also a guard stationed here. \n"
    },
    [SHOW_INVENTORY, CHECK, MOVE, KITCHEN_SHIFT, TAKE_GUARD_UNIFORM], #Actions
    [], #Items
    ["CAFETERIA", "YARD"] #Exits
)

bathroom = Room(
    "bathroom",
    {
        "location": "You are in the BATHROOM",
        "description": "It's got 5 cubicles all with broken doors. A strange prisoner is sitting in the corner, muttering to himself. There is also a vent above one of the cubicles. \n"
    },
    [SHOW_INVENTORY, CHECK, MOVE, TALK, VENT_ESCAPE], #Actions
    [ITEM_TOOTHBRUSH], #Items
    ["CELL", "WORKSHOP"], #Exits
    npc=Bob_NPC
)

workshop = Room(
    "workshop",
    {
        "location": "You are in the WORKSHOP",
        "description": "It's a small room that offers a shift for money and a place to craft items. There is also another prisoner who spends all his time here. \n"
    },
    [SHOW_INVENTORY, CHECK, MOVE, TALK, WORKSHOP_SHIFT, CRAFT], #Actions
    [ITEM_ROPE], #Items
    ["CELL", "BATHROOM"], #Exits
    npc=Joel_NPC
)

rooms = {
    "CELL": cell,
    "CAFETERIA": cafeteria,
    "YARD": yard,
    "KITCHEN": kitchen,
    "BATHROOM": bathroom,
    "WORKSHOP": workshop
}


#Crafting
#Recipes are stored in a dictionary so more craftable items can be added later without changing the crafting code.
craftable_items = {
    ITEM_MAKESHIFT_WEAPON: [ITEM_SCRAP_METAL, ITEM_SCREWDRIVER],
    ITEM_GRAPPLING_HOOK: [ITEM_ROPE, ITEM_SCRAP_METAL]
}


#PLAYER CLASS OBJECT
player = Player(rooms["CELL"], rooms)


#Escape prison texts
vent_escape_text = {
    "Correct item": {"True": "You use your screwdriver to open the vent and climb through.", 
                    "False": "You need a screwdriver to open the vent."},
    "Mini game instructions": "You are crawling through the vent, and to make sure you don't get lost you must type the correct sequence of directions. \nYou will be given a sequence of {length_of_sequence} directions, either left or right, for example 'left, right, left, left, right'. You must type the sequence correctly to make it through the vent. \nTo type the sequence correctly, separate directions with a space, e.g. 'left right left' \nGood luck! \n",
    "Mini game result": {"True": "You successfully crawl the correct way and make your way to the guards office. You check the coast is clear and jump in.", 
                         "False": "You get lost in the vents. Eventually, the guards notice an open vent and find you."},
    "Final escape text": "You jump into the guards office and quickly hide. A guard walks in and you jump attack him, knocking him out. You take the guards uniform and his keycard. His ID number is {guard_id}. All you have to do is walk out the front door."
        
}

guard_disguise_text = {
    "Attack guard no weapon text": {
        "Successful": "You successfully beat the guard with no makeshift weapon.",
        "Unsuccessful": "You tried to sneak attack the guard without a makeshift weapon, he beats you up."
    },
    "Attack guard text": "You use your makeshift weapon to incapacitate the guard.",
    "Take uniform": {
        "success": "You successfully take the guard's uniform without anyone catching you.",
        "fail": "You attempt to take the guards uniform but someone catches you."
    },
    "In uniform text": "You have the guards keycard and his ID number is {guard_id}. All you have to do is walk out the front door.",
    "Guard id check": "As you are walking towards the exit you see another guard. He says, 'I don't think I've seen you around before. What's your ID number?'",
    "Correct Id": "'Perfect, have a good one.', he says. You arrive at the front door and swipe your keycard.",
    "Incorrect Id": "The guard looks confused and says, 'No guard has that ID, who are you?'. Before you can think of an excuse he is handcuffing you and taking you away."

}

wall_climb_escape_text = {
    "Win text": "You go over to the East side of the prison and carefully set up the firework behind a bush. You light the firework and swiftly walk away. The firework goes off, exploding above the prison. You set up the firework a little too close to the bush and the bush catches on fire. As everyone is focused on the commotion of the fire, you make your way over to the West side. You grab your grappling hook and climb the wall. ",
    "No grappling hook text": "You need a grappling hook to climb the walls, this can be crafted by using scrap metal and rope.",
    "No firework text": "There are too many guards around, you need a distraction. Find a firework to create a distraction."
}





#FUNCTIONS
def restart_game():
    clear_screen()
    print("Restarting game...\n")
    time.sleep(0.5)
    os.execl(sys.executable, sys.executable, os.path.abspath(__file__)) #Searched this line up to restart game with no bugs, if I don't use it I will have to manually reset everything back to default. E.g room items, npcs, etc.

def get_input(prompt):
    user_input = input(prompt)
    if user_input.strip().lower() == "restart":
        restart_game()
    return user_input

def countdown():
    clear_input_buffer()
    print("Starting in ...")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1 \n")
    time.sleep(1)
    clear_input_buffer()

def indexed_loop(looped_list):
    for index, value in enumerate(looped_list):
        print(f"{index + 1}: {value}")

def pick_from_choices(prompt, options):
    while True:
        try:
            choice = int(get_input(prompt))

            if 1 <= choice <= len(options):
                return options[choice - 1]
            
            else:
                print(f"Choose option between 1 - {len(options)}")

        except ValueError:
            print("Please input a valid number")

def game_over_lost():
    print("You failed to escape the prison.")
    print("Game over!")
    restart_game_choice()
    

def game_over_won(ending):
    print("Congratulations! You successfully escaped the prison.")
    print(f"Ending {ending}/3")
    restart_game_choice()

def restart_game_choice():
    while True:
        choice = get_input("Do you want to restart the game? (Yes/No): ").lower()
        if choice == "yes":
            restart_game()
            break
        elif choice == "no":
            print("Thanks for playing!")
            raise SystemExit
        else:
            print("Please enter 'Yes' or 'No'.")

def show_map(current_room):
    #Creating strings for the locations on the map which are mutable. The room you are in shows as ALL CAPS.
    w_name = workshop.name
    cell_name = cell.name
    b_name = bathroom.name
    cafeteria_name = cafeteria.name
    k_name = kitchen.name
    y_name = yard.name

    print(  f'{w_name.upper() if current_room.name == w_name else w_name} \n'
            "|       \\ \n"
            f"{cell_name.upper() if current_room.name == cell_name else cell_name} --- {b_name.upper() if current_room.name == b_name else b_name} \n"
            "| \n"
            f"{cafeteria_name.upper() if current_room.name == cafeteria_name else cafeteria_name} --- {k_name.upper() if current_room.name == k_name else k_name} \n"
            "        \\    / \n"
            f"         {y_name.upper() if current_room.name == y_name else y_name} \n"
    )
    print(f"Player location: {player.player_location.name.upper()}\n")

def clear_screen():
    if not sys.stdout.isatty():
        return

    # Check the operating system name
    if os.name == 'nt':
        # Command for Windows
        _ = os.system('cls')
    else:
        # Command for Linux, Mac, and other systems
        _ = os.system('clear')

##Searched this up online to clear the input from the user while text is on the screen. The game would break if the user inputs something when they are not supposed to.##
if os.name == 'nt':
    import msvcrt
    def clear_input_buffer():
        if not sys.stdin.isatty():
            return
        while msvcrt.kbhit():
            msvcrt.getch()
else:
    import termios
    def clear_input_buffer():
        if not sys.stdin.isatty():
            return
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def type_writer(text, delay=0.03, ask_for_input=True, clear_screen_at_start=True):
    if clear_screen_at_start:
        clear_screen()
    clear_input_buffer() #Clear any user input from being entered while text is being printed
    for char in text:
        sys.stdout.write(char) #Write character to the terminal without a newline
        sys.stdout.flush() #Tells python to immediately print the character instead of waiting for the buffer to fill up
        time.sleep(delay) #Wait a short delay before next character
    print() #Print a newline at the end of the text
    clear_input_buffer()

    if ask_for_input:
        get_input("Press enter to continue \n") #Gives user time to read the text before clearing the screen
        clear_screen()

def main():
    clear_screen()
    type_writer(INSTRUCTIONS) #Give user game instructions
    print("----Prison Map----")
    print(STARTING_MAP)
    get_input("Press enter to start game \n")
    clear_screen()
    
    player.action()


if __name__ == "__main__":
    main()
