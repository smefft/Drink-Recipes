import requests

class Recipe:
    def __init__(self, id):
        # Access recipe API
        self.id = id
        self.response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={}'.format(self.id))
        self.token = self.response.json()
        for recipe in self.token['drinks']:
            self.recipe = dict(recipe)

    def ingredients(self):
        # create string of formatted ingredients
        self.ingredients = ''
        for i in range(30):
            for key in self.recipe:
                # get ingredient name and add to ingredients string
                if key == 'strIngredient{}'.format(i):
                    if self.recipe[key] != None and self.recipe[key] != '':
                        self.ingredients += '- '
                        self.ingredients += self.recipe[key]
                        self.ingredients += ': '
                        # get ingredient measurement and add to ingredients string
                        for key in self.recipe:
                            if key == 'strMeasure{}'.format(i):
                                if self.recipe[key] != None:
                                    self.ingredients += self.recipe[key].strip()
                                    self.ingredients += '\n'
        return self.ingredients

    def instructions(self):
        # isolate instructions
        for key in self.recipe:
            if key == 'strInstructions':
                self.instructions = self.recipe[key]
        return self.instructions

    def __str__(self):
        return ('\n----Recipe:----\n'
                'Ingredients:\n'
                '{}\n'
                '\n----Instructions:----\n'
                '{}'.format(self.ingredients(), self.instructions()))
