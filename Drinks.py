import requests

class Drinks:
    def __init__(self, spirit):
        # Access API of chosen spirit
        self.spirit = spirit
        self.response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/filter.php?i={}'.format(spirit))
        self.drinklist = self.response.json()

    def drinks(self):
        # split data into separate drinks - containing drink id, name, and jpg
        self.drink_info = []
        self.drink_names = []

        for drink_info in self.drinklist['drinks']:
            self.drink_info.append(drink_info)

        # isolate drink name
        for drink_name in self.drink_info:
            for key in drink_name:
                if key == 'strDrink':
                    self.drink_names.append(drink_name[key])

        # print all drink names
        print('\nDrink Options:')
        for drink in self.drink_names:
            print(drink)