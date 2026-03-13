#Prison Escape Game
#Start in cell
#Can go to: Cafeteria, Yard, Laundry, Kitchen(Shift for money)
#Inventory starts empty
#Items are randomly scattered around rooms
#Hold a maximum of 3 items, hide item under bed to get rid of item or use it
#Rooms that you can only get to with specific items, such as vents with a screwdriver



#Variables
instructions = "\nWelcome to PRISON ESCAPE \n" \
               "Your goal is to escape the prison! \n" \
               "Each playthrough the items to help you escape are randomly littered throughout the rooms \n" \
               "Type restart at anytime to restart \n" \
               "Type quit at anytime to stop playing \n" \
               "Good Luck!!! \n"


class Room():
    def __init__(self, description, actions, items, exits):
        self.description = description
        self.actions = actions
        self.items = items
        self.exits = exits

    def show_description(self):
        print(self.description)


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
                continue

            if choice == 1:
                self.look_around()
            elif choice == 2:
                self.move_room()
            elif choice == 3:
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
            for index, value in enumerate(self.player_location.exits):
                print(f"{index + 1}: {value.capitalize()}")

            try:
                choice = int(input("Choose a room to go to: "))

                if 1 <= choice <= len(self.player_location.exits):
                    index_choice = choice - 1 #Get the index of users choice
                    
                    chosen_room = self.player_location.exits[index_choice]
                    print(f"You chose {chosen_room.capitalize()}") #Print chosen room

                    self.player_location = self.rooms[chosen_room] #Update player location
                    break
                    
                else:
                    print(f"Choose option between 1 and {len(self.player_location.exits)}")

            except ValueError:
                print("Please input a valid number")
                continue

        print() #Add space for readability
        print(self.player_location.description) #Print new location to terminal


    def talk_to_npc(self):
        #CODE FOR TALKING TO NPC
        self.hi = 'hello'  #TEMPORARY line, avoid getting static error
        print("You chose chat to NPC")

        print() #Add space for readability



cell = Room(
    "You are in your Cell. \nIt's a small, dimly lit room with two hard beds and a window. You have a cellmate, you don't talk often. \n", #Description
    ["Check room for items", "Move room", "Talk to cellmate"], #Actions
    ["Sword", "Fork", "Knife"], #Items
    ["workshop", "bathroom", "cafeteria"] #Exits
)

cafeteria = Room(
    "You are in the Cafeteria. \nIt's a loud place with", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cell", "yard", "kitchen"] #Exits
)

yard = Room(
    "You are in the Yard. \n", #Description
    ["Check room for items", "Move room"], #Actions``
    [], #Items
    ["cafeteria", "kitchen"] #Exits
)

kitchen = Room(
    "You are in the Kitchen. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cafeteria", "yard"] #Exits
)

bathroom = Room(
    "You are in the Bathroom. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cell", "workshop"] #Exits
)

workshop = Room(
    "You are in the Workshop. \n", #Description
    ["Check room for items", "Move room"], #Actions
    [], #Items
    ["cell", "bathroom"] #Exits
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
print(player.player_location.description) #Starting room description

while True:
    player.action()
    # player.look_around()
    # player.move_room()


