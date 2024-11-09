from functools import partial
from View.BaseFrames import Controller, InnerFrame # Import from View package

class SpiritsFrame(InnerFrame):
    """Sets up content of the inner frame
    New pages are added by creating an inner frame,
    which then chooses a base frame or scrollable base frame as its parent."""
    def __init__(self, controller: Controller, spirits: list[str]):
        super().__init__(controller)
        self.add_header("Pick your Spirit: ")
        for count, spirit in enumerate(spirits, 1):
            self.add_button(
                text=spirit.capitalize(),
                width=10,
                height=2,
                button_info=("spirit", spirit),
                row=count,
                column=2)
        # command pass in dict with {"spirit": spirit}. Update the observer to take a dictionary

class DrinkListFrame(InnerFrame):

    def __init__(self, controller, spirit: str, drinklist):
        super().__init__(controller, scrollable=True)
        self.add_back_button()
        self.add_header(f"Drinks with {spirit.capitalize()}: ")

        drink_names = drinklist.keys()
        button_width = max([len(drinkname) for drinkname in drink_names]) + 2
        for count, (name, drink_id) in enumerate(drinklist.items(), 1):
            self.add_button(
                text=name.title(),
                width=button_width,
                height=1,
                button_info=("drink_id", drink_id),
                row=count,
                column=2)

class RecipeFrame(InnerFrame):

    def __init__(self, controller, recipe_name, instructions, ingredients):
        super().__init__(controller)
        self.add_back_button()

        self.add_header(recipe_name)
        self.add_label(instructions, 1)
        self.add_label(ingredients, 2)
