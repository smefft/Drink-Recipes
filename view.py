from tkinter import *
from functools import partial
from Spirits import SPIRITS
import Drinks

# TODO 1 compartmentalize
# TODO 2 make scrollable
# TODO 4 make back and quit buttons in different spots
# TODO 5 connect drinks to recipes (make recipe screen)

class DrinkListApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('3000x1600')

        self.main_container = Frame(self)
        self.main_container.pack(side = "top", fill = "both", expand = True)

        self.main_container.grid_rowconfigure(0, weight = 1)
        self.main_container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F in (SpiritsPage,):
            frame = F(self.main_container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.show_frame(SpiritsPage)

    def show_frame(self, frame_class, spirit=None) -> None:
        if frame_class in self.frames:
            frame: Frame = self.frames[frame_class]
        elif frame_class == DrinkListPage:
            frame: Frame = DrinkListPage(self.main_container, self, spirit)
            frame.grid(row = 0, column = 0, sticky ="nsew")
        else:
            raise NotImplementedError
        frame.tkraise()

class SubFrame(Frame):
    def __init__(self, parent: Frame, controller: Tk):
        Frame.__init__(self, parent)
        self.controller = controller
    
    def _back_button(self, back_to_frame: Frame):
        back_button = Button(
            self, 
            text="Back",
            command=partial(self.controller.show_frame, back_to_frame), 
            foreground="blue",
        )
        back_button.pack(pady=4)
    
    def _quit_button(self):
        quit_button = Button(self, text="Quit", command=self.controller.destroy, foreground="red")
        quit_button.pack(pady=4)

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
                command=partial(controller.show_frame, DrinkListPage, spirit),
            )
            button.pack(pady=4)

class DrinkListPage(SubFrame):
    def __init__(self, parent: Frame, controller: Tk, spirit_name: str):
        super().__init__(parent, controller)
        self.spirit_name = spirit_name.capitalize()
        self.label = Label(self, text=f"Drinks with {self.spirit_name}:", fg="#000000")
        self.drinklist = self._get_drinklist()

        self._back_button(SpiritsPage)
        self._quit_button()
        self._drink_buttons()

    def _get_drinklist(self) -> dict:
        return Drinks.DrinkList(self.spirit_name).get_drinklist()
    
    def _drink_buttons(self):
        drinkname_lengths = [len(drinkname) for drinkname in self.drinklist]
        button_width = max(drinkname_lengths) + 2
        for drink_name in self.drinklist:
            button = Button(
                self,
                text=drink_name.capitalize(),
                width=button_width,
            )
            button.pack(pady=4)

app = DrinkListApp()
app.mainloop()
