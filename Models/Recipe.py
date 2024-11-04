import requests

class Recipe:

    def __init__(self, id):
        self.id = id
        self._recipe: dict[str, str] = self._set_recipe()
        self.drink_name: str = self._set_drinkname()
        self.ingredients: list[tuple[str, str]] = self._set_ingredients()
        self.instructions: list[str] = self._set_instructions()

    def _set_recipe(self) -> dict[str, str]:
        response = requests.get(
            f'https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i={self.id}'
        )
        token: dict = response.json()
        recipe = token['drinks'][0]
        return recipe

    def _set_drinkname(self) -> str:
        return self._recipe["strDrink"]

    def _set_ingredients(self) -> list[tuple[str, str]]:
        ingredients = []
        # in json file, ingredients are named strIngredient1, strIngredient2, etc
        ing_count = 1
        while self._recipe[f"strIngredient{ing_count}"] is not None:
            ingredient = self._recipe[f"strIngredient{ing_count}"]
            measurement = self._recipe[f"strMeasure{ing_count}"]
            ingredients.append((ingredient, measurement))
            ing_count += 1
        return ingredients

    def _set_instructions(self) -> str:
        # in json file, instructions are inconsistent, sometimes numbering the steps, sometimes not.
        # that's why there is no formatting done bc it creates inconsistencies when printing
        instructions = self._recipe["strInstructions"]
        instructions = instructions.split(". ")
        return "\n".join(instructions)

    def get_drinkname(self) -> str:
        return self.drink_name

    def get_ingredients(self, as_list: bool = False) -> str or list:
        return self.ingredients if as_list else self._str_ingredients()

    def get_instructions(self) -> str:
        return self.instructions

    def get_picture(self):
        return self._recipe["strDrinkThumb"]
    
    def get_recipe(self):
        return self._recipe

    def _str_ingredients(self) -> str:
        ingredients = []
        for (ingredient_name, measurement) in self.ingredients:
            if measurement:
                ingredients.append(f"- {measurement.strip()} {ingredient_name.strip()}")
            else:
                ingredients.append(f"- {ingredient_name.strip()}")
        return "\n".join(ingredients)

    def __str__(self) -> str:
        header = f"\n---- Recipe for {self.get_drinkname()}: ----"
        ingredients = "\n".join(("Ingredients:", self.get_ingredients()))
        instructions = "\n".join(("Instructions:", self.get_instructions()))
        return "\n\n".join((header, ingredients, instructions)) + "\n"
