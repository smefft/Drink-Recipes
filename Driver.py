from View.BaseFrames import Controller, ButtonObserver
from View.SpecificFrames import SpiritsFrame, DrinkListFrame, RecipeFrame
from Models.Spirits import SPIRITS
from Models.Drinks import DrinkDict
from Models.Recipe import Recipe

class DrinkNameAndId:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class DrinkListApp(ButtonObserver):

    def __init__(self):
        self.width = 1300
        self.height = 700
        self.title = "DrinkChooser"

        self.controller = Controller(self, self.width, self.height, self.title)
        self.navigation = {
            "back": self.controller.show_previous_frame,
            "spirit": self.get_drinklist,
            "drink_id": self.get_recipe,
        }

    def process_button_clicked(self, button_info: tuple[str, str]):
        """Overrides ButtonObserver.process_button_clicked"""
        (item_type, item) = button_info
        func = self.navigation.get(item_type)
        if func:
            func(item)
        else:
            print(f"No function implemented for item type {item_type}")

    def get_drinklist(self, spirit):
        drinklist = DrinkDict(spirit).get_drinkdict()
        drinklist_frame = DrinkListFrame(self.controller, spirit, drinklist).base_frame
        self.controller.add_frame(drinklist_frame)

    def get_recipe(self, drink_id):
        recipe = Recipe(drink_id)
        recipe_name = recipe.get_drinkname()
        ingredients = recipe.get_ingredients()
        instructions = recipe.get_instructions()
        recipe_frame = RecipeFrame(self.controller, recipe_name.title(), ingredients, instructions) # TODO ingredients not showing
        self.controller.add_frame(recipe_frame)

    def run(self):
        """Starts the app"""
        spirits_frame = SpiritsFrame(self.controller, SPIRITS).base_frame
        self.controller.add_frame(spirits_frame)
        self.controller.mainloop()

app = DrinkListApp()
app.run()
