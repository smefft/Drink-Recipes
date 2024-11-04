from functools import partial
from View.Bases import Controller, InnerFrame # Import from View package

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
                command=partial(controller.app.get_drinklist, spirit),
                count=count)


class DrinkListFrame(InnerFrame):

    def __init__(self, controller, spirit, drinklist):
        super().__init__(controller, scrollable=True)
        self.add_header(f"Drinks with {spirit.capitalize()}: ")

        drink_names = drinklist.keys()
        button_width = max([len(drinkname) for drinkname in drink_names]) + 2
        for count, (name, drink_id) in enumerate(drinklist.items(), 1):
            self.add_button(
                text=name.title(),
                width=button_width,
                height=1,
                command=partial(controller.app.get_recipe, drink_id),
                count=count)

class RecipeFrame(InnerFrame):

    def __init__(self, controller, recipe):
        super().__init__(controller)
