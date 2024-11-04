import requests

class DrinkNameAndId:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class DrinkDict:
    def __init__(self, spirit):
        self.spirit = spirit
        self.drinkdict: dict[str, str] = {}
        self._set_drinkdict()

    def _set_drinkdict(self) -> None:
        response = requests.get(f'https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={self.spirit}')
        json_data: dict = response.json()
        for drink_data in json_data["drinks"]:
            self.drinkdict[drink_data["strDrink"]] = drink_data["idDrink"]

    def get_drinkdict(self):
        return self.drinkdict

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