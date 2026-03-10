#LIBRARIES
import random
import time

#This is a small change lollll


#Variables
wild_pokemon = [
    {"Name": "Charizard",
     "Type": "Fire",
     "Level": random.randint(1, 3),
     "Health": random.randint(1, 100),
     "Attacks": {
        "Fire Blast": 50,
        "Flame Thrower": 30,
        "Wind Blast": 15,
        }
}]
#e
own_pokemon = [
    {"Name": "Pikachu",
     "Type": "Electric",
     "Level": random.randint(1, 3),
     "Health": 100,
     "Attacks": {
         "Thunder Bolt": 25,
         "Thunder": 20,
         "Quick Attack": 10
     }
}]

seen = [None]

def overworld_timer():
    timer = random.randint(1, 2)
    print(timer)
    time.sleep(timer)
    print("Battle Begins")
    battle()

def battle():
    x = random.randint(0, len(wild_pokemon) - 1)
    enemy_pokemon = wild_pokemon[x]
    enemy_pokemon_name = enemy_pokemon["Name"]
    enemy_pokemon_hp = enemy_pokemon["Health"]


    player_pokemon = own_pokemon[0]
    player_pokemon_name = player_pokemon["Name"]
    player_pokemon_hp = player_pokemon["Health"]
    player_pokemon_attacks = player_pokemon["Attacks"]
    last_attack = None


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
            choice = int(input("Press 1 to fight, press 2 to run: "))
            if choice == 1:
                break
            elif choice == 2:
                pass
        except ValueError:
            print("Enter 1 or two")


    #Battle Begins
    while True:
        enemy_attack_randomiser = random.randint(0, len(enemy_pokemon['Attacks']) - 1)
        enemy_attack = list(enemy_pokemon['Attacks'].keys())[enemy_attack_randomiser]
        enemy_attack_damage = enemy_pokemon['Attacks'][enemy_attack]

        print("\nBattle Begins")
        print(f"Random number for attack: {enemy_attack_randomiser}")
        print(f"{enemy_pokemon['Name']} attacks with {enemy_attack} and deals {enemy_attack_damage} damage")


        player_pokemon_hp -= enemy_attack_damage

        if player_pokemon_hp <= 0:
            print("Your Pokemon died!")
            break
        else:
            print(f"{player_pokemon_name} now has {player_pokemon_hp} HP\n")

        player_attack(player_pokemon_attacks, seen, enemy_pokemon_name, enemy_pokemon_hp)

        if enemy_pokemon_hp <= 0:
            print(f"{enemy_pokemon_name} has died!")
            break


# def attack_cooldown(player_pokemon, last_attack, chosen_attack):
#
#     for i in player_pokemon["Attacks"]:
#         print(i)

def player_attack(player_pokemon_attacks, seen, enemy_pokemon_name, enemy_pokemon_hp):
    while True:
        attacks = list(player_pokemon_attacks.keys())

        for i, attack in enumerate(attacks):
            damage = player_pokemon_attacks[attack]
            print(f"Choose {i + 1} for {attack}, it deals {damage} damage")


        try:
            choice = int(input("Choose number for attack: "))

            if 1 <= choice <= len(player_pokemon_attacks):
                index_attack = choice - 1
                chosen_attack = attacks[index_attack]


            if seen[-1] == chosen_attack:
                print("Already used this attack, choose another")
                continue
            seen.append(chosen_attack)

            chosen_attack_damage = player_pokemon_attacks[chosen_attack]
            enemy_pokemon_hp -= chosen_attack_damage
            print(f"\n{enemy_pokemon_name} now has {enemy_pokemon_hp} HP")

            return


        except ValueError:
            print("Enter valid number")

        except IndexError:
            print("Choose one of the attacks")








overworld_timer()
print("Done boi")