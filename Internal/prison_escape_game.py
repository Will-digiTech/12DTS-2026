#Prison Escape Game
#Start in cell
#Can go to: Cafeteria, Yard, Laundry, Kitchen(Shift for money)
#Inventory starts empty
#Items are randomly scattered around rooms
#Hold a maximum of 3 items, hide item under bed to get rid of item or use it
#Rooms that you can only get to with specific items, such as vents with a



#Variables
instructions = "\nWelcome to PRISON ESCAPE \n" \
               "Your goal is to escape the prison! \n" \
               "Each playthrough the items to help you escape are randomly littered throughout the rooms \n" \
               "Type restart at anytime to retry \n" \
               "Type quit at anytime to stop playing \n" \
               "Good Luck!!! \n"


rooms = {
    "cell": {
        "description": "You are in your cellroom",
        "actions": ["Check room for items", "Move room", "Talk to cellmate"],
        "items": ["Sword", "Fork", "Knife"],
        "exits": ["workshop", "bathroom", "cafeteria"]
    },
    "cafeteria": {
        "description": "",
        "items": [],
        "exits": ["cell", "yard", "kitchen"]
    },
    "yard": {
        "description": "",
        "items": [],
        "exits": ["cafeteria", "kitchen"]
    },
    "kitchen": {
        "description": "",
        "items": [],
        "exits": ["cafeteria", "yard"]
    },
    "bathroom": {
        "description": "",
        "items": [],
        "exits": ["cell", "workshop"]
    },
    "workshop": {
        "description": "",
        "items": [],
        "exits": ["cell", "bathroom"]
    }
}

starting_room = rooms["cell"]


class Player:
    def __init__(self, player_location, all_rooms):
        self.rooms = all_rooms

        self.player_location = player_location
        self.room_description = self.player_location["description"]
        self.player_actions  = self.player_location["actions"]

        self.hi = 'hi' #TEMPORARY line, avoid getting static error

    def action(self):
        while True:
            for index, action in enumerate(self.player_actions):
                print(f"{index + 1}: {action}")

            try:
                choice = int(input("Choose action: "))

            except ValueError:
                print("Please input a valid number")

            if choice == 1:
                player.look_around()
                break
            elif choice == 2:
                player.move_room()
            elif choice == 3:
                player.talk_to_npc()
            else:
                print()
                continue
        


    def look_around(self):
        items = self.player_location["items"]

        if len(items) > 1:
            joined_items = ", ".join(items[:-1]) + ' and ' + items[-1] #Displays items found in Enlgish
            print(f"\nYou see a {joined_items}")

        elif items:
            print(f"You see a {items[0]}")

        else:
            print("You don't find anything")

        print() #Add space for readability

    def move_room(self): #NEED TO FIX THIS. When player changes room the exits for that room should show instead of the ones for cell.
        print() # Add space for readability
        exits = self.player_location["exits"]
        while True:
            for index, value in enumerate(exits):
                print(f"{index + 1}: {value.capitalize()}")

            try:
                choice = int(input("Choose a room to go to: "))

                if 1 <= choice <= len(exits):
                    index_choice = choice - 1 #Get the index of users choice
                    
                    chosen_room = exits[index_choice]
                    print(f"You choose {chosen_room.capitalize()}") #Print chosen room

                    self.player_location = self.rooms[chosen_room] #Update player location
                    break
                    
                else:
                    print(f"Choose option between 1 and {len(exits)}")

            except ValueError:
                print("Please input a valid number")
                continue

        print() #Add space for readability

    def talk_to_npc(self):
        #CODE FOR TALKING TO NPC
        self.hi = 'hello'  #TEMPORARY line, avoid getting static error
        print("You chose chat to NPC")

        print() #Add space for readability



player = Player(starting_room, rooms)


#----Game Loop----
print(instructions) #Give user game instructions

while True:
    player.action()
    # player.look_around()
    # player.move_room()


