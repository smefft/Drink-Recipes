from tkinter import *
from functools import partial
from Spirits import SPIRITS
import Drinks
from Recipe import Recipe

# TODO 1 compartmentalize
# TODO 2 make scrollable
# TODO 4 make back and quit buttons in different spots
# TODO 5 connect drinks to recipes (make recipe screen)


class DrinkListApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.geometry('3000x1600')
        self.title("DrinkChooser")

        self.main_container = Frame(self)
        self.main_container.pack(side="top", fill="both", expand=True)

        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.frames: list[Frame] = []

        self.show_next_frame(SpiritsPage)
    
    def add_frame(self, frame):
        self.frames.append(frame)
    
    def remove_last_frame(self):
        del self.frames[-1]

    def show_next_frame(self, page, *args) -> None:
        frame = page(self.main_container, self, *args)
        frame.grid(row=0, column=0, sticky="nsew")
        self.add_frame(frame)
        frame.tkraise()
    
    def show_previous_frame(self) -> None:
        self.remove_last_frame()
        frame = self.frames[-1]
        frame.tkraise()


class SubFrame(Frame):
    def __init__(self, parent: Frame, controller: Tk):
        Frame.__init__(self, parent)
        self.parent = parent
        self.controller: Tk = controller

    def _back_button(self, **kwargs):
        back_button = Button(
            self,
            text="< Back",
            command=self.controller.show_previous_frame,
            foreground="blue",
        )
        back_button.pack(anchor="nw", side="top", pady=4, padx=4)

    def _quit_button(self):
        quit_button = Button(self, text="Quit", command=self.controller.destroy, foreground="red")
        quit_button.pack(anchor="ne", side="top", pady=4, padx=4)

class SpiritsPage(SubFrame):
    def __init__(self, parent: Frame, controller: Tk):
        super().__init__(parent, controller)
        label = Label(self, text="Pick your Spirit: ", fg="#000000")
        label.pack(pady=4)

        self._quit_button()

        for spirit in SPIRITS:
            button = Button(
                self,
                text=spirit.capitalize(),
                width=10,
                height=2,
                command=partial(controller.show_next_frame, DrinkListPage, spirit),
            )
            button.pack(pady=4)


class DrinkListPage(SubFrame):
    @property
    def drinklist(self):
        return self._drinklist
    @drinklist.setter
    def drinklist(self, value):
        assert isinstance(value, Drinks.DrinkList)
        self._drinklist = value

    def __init__(self, parent: Frame, controller: Tk, spirit_name: str):
        super().__init__(parent, controller)
        self.spirit_name = spirit_name.capitalize()
        self.drinklist = Drinks.DrinkList(self.spirit_name)
        self.drinknames = self._get_drinknames()

        self._header()
        self._back_button()
        self._quit_button()
        self._drink_buttons()

    def _header(self):
        self.label = Label(self,
                           text=f"Drinks with {self.spirit_name}:",
                           fg="#000000")
        self.label.pack(pady=4)

    def _get_drinknames(self) -> dict:
        return self.drinklist.get_drinklist()
    
    def _get_drinkid(self, drinkname):
        return self.drinklist.get_drink_id(drinkname)

    def _drink_buttons(self):
        drinkname_lengths = [len(drinkname) for drinkname in self.drinknames]
        button_width = max(drinkname_lengths) + 2
        for drinkname in self.drinknames:
            assert isinstance(drinkname, str)
            drink_id = self._get_drinkid(drinkname)
            button = Button(
                self,
                text=drinkname.title(),
                width=button_width,
                command=partial(
                    self.controller.show_next_frame, RecipePage, drink_id)
            )
            button.pack(pady=4)


class RecipePage(SubFrame):

    @property
    def recipe(self):
        recipe = self._recipe
        assert isinstance(recipe, Recipe)
        return recipe
    @recipe.setter
    def recipe(self, value):
        assert isinstance(value, Recipe)
        self._recipe = value

    def __init__(self, parent: Frame, controller: Tk, drink_id: str):
        super().__init__(parent, controller)
        self.drink_id = drink_id
        self.recipe = self._get_recipe()
        self._back_button()
        self._quit_button()
        self.display_recipe()

    def display_recipe(self):
        self._header()
        self._ingredients()
        self._instructions()
        # self._photo()
    
    def _photo(self):
        picture = self.recipe.get_picture()
        if picture:
            recipe_picture = PhotoImage(master=self, data=picture)

    def _header(self):
        drinkname = self.recipe.get_drinkname()
        # TODO make bigger
        recipe_header = Label(self, text=drinkname.title(), fg='#000000')
        recipe_header.pack(pady=4)
    
    def _ingredients(self):
        ingredients = self.recipe.get_ingredients()
        recipe_ingredients = Label(self, text=ingredients, fg='#000000', justify='left')
        recipe_ingredients.pack(pady=4)
    
    def _instructions(self):
        instructions = self.recipe.get_instructions()
        recipe_instructions = Label(self, text=instructions, fg='#000000', justify='left')
        recipe_instructions.pack(pady=4)

    def _get_recipe(self):
        return Recipe(self.drink_id)

app = DrinkListApp()
app.mainloop()
