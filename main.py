import json
from Drinks import Drinks
from Recipe import Recipe


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def drink_id(drink_choice, drink_list):
    info = {}
    # find chosen drink in original list of drinks with user spirit
    for drink_info in drink_list:
        for key in drink_info:
            if drink_info[key]== drink_choice:
                info.update(dict(drink_info))
    # isolate drink ID
    for key in info:
        if key == 'idDrink':
            drink_id = info['idDrink']
            return drink_id

spirits = ['gin', 'tequila', 'vodka', 'rum', 'whiskey','brandy', 'bourbon']
# Get user's spirit of choice
spirit = input('Choose your spirit:\n').strip().lower()

# Check if spirit is actually a spirit
if spirit in spirits:
    user_drinks = Drinks(spirit)
    user_drinks.drinks() # print list of drinks with chosen spirits
    chosen_drink = input('\nPlease choose:\n').strip()
    # have user choose a drink from the list
    if chosen_drink in user_drinks.drink_names:
        #get drink id from original API data
        chosen_drink_id = drink_id(chosen_drink, user_drinks.drink_info)
        recipe = Recipe(chosen_drink_id) #access recipe API for chosen drink using drink id
        print(recipe)
    else:
        print('Sorry, that drink is not on the list.')
else:
    print('Sorry, we don\'t know that spirit.')




