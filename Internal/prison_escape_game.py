#Prison Escape Game
#Start in cell
#Can go to: Cafeteria, Yard, Laundry, Kitchen(Shift for money)
#Inventory starts empty
#Items are randomly scattered around rooms
#Hold a maximum of 3 items, hide item under bed to get rid of item or use it
#Rooms that you can only get to with specific items, such as vents with a

print() #Add space at top

#Variables
instructions = "\nWelcome to PRISON ESCAPE \n" \
               "Your goal is to escape the prison! \n" \
               "Each playthrough the items to help you escape are randomly littered throughout the rooms \n" \
               "Type restart at anytime to retry \n" \
               "Type quit at anytime to stop playing \n" \
               "Good Luck!!!"


rooms = {
    "cell": {
        "description": "You are in your cellroom",
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
        self.items = player_location["items"]
        self.exits = player_location["exits"]

    def look_around(self):
        if len(self.player_location["items"]) > 1:
            items = ", ".join(self.items[:-1]) + ' and ' + self.items[-1] #Displays items found in Enlgish
            print(f"You see a {items}")

        elif self.player_location["items"]:
            print(f"You see a {self.items[0]}")

        else:
            print("You don't find anything")

    def move_room(self):
        while True:
            for index, value in enumerate(self.exits):
                print(f"{index + 1}: {value.capitalize()}")

            try:
                choice = int(input("Choose a room to go to: "))

                if 1 <= choice <= len(self.exits):
                    index_choice = choice - 1 #Get the index of users choice
                    
                    chosen_room = self.exits[index_choice]
                    print(f"You choose {chosen_room.capitalize()}") #Print chosen room

                    self.player_location = self.rooms[chosen_room] #Update player location
                    break

            except ValueError:
                print("Please input a valid number")
                continue



player = Player(starting_room, rooms)

player.look_around()
player.move_room()





