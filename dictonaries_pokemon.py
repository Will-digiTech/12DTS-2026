#LIBRARIES
import random
import time

#Variables
wild_pokemon = [
    {"Name": "Charizard", "Type": "Fire", "Level": random.randint(1, 3), "Health": random.randint(1, 100), "Attack": ["FireBlast", 30]}
]

own_pokemon = [{"Name": "Pikachu", "Type": "Electric", "Level": random.randint(1, 3), "Health": random.randint(1, 100), "Attacks": ["Volt Tackle", 25]}]

def overworld_timer():
    timer = random.randint(1, 5)
    print(timer)
    time.sleep(timer)
    print("Battle Begins")
    battle()

def battle():
    x = random.randint(0, len(wild_pokemon) - 1)
    enemy_pokemon = wild_pokemon[x]
    player_pokemon = own_pokemon[0]
    player_pokemon_hp = player_pokemon["Health"]

    #Show player Pokemon
    print(f"Player pokemon: {player_pokemon['Name']}")
    print(f"Player pokemon HP: {player_pokemon_hp}\n")

    #Show enemy Pokemon
    print(f"A wild {enemy_pokemon['Name']} has appeared")
    print(f"It's a {enemy_pokemon['Type']} type Pokemon")
    print(f"It's level is {enemy_pokemon['Level']}")
    print(f"It has {enemy_pokemon['Health']} health")


    while True:
        try:
            choice = input(int("Press 1 to fight, press 2 to run: "))

        except ValueError:
            print("Enter 1 or two")

        if choice == 1:
            break
        elif choice == 2:
            pass

    #Battle Begins
    while True:
        enemy_attack_randomiser = random.randrange(start=0, stop=3, step=2)
        print(f"Random number for attack: {enemy_attack_randomiser}")
        print(f"{enemy_pokemon['Name']} attacks with {enemy_pokemon['Attack'][enemy_attack_randomiser]}")



overworld_timer()