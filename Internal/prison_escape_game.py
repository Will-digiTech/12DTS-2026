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
import time
import sys

#VARIABLES
INSTRUCTIONS = "\nWelcome to PRISON ESCAPE \n" \
               "Your goal is to escape the prison! \n" \
               "There are three possible escape routes. Route 1 is the easiest, while Route 3 is the most difficult. \n" \
               "Do not press enter while the game  \n" \
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
KITCHEN_SHIFT = "Start Kitchen shift"
WORKSHOP_SHIFT  = "Start Workshop shift"
STEAL_FOOD = "Steal food"
HIDE_ITEM = "Hide item under bed"
GET_ITEM_BED = "Get stored items from under bed"
TAKE_GUARD_UNIFROM = "Attempt to beat up guard"
CLIMB_WALL = "Attempt to climb wall"
VENT_ESCAPE = "Climb through vent"

MESSAGE_LENGTHS = 3
LONGER_MESSAGE_LENGTHS = 5


#CLASSES
class Room:
    def __init__(self, name, room_text, actions, items, exits, npcs=None, has_visited=False):
        self.name = name
        self.room_text = room_text
        self.actions = actions
        self.items = items
        self.exits = exits
        self.npcs = npcs if npcs else []
        self.has_visited = has_visited

    def show_description(self):
        clear_screen()
        if not self.has_visited:
            type_writer(self.room_text["location"] + "\n" + self.room_text["description"])
            self.has_visited = True
        else:
            type_writer(self.room_text["location"])


