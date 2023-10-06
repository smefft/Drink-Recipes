import requests
from helper_functions import get_confirmation

class DrinkList:
    def __init__(self, spirit):
        self.spirit = spirit
        self.drink_names = []
        self.drink_infos: list[dict] = []
        self._populate_drinklist(spirit)
    
    def _populate_drinklist(self, spirit):
        self.spirit = spirit
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={}'.format(spirit))
        json_data: dict = response.json()
        for drink_info in json_data["drinks"]:
            self.drink_infos.append(drink_info)
            self.drink_names.append(drink_info["strDrink"])
    
    def print_drinklist(self):
        print(f"Drinks with {self.spirit}:")
        for index, drink_name in enumerate(self.drink_names, 1):
            print(f"{index}: {drink_name}")
    
    def prompt_user_for_drink(self):
        self.print_drinklist()
        confirm = False
        while not confirm:
            user_drink = None
            while user_drink is None: 
                user_index = int(input("Enter the number of the drink you'd like to see the recipe of: ")) - 1
                user_drink = self.pick_drink_with_index(user_index)
            confirm = get_confirmation(user_drink)
        return self.drink_infos[user_index]
    
    def pick_drink_with_index(self, index:int) -> dict:
        try:
            drink = self.drink_names[index]
            return drink
        except IndexError:
            print(f"Pick a number between 1 and {len(self.drink_names)}")
            return None
    
    def get_drink_id(self, drink):
        for drink_info in self.drink_infos:
            if drink_info["strDrink"] == drink:
                return drink_info["idDrink"]

class Drink:
    def __init__(self, drink_info: dict):
        self.drink_name = drink_info["strDrink"]
        self.drink_picture = drink_info["strDrinkThumb"]
        self.drink_id = drink_info["idDrink"]
    
    def get_drink_picture(self):
        return self.drink_picture
    
    def get_drink_id(self):
        return self.drink_id
    
    def get_drink_name(self):
        return self.drink_name