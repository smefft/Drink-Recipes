from View.Bases import Controller
from View.SpecificFrames import SpiritsFrame, DrinkListFrame
from Models.Spirits import SPIRITS
from Models.Drinks import DrinkDict

class DrinkNameAndId:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class DrinkListApp:

    def __init__(self):
        self.width = 1300
        self.height = 700
        self.title = "DrinkChooser"

        self.spirit: str
        self.drinklist: dict[str, str]

        self.controller = Controller(self, self.width, self.height, self.title)
        spirits_frame = SpiritsFrame(self.controller, SPIRITS).base_frame
        self.controller.add_frame(spirits_frame)

    def get_drinklist(self, spirit):
        self.spirit = spirit
        self.drinklist = DrinkDict(self.spirit).get_drinkdict()
        drinklist_frame = DrinkListFrame(self.controller, self.spirit, self.drinklist).base_frame
        self.controller.add_frame(drinklist_frame)

    def get_recipe(self, drink_id):
        print(drink_id)

    def run(self):
        """Starts the app"""
        self.controller.mainloop()

app = DrinkListApp()
app.run()
