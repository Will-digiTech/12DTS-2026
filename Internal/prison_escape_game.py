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


class Room():
    def __init__(self, description, actions, items, exits):
        self.description = description
        self.actions = actions
        self.items = items
        self.exits = exits


class Player:
    def __init__(self, player_location, all_rooms):
        self.rooms = all_rooms

        self.player_location = player_location

        self.hi = 'hi' #TEMPORARY line, avoid getting static error

    def action(self):
        while True:
            for index, action in enumerate(self.player_location.actions):
                print(f"{index + 1}: {action}")

            try:
                choice = int(input("Choose action: "))

            except ValueError:
                print("Please input a valid number")

            if choice == 1:
                self.look_around()
                break
            elif choice == 2:
                self.move_room()
                break
            elif choice == 3:
                self.talk_to_npc()
                break
            else:
                print()
                continue


    def look_around(self):
        if len(self.player_location.items) > 1:
            joined_items = ", ".join(self.player_location.items[:-1]) + ' and ' + self.player_location.items[-1] #Displays items found in Enlgish
            print(f"\nYou see a {joined_items}")

        elif self.player_location.items:
            print(f"You see a {self.player_location.items[0]}")

        else:
            print("You don't find anything")

        print() #Add space for readability


    def move_room(self):
        print() #Add space for readability
        while True:
            for index, value in enumerate(self.player_location.exits):
                print(f"{index + 1}: {value.capitalize()}")

            try:
                choice = int(input("Choose a room to go to: "))

                if 1 <= choice <= len(self.player_location.exits):
                    index_choice = choice - 1 #Get the index of users choice
                    
                    chosen_room = self.player_location.exits[index_choice]
                    print(f"You choose {chosen_room.capitalize()}") #Print chosen room

                    self.player_location = self.rooms[chosen_room] #Update player location
                    break
                    
                else:
                    print(f"Choose option between 1 and {len(self.player_location.exits)}")

            except ValueError:
                print("Please input a valid number")
                continue

        print() #Add space for readability


    def talk_to_npc(self):
        #CODE FOR TALKING TO NPC
        self.hi = 'hello'  #TEMPORARY line, avoid getting static error
        print("You chose chat to NPC")

        print() #Add space for readability



cell = Room(
    "You are in your cellroom",
    ["Check room for items", "Move room", "Talk to cellmate"],
    ["Sword", "Fork", "Knife"],
    ["workshop", "bathroom", "cafeteria"]
)

cafeteria = Room(
    "",
    ["Check room for items", "Move room"],
    [],
    ["cell", "yard", "kitchen"]
)

yard = Room(
    "",
    ["Check room for items", "Move room"],
    [],
    ["cafeteria", "kitchen"]
)

kitchen = Room(
    "",
    ["Check room for items", "Move room"],
    [],
    ["cafeteria", "yard"]
)

bathroom = Room(
    "",
    ["Check room for items", "Move room"],
    [],
    ["cell", "workshop"]
)

workshop = Room(
    "",
    ["Check room for items", "Move room"],
    [],
    ["cell", "bathroom"]
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


#----Game Loop----
print(instructions) #Give user game instructions

while True:
    player.action()
    # player.look_around()
    # player.move_room()