class Player:
    def __init__(self, player_location, all_rooms):
        self.rooms = all_rooms

        self.player_location = player_location
        self.action_functions = {
            CHECK: self.look_around,
            MOVE: self.move_room,
            TALK: self.talk_to_prisoner,
            KITCHEN_SHIFT: self.kitchen_shift,
            WORKSHOP_SHIFT: self.workshop_shift,
            STEAL_FOOD: self.steal_food,
            HIDE_ITEM: self.hide_item,
            GET_ITEM_BED: self.get_item_from_bed,
            TAKE_GUARD_UNIFROM: self.knock_out_guard,
            CLIMB_WALL: self.climb_wall,
            VENT_ESCAPE: self.vent_escape
        }

        self.inventory = ["Makeshift weapon", "Screwdriver"]
        self.max_inventory = 3
        self.bed_inventory = []
        self.money = 10
        self.last_shift = None #Keep track of last shift to stop player doing same shift twice in a row

        self.length_of_vent_sequence = 5 #Length of direction sequence in vent mini game, can be changed to make mini game easier or harder
        self.guard_id = random.randint(10000, 99999) #Random guard ID number for final escape


    def action(self):
        while True:
            self.player_location.show_description()
        
            indexed_loop(self.player_location.actions)

            chosen_action = self.pick_from_choices("\nChoose action: ", self.player_location.actions)

            action_function = self.action_functions[chosen_action]
            action_function()
            


    def look_around(self):
        clear_screen()
        if len(self.player_location.items) > 1:
            joined_items = ", ".join(self.player_location.items[:-1]) + ' and ' + self.player_location.items[-1] #Displays items found in Enlgish
            print(f"\nYou see a {joined_items}\n")

            self.pick_up_item()

        elif self.player_location.items:
            print(f"\nYou see a {self.player_location.items[0]}\n")

            self.pick_up_item()
        else:
            display_a_message("You don't find anything", 3)
            # print("\nYou don't find anything\n")

        print() #Add space for readability


    def pick_up_item(self):
        print("Would you like to pick an item up?")

        while True:
            pick_item_choice = input("Yes/No \n>").lower()

            if pick_item_choice == "yes":

                options = self.player_location.items.copy()

                if len(options) > 1:
                    options.append("Pick up all items")

                indexed_loop(options)

                choice = self.pick_from_choices("\nChoose item to pick up: ", options)
                
                if choice == "Pick up all items":
                    for item in self.player_location.items[:]:
                        try:
                            self.add_to_inventory(item, self.player_location.items)
                        except ValueError as e:
                            print(f"\n{e}\n")

                    self.show_inventory(self.inventory, "Inventory", LONGER_MESSAGE_LENGTHS)
                    break
                    
                else:
                    try:
                        self.add_to_inventory(choice, self.player_location.items)
                    except ValueError as e:
                        print(e)

                
                self.show_inventory(self.inventory, "Inventory", LONGER_MESSAGE_LENGTHS)
                break
            elif pick_item_choice == "no":
                break
            else:
                print("Enter Yes or No")
                continue

    def add_to_inventory(self, item, remove_key):
        if len(self.inventory) >= self.max_inventory:
            raise ValueError(f"Inventory is full (max {self.max_inventory} items). Clear inventory by using items or hiding it under your bed")
        
        self.inventory.append(item)
        remove_key.remove(item)
        print(f"+{item}")


    def move_room(self):
        clear_screen()
        print("----Prison Map----")
        show_map()

        options = self.player_location.exits + ["Stay in current room"]

        indexed_loop(options)

        chosen_room = self.pick_from_choices("Choose a room to go to: ", options)

        if chosen_room == "Stay in current room":
            print("You chose to stay")
        else:
            self.player_location = self.rooms[chosen_room] #Update player location
            print(f"You chose {chosen_room}")  # Print chosen room
        

        clear_screen()


    def talk_to_prisoner(self):
        clear_screen()
        dialogue = self.player_location.npcs.dialogue
        already_spoken_to = self.player_location.npcs.already_spoken_to
        requirement_type = self.player_location.npcs.exchange["type"]
        requirement = self.player_location.npcs.exchange["requirement"]
        reward = self.player_location.npcs.exchange["reward"]


        if already_spoken_to:
            #Check if user has required items NPC is requesting.
            if requirement_type == "money": #Check if npc wants money
                if self.money >= requirement:
                    self.money -= requirement
                    self.inventory.append(reward)
                    print(dialogue["after_exchange"]) #Print dialogue for when you give npc required item
                    print(f"-${requirement}")
                    print(f"+{reward} \n")
                    self.show_inventory(self.inventory, "Inventory", MESSAGE_LENGTHS)
                    return
                
            elif requirement_type == "item": #Check if npc wants an item
                if requirement in self.inventory:
                    self.inventory.remove(requirement)
                    self.inventory.append(reward)
                    print(dialogue["after_exchange"]) #Print dialogue for when you give npc required item
                    print(f"-{requirement}")
                    print(f"+{reward} ")
                    self.show_inventory(self.inventory, "Inventory", MESSAGE_LENGTHS)
                    return


            print(dialogue["already_spoken"]) # Print dialogue for if user has already spoken to npc
        else:
            print(dialogue["intro"]) # Print dialogue for npc opening script
            self.player_location.npcs.already_spoken_to = True


    def hide_item(self):
        if self.inventory:
            options = self.inventory.copy()

            if len(options) > 1:
                options.append("Hide all items")

            indexed_loop(options)

            choice = self.pick_from_choices("\nChoose item to hide under the bed: ", options)

            if choice == "Hide all items":
                for item in self.inventory[:]:
                    self.bed_inventory.append(item)
                    self.inventory.remove(item)
                    print(f"+{item}")
                self.show_inventory(self.bed_inventory, "Bed inventory", MESSAGE_LENGTHS)

            else:
                self.bed_inventory.append(choice)
                self.inventory.remove(choice)
                print(f"+{choice}")
                self.show_inventory(self.bed_inventory, "Bed inventory", MESSAGE_LENGTHS)

        else:
            print("You don't have anything to hide")
            return

    def get_item_from_bed(self):
        while True:
            clear_screen()
            if self.bed_inventory:

                options = self.bed_inventory.copy()

                if len(options) > 1:
                    options.append("Get all items from bed")

                indexed_loop(options)

                choice = self.pick_from_choices("\nChoose item to take: ", options)

                if choice == "Get all items from bed":
                    for item in self.bed_inventory[:]:
                        try:
                            self.add_to_inventory(item, self.bed_inventory)
                        except ValueError as e:
                            print(f"\n{e}\n")

                    self.show_inventory(self.inventory, "Inventory", LONGER_MESSAGE_LENGTHS)
                    break

                else:
                    try:
                        self.add_to_inventory(choice, self.bed_inventory)
                    except ValueError as e:
                        print(f"\n{e}\n")

                self.show_inventory(self.inventory, "Inventory", LONGER_MESSAGE_LENGTHS)
                break

            else:
                display_a_message("There are no stored items under your bed", 3)
                break


    def kitchen_shift(self):
        if self.last_shift == KITCHEN_SHIFT:
            print("\nYou can't do the same shift twice in a row, choose a different shift\n")
            return

        # MINI GAME to complete kitchen shift
        correct_food_counter = 0
        num_of_lifes = 2 #Changable later if I want to give more lives
        anagram_foods = ["TOMATO", "CHEESE", "APPLE", "MILK", "POTATO", "BREAD"] #All possible foods for anagrams

        print() #Add space for readibility
        print("You started your shift in the Kitchen")
        print("You must solve these anagrams by typing the correct food.")
        print("You must get 5 correct to finish your shift")
        print(f"You have have {num_of_lifes} lives, if you fail you get kicked off your shift and earn no money.")

    
        while correct_food_counter < 5:
            chosen_food = random.choice(anagram_foods) #Choose random food from list
            list_food = list(chosen_food) #Turn the immutable string into a list
            random.shuffle(list_food) #Shuffle characters in list
            anagram = "".join(list_food) #Join shuffled list into string

            if anagram == chosen_food: #If the anagram is the same as the original word, shuffle again
                continue

            #Repeat until valid user entry
            while True:
                try:
                    print(anagram)
                    guess = input("Guess the food \n>")
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

                print("You guessed correct")
                print(f"{correct_food_counter}/5 completed \n")
                
            else:
                num_of_lifes -= 1
                print("You guessed incorrect!")
                if num_of_lifes == 0:
                    print("You failed your shift!\n")
                    self.last_shift = KITCHEN_SHIFT #Update last shift to stop player doing same shift twice in a row
                    return
                else:
                    print(f"You have used a life, you have {num_of_lifes} remaining")

        self.money += 5
        self.last_shift = KITCHEN_SHIFT #Update last shift to stop player doing same shift twice in a row
        print("Congratulations you completed your shift and earnt 5 dollars")
        print(f"You now have ${self.money} in total")

    def workshop_shift(self):

        if self.last_shift == WORKSHOP_SHIFT:
            print("\nYou can't do the same shift twice in a row, choose a different shift\n")
            return

        #MINI GAME to complete workshop shift
        completed_num_plates = 0
        num_of_lives = 2
        allowed_time = 7
        num_to_complete = 5

        print() #Add space for readibility
        print("You started your shift in the Workshop")
        print("You will get given a number plate back to front and you must type it the correct way")
        print("For example you might be given '321CBA' and you must type 'ABC123'")
        print(f"You have {allowed_time} seconds to type it or you fail your shift")
        print(f"Complete {num_to_complete} number plates to complete your shift")
        print(f"You have {num_of_lives} lives good luck!\n")
        input("Press enter to start\n")

        while completed_num_plates < num_to_complete:
            countdown()

            number_plate_letters = "".join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            number_plate_numbers = "".join(random.choices('1234567890', k=3))
            number_plate = number_plate_letters + number_plate_numbers

            print("Backwards number plate:")
            print(number_plate[::-1]) #Backwards number plate
            print("Correct number plate:")
            start = time.time()
            user_input = input("> ")
            end = time.time()
            elapsed_time = round(end - start, 2)

            if elapsed_time < allowed_time:
                if user_input.upper() == number_plate:
                    completed_num_plates += 1
                    print("You got it")
                    print(f"It took you {elapsed_time} seconds")
                    print(f"Completed number plates : {completed_num_plates}/{num_to_complete} \n")
                else:
                    num_of_lives -= 1
                    print("You typed it out incorrectly")
                    print(f"You have {num_of_lives} lives remaining \n")
            else:
                num_of_lives -= 1
                print("You ran out of time")
                print(f"It took you {elapsed_time} seconds")
                print(f"You have {num_of_lives} lives remaining \n")

            if num_of_lives == 0:
                print("You failed your shift! \n")
                self.last_shift = WORKSHOP_SHIFT #Update last shift to stop player doing same shift twice in a row
                return
            
        self.money += 5
        self.last_shift = WORKSHOP_SHIFT #Update last shift to stop player doing same shift twice in a row
        print("You successfully completed your shift and earnt 5 dollars!")
        print(f"You now have ${self.money} in total \n")

    def steal_food(self):
        print("You are trying to take someones food without getting caught")
        print("To succesfully take someones food you must press the enter button within a given time frame")
        print("Don't press enter too early or too late to take the food.")
        print("Good luck! \n")
        input("Press enter to start\n")

        while True:
            countdown()
            time_frame_min = random.randrange(2, 10)
            time_frame_max = time_frame_min + 2

            start = time.time()
            stop_timer = input(f"Press enter between {time_frame_min} and {time_frame_max} seconds. \n>")
            if stop_timer != "":
                print("Only press enter")
                continue
            end = time.time()
            elapsed_time = round(end - start, 2)

            print(f"{elapsed_time} seconds")
            if time_frame_min <= elapsed_time <= time_frame_max:
                self.inventory.append("Food")
                print("You succesfully stole food!")
                print("+Food")
                self.show_inventory(self.inventory, "Inventory", MESSAGE_LENGTHS)

                return
            else:
                print("You missed your opportunity")
                print("Try again \n")


    def vent_escape(self):
 
        if "Screwdriver" in self.inventory:
            display_a_message(vent_escape_text["Correct item"]["True"], 4)
        else:
            display_a_message(vent_escape_text["Correct item"]["False"], 4)
            return


        if self.vent_mini_game():
            display_a_message(vent_escape_text["Mini game result"]["True"], 6)
        else:
            display_a_message(vent_escape_text["Mini game result"]["False"], 6)
            game_over_lost()

        display_a_message(vent_escape_text["Final escape text"].format(guard_id=self.guard_id), 5)
        
        if self.id_check():
            game_over_won(1)
        else:
            game_over_lost()


    def vent_mini_game(self):
        directions = ["left", "right"]
        length_of_sequence = 5
        randomised_sequence = []

        print(vent_escape_text["Mini game instructions"].format(length_of_sequence=player.length_of_vent_sequence))

        print("Remeber the sequence: ")
        for i in range(length_of_sequence):
            randomised_sequence.append(random.choice(directions))
        sequence = " ".join(randomised_sequence)
        print(sequence)

        input("\nPress enter to type sequence")
        clear_screen()

        user_sequence = input("Enter sequence: \n")
        if user_sequence == sequence:
            return True
        else:
            return False



    def knock_out_guard(self):
        #Chance of escaping without a makeshift weapon (1% success rate)
        if "Makeshift weapon" not in self.inventory:
            if random.random() > 0.01:
                display_a_message("You tried to sneak attack the guard without a makeshift weapon, he beats you up.", 5)
                game_over_lost()
            else:
                display_a_message("You succesfully beat the guard with no makeshift weapon.", 4)

        else:
            display_a_message(guard_disguise_text["Attack guard text"], 5)

        #Chance of taking guards clothes wihtout getting caught (70% success rate)
        if random.random() > 0.3:
            display_a_message(guard_disguise_text["Take uniform"]["success"], 5)
        else:
            display_a_message(guard_disguise_text["Take uniform"]["fail"], 5)
            game_over_lost()

        print(guard_disguise_text["In uniform text"].format(guard_id=player.guard_id))
        input("Press enter to continue")

        if self.id_check():
            game_over_won(2)
        else:
            game_over_lost()
        
    def id_check(self):
        clear_screen()
        print(guard_disguise_text["Guard id check"])
        user_input = int(input("\nEnter guard ID number : "))

        if user_input == self.guard_id:
            print(guard_disguise_text["Correct Id"])
            return True
        else:
            print(guard_disguise_text["Incorrect Id"])
            return False


    def climb_wall(self):
        if "Grapping hook" not in self.inventory:
            display_a_message(wall_climb_escape_text["No grappling hook text"], 8)
        elif "Firework" not in self.inventory:
            display_a_message(wall_climb_escape_text["No firework text"], 8)
        else:
            clear_screen()
            print(wall_climb_escape_text["Win text"])
            game_over_won(3)



    def show_inventory(self, inventory, name, seconds):
        if inventory:
            print(f"{name}: {', '.join(inventory)} \n")
        else:
            print(f"{name} empty \n")

        time.sleep(seconds)
        clear_screen()

    def pick_from_choices(self, prompt, options):
        while True:
            try:
                choice = int(input(prompt))

                if 1 <= choice <= len(options):
                    return options[choice - 1]
                
                else:
                    print(f"Choose option between 1 - {len(options)}")

            except ValueError:
                print("Please input a valid number")



