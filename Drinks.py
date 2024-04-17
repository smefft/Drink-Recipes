import requests
from helper_functions import get_confirmation

class DrinkList:
    def __init__(self, spirit):
        self.spirit = spirit
        self.drinklist: dict[str, dict] = self._set_drinklist()
    
    def _set_drinklist(self):
        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={self.spirit}')
        json_data: dict = response.json()
        drinklist = {}
        for drink_data in json_data["drinks"]:
            drink_name = drink_data["strDrink"]
            drinklist[drink_name] = drink_data
        return drinklist
    
    def get_drinklist(self):
        return self.drinklist
    
    def print_drinklist(self):
        print(f"Drinks with {self.spirit}:")
        for index, drink_name in enumerate(self.drinklist.keys(), 1):
            print(f"{index}: {drink_name}")
    
    def pick_drink_with_index(self, index:int) -> dict:
        try:
            drink = self.drinklist.keys()[index]
            return drink
        except IndexError:
            print(f"Pick a number between 1 and {len(self.drinklist.keys())}")
            return None
    
    def get_drink_id(self, drink):
        for drink_name, drink_info in self.drinklist.items():
            if drink_name == drink:
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