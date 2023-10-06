import requests

class Recipe:
    def __init__(self, id):
        self.id = id
        self.recipe: dict = self._populate_recipe()
        self.drink_name = self.recipe["strDrink"]
        self.ingredients: list[tuple] = self._populate_ingredients()
        self.instructions: str = self._populate_instructions()

    def _populate_recipe(self):
        response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={}'.format(self.id))
        token = response.json()
        for recipe in token['drinks']:
            return recipe

    def _populate_ingredients(self):
        ingredients = []
        ing_count = 1
        while self.recipe[f"strIngredient{ing_count}"] is not None:
            ingredient = self.recipe[f"strIngredient{ing_count}"]
            measurement = self.recipe[f"strMeasure{ing_count}"]
            ingredients.append((ingredient, measurement))
            ing_count += 1
        return ingredients

    def _populate_instructions(self):
        return self.recipe["strInstructions"]

    def ingredients_as_string(self):
        string = ""
        for (ingredient, measurement) in self.ingredients:
            string += f"- {measurement} {ingredient}\n"
        return string
    
    def __str__(self):
        return ('\n----Recipe for {}:----\n'
                'Ingredients:\n'
                '{}\n'
                '\n----Instructions:----\n'
                '{}'.format(self.drink_name, self.ingredients_as_string(), self.instructions))
