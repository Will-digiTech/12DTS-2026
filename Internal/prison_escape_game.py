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
KITCHEN_SHIFT = "Start Kitchen shift"
WORKSHOP_SHIFT  = "Start Workshop shift"

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
            KITCHEN_SHIFT: self.kitchen_shift,
            WORKSHOP_SHIFT: self.workshop_shift,
        }

        self.money = 0
        self.last_shift = None #Keep track of last shift to stop player doing same shift twice in a row

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
                print(anagram_foods)
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
            print("Starting in ...")
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1 \n")
            time.sleep(1)

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

            
            
            

class NPC:
    def __init__(self, name, dialogue, item):
        self.name = name
        self.dialogue = dialogue
        self.required_item = item
        self.already_spoken_to = False


#NPC CLASS OBJECTS
Derek_NPC = NPC(
    "Derek",
    ["Yo, Derek is me. I got a mission for you. If you get me 10 dollars i'll give you a screwdriver. Get money from doing a shift in the Kitchen or Workshop then get back to me. \n",
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
    [CHECK, MOVE, TALK, WORKSHOP_SHIFT], #Actions
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
    [CHECK, MOVE, KITCHEN_SHIFT], #Actions
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