class NPC:
    def __init__(self, name, dialogue, exchange):
        self.name = name
        self.dialogue = dialogue
        self.exchange = exchange
        self.already_spoken_to = False


#NPC CLASS OBJECTS
Derek_NPC = NPC(
    "Derek",
    {"intro": "Yo, Derek is me. I got a mission for you. If you get me 10 dollars i'll give you a screwdriver. Get money from doing a shift in the Kitchen or Workshop then get back to me. \n",
     "already_spoken": "I already told you. Go get me money from a shift in the Kitchen or Workshop and you can have the screwdriver. \n",
     "after_exchange": "I appreciate it bro. Heres your screwdriver."},
    {"type": "money",
     "requirement": 10,
     "reward": "Screwdriver"}
)

Joel_NPC = NPC(
    "Joel",
    {"intro": "Hey man, I'm Joel. Look, I'm super busy at the moment and have a little task for you. I left my toothbrush in the bathroom, if you go and get it for me, i'll give you a piece of scrap metal which is great for crafting items. \n",
     "already_spoken": "Get back to me when you have my toothbrush and i'll give you the scrap metal. \n",
     "after_exchange": "Thanks man! Here's the scrap metal."},
    {"type": "item",
     "requirement": "Toothbrush",
     "reward": "Scrap metal"}
)

