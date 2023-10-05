import requests

class Drinks:
    def __init__(self):
        self.drink_names = []
        self.drink_infos = []

    def populate_drinklist(self, spirit):
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
    
    def pick_drink_with_index(self, index:int):
        try:
            drink = self.drink_names[index-1]
            return drink
        except IndexError:
            print(f"Pick a number between 1 and {len(self.drink_names)}")
            return None
    
    def get_drink_id(self, drink):
        for drink_info in self.drink_infos:
            if drink_info["strDrink"] == drink:
                return drink_info["idDrink"]
