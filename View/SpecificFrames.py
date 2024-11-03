from functools import partial
from Bases import Controller, InnerFrame

class DrinkListApp:
    def __init__(self):
        self.width = 1300
        self.height = 700
        self.title = "DrinkChooser"
        self.controller= Controller(self.width, self.height, self.title)

        first_frame = SpiritsFrame(self.controller, ["spirit2", "spirit1"]).base_frame
        self.controller.add_frame(first_frame)
        self.controller.show_next_frame()

    def run(self):
        """Starts the app"""
        self.controller.mainloop()

class SpiritsFrame(InnerFrame):
    """Sets up content of the inner frame
    New pages are added by creating an inner frame,
    which then chooses a base frame or scrollable base frame as its parent."""
    def __init__(self, controller: Controller, spirits: list[str]):
        super().__init__(controller)
        self.add_header("Pick your Spirit: ")
        for spirit in spirits:
            self.add_button(
                text=spirit.capitalize(),
                width=10,
                height=2,
                command=partial(controller.show_next_frame, DrinkListFrame, spirit),)

class DrinkListFrame(InnerFrame):
    def __init__(self, controller, spirit_name: str):
        super().__init__(controller)

app = DrinkListApp()
app.run()
