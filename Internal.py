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
        "description": "",
        "items": ["Sword", "Fork", "Knife"]
    },
    "cafeteria": {},
    "yard": {},
    "laundry": {},
    "kitchen": {}
}

starting_room = rooms["cell"]


class Player:
    def __init__(self, room):
        self.room = room
        self.room_description = self.room["description"]
        self.items = room["items"]

    def look_around(self):
        if len(self.room["items"]) > 1:
            items = ", ".join(self.items[:-1]) + ' and ' + self.items[-1] #Displays items found in Enlgish
            print(f"You see a {items}")

        elif self.room["items"]:
            print(f"You see a {self.items[0]}")

        else:
            print("You don't find anything")

player = Player(starting_room)

player.look_around()
print(player.items)



