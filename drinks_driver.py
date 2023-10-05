import json
from Drinks import Drinks
from Recipe import Recipe

def print_list_of_spirits() -> None:
    print("Spirits to choose from:\n"
      "    Gin\n"
      "    Tequila\n"
      "    Vodka\n"
      "    Rum\n"
      "    Whiskey\n"
      "    Brandy\n"
      "    Bourbon\n")
    
def set_user_spirit() -> str:
    spirit = ""
    spirits = ['gin', 'tequila', 'vodka', 'rum', 'whiskey','brandy', 'bourbon']
    while spirit not in spirits:
        spirit = input('Choose your spirit:\n').strip().lower()
        if spirit not in spirits:
            print(f"You picked {spirit}, which is not on the list. Please pick a spirit from the list.")
    return spirit

def get_drink_list(spirit):
    drink_list = Drinks()
    drink_list.populate_drinklist(spirit)
    return drink_list

def get_confirmation() -> bool:
    user_input = input("Confirm? y/n: ")
    return user_input.strip().lower() in ("yes", "y")

def set_user_drink(drink_list: Drinks()):
    confirm = False
    while not confirm:
        user_index = input("Enter the number of the drink you'd like to see the recipe of: ")
        user_drink = None
        while user_drink is None:
            user_drink = drink_list.pick_drink_with_index(int(user_index))
            print(f"You picked {user_drink}.")
            confirm = get_confirmation()
    return user_drink

def print_recipe(drink, drink_list):
    drink_id = drink_list.get_drink_id(drink)
    print(Recipe(drink_id))

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

if __name__ == "__main__":
    print("\n---Welcome to your personal drink generator---\n")
    print_list_of_spirits()

    spirit = set_user_spirit()
    drink_list = get_drink_list(spirit)
    drink_list.print_drinklist()
    user_drink = set_user_drink(drink_list)

    print_recipe(user_drink, drink_list)