Bob_NPC = NPC(
    "Bob",
    {"intro": "Hello there! It's me BOB. Everyone hates me in the cafeteria, could you please please please go get me some food. If you do I'll give you this firework!!! \n",
     "already_spoken": "I'm begging you man please get me some food I'm starving! Then you can have the firework. It's perfect for a good distraction. \n",
     "after_exchange": "YAY, i've been starving for so long! Thanks so much, here's the firework!"},
    {"type": "item",
     "requirement": "Food",
     "reward": "Firework"}
)

#ROOM CLASS OBJECTS
cell = Room(
    "cell",
    {
        "location": "You are in your Cell",
        "description": "It's a small, dimly lit room with two hard beds and a window. You have a cellmate, you don't talk often. \n"
    },
    [CHECK, MOVE, TALK, HIDE_ITEM, GET_ITEM_BED], #Actions
    ["Spoon", "Fork", "Knife", "Scissors"], #Items
    ["workshop", "bathroom", "cafeteria"], #Exits
    npcs=Derek_NPC
)

cafeteria = Room(
    "cafeteria",
    {
        "location": "You are in the Cafeteria",
        "description": "It's a loud place with lots of prisoners. The food is terrible and the service is even worse. \n"
    },
    [CHECK, MOVE, STEAL_FOOD], #Actions
    [], #Items
    ["cell", "yard", "kitchen"] #Exits
)

yard = Room(
    "yard",
    {
        "location": "You are in the Yard",
        "description": "It's a long area that stretches from the West to East side of the prison. The walls look climbable with the right tools. \n"
    },
    [CHECK, MOVE, CLIMB_WALL], #Actions
    [], #Items
    ["cafeteria", "kitchen"] #Exits
)

kitchen = Room(
    "kitchen",
    {
        "location": "You are in the Kitchen",
        "description": "It's a dirty room where prisoners can do shifts to earn money. There is also a guard stationed here. \n"
    },
    [CHECK, MOVE, KITCHEN_SHIFT, TAKE_GUARD_UNIFROM], #Actions
    [], #Items
    ["cafeteria", "yard"] #Exits
)

bathroom = Room(
    "bathroom",
    {
        "location": "You are in the Bathroom",
        "description": "It's got 5 cubicles all with broken doors. A strange prisoner is sitting in the corner, muttering to himself. There is also a vent above one of the cubicles. \n"
    },
    [CHECK, MOVE, TALK, VENT_ESCAPE], #Actions
    ["Toothbrush"], #Items
    ["cell", "workshop"], #Exits
    npcs=Bob_NPC
)

workshop = Room(
    "workshop",
    {
        "location": "You are in the Workshop",
        "description": "It's a small room that offers a shift for money and a place to craft items. There is also another prisoner who spends all his time here. \n"
    },
    [CHECK, MOVE, TALK, WORKSHOP_SHIFT], #Actions
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


#Escape prison texts
vent_escape_text = {
    "Correct item": {"True": "You use your screwdriver to open the vent and climb through.", 
                    "False": "You need a screwdriver to open the vent."},
    "Mini game instructions": "You are crawing through the vent, to make sure you don't get lost you must type the correct sequence of directions. \nYou will be given a sequence of {length_of_sequence} dirrections either left or right, for example 'left, right, left, left, right'. You must type the sequence correctly to make it through the vent. \nTo type the sequence correctly seperate dirrections with a space, e.g 'left right left' \nGood luck! \n",
    "Mini game result": {"True": "You successfully make your way to the guards office and jump in.", 
                         "False": "You get lost in the vents. Eventually, the guards notice an open vent and find you."},
    "Final escape text": "You jump into the guards office and quickly hide. A guard walks in and you jump attack him, knocking him out. You take the guards uniform and his keycard. His ID number is {guard_id}. All you have to do is walk out the front door."
        
}

guard_disguise_text = {
    "Attack guard text": "You use your makeshift weapon to incapacitate the guard.",
    "Take uniform": {
        "success": "You successfully take the guards uniform without anyone catching you.",
        "fail": "You try to take the guards uniform but get caught."
    },
    "In uniform text": "You have the guards keycard and his ID number is {guard_id}. All you have to do is walk out the front door.",
    "Guard id check": "As you are walking towards the exit you see another guard. He says, 'I don't think I've seen you around before. What's your ID number?'",
    "Correct Id": "'Perfect, have a good one.', he says. You arrive at the front door and swipe your keycard.",
    "Incorrect Id": "The guard looks confused and says, 'No guard has that ID, who are you?'. Before you can think of an excuse he is handcuffing you and taking you away."

}

wall_climb_escape_text = {
    "Win text": "You go over to the East side of the prison and carefully set up the firework behind a bush. You light the firework and swiftly walk away. The firework goes off, exploding above the prison. You set up the firework a little too close to the bush and the bush catches on fire. As everyone is focused on the commotion of the fire, you make your way over to the West side. You grab your grappling hook and climb the wall. ",
    "No grappling hook text": "You need a grapping hook to climb the walls, this can be crafted by using scrap metal and rope.",
    "No firework text": "There are too many guards around, you need a distraction. Find a firework to create a distraction."
}





#FUNCTIONS
def countdown():
    print("Starting in ...")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1 \n")
    time.sleep(1)

def indexed_loop(looped_list):
    for index, value in enumerate(looped_list):
        print(f"{index + 1}: {value.capitalize()}")

def display_a_message(message, seconds):
    clear_screen()
    print(message)
    time.sleep(seconds)
    clear_screen()

def game_over_lost():
    print("Game over!")
    quit()

def game_over_won(ending):
    print("Congratulations! You successfully escaped the prison.")
    print(f"Ending {ending}/3")
    quit()

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

##Searhed this up online to clear the input from the user while text is on the screen. Game would break if user inputs something when they are not supposed to##
if os.name == 'nt':
    import msvcrt
    def clear_input_buffer():
        while msvcrt.kbhit():
            msvcrt.getch()
else:
    import termios
    def clear_input_buffer():
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


def type_writer(text, delay=0.03):
    clear_input_buffer() #Clear any user input from being entered while text is being printed
    for char in text:
        sys.stdout.write(char) #Write character to the terminal without a newline
        sys.stdout.flush() #Tells python to immediately print the character instead of waiting for the buffer to fill up
        time.sleep(delay) #Wait a short delay before next character
    print() #Print a newline at the end of the text
    clear_input_buffer()
    input("Press enter to continue \n") #Gives user time to read the text before clearing the screen
    clear_screen()


#----Game Loop----
clear_screen()
type_writer(INSTRUCTIONS) #Give user game instructions
print("----Prison Map----")
print(STARTING_MAP)
input("Press enter to start game \n")
clear_screen()

while True:
    player.action()

