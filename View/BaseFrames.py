from tkinter import *
from functools import partial

class ButtonObserver:
    """Observer for buttons. Updates when a button is clicked"""
    def process_button_clicked(self, button_info):
        pass
    
class ButtonSubject:
    """Subject for buttons. Notifies observers when a button is clicked"""
    def __init__(self):
        self.observers: list[ButtonObserver] = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        self.observers.remove(observer)
    
    def notify_observers(self, button_info):
        for observer in self.observers:
            observer.process_button_clicked(button_info)

class Controller(Tk):
    """Controller class for controling the flow of the app and its frames"""

    def __init__(self, app, width=1000, height=600, title="New App"):
        """Sets up the root window and controls of a new app

        Args:
            width: width of the root window (defaults to 1000)
            height: height of the root window (defaults to 600)
            title: title of the new app (defaults to "New App")     
    """
        Tk.__init__(self)
        self.geometry(f'{width}x{height}')
        self.title(title)

        # used to pass information to the app using the controller
        self.button_subject = ButtonSubject()
        self.button_subject.add_observer(app)

        self.main_canvas = Canvas(self)
        self.main_canvas.pack(side="top", fill="both", expand=True)
        self.main_canvas.grid_rowconfigure(0, weight=1)
        self.main_canvas.grid_columnconfigure(0, weight=1)

        # list keeps track of the order of frames, since they are dynamic
        # last frame is the one on top
        self.frames: list[Frame] = []

    def get_main_canvas(self) -> Canvas:
        """Getter for main_canvas

        Returns:
            Canvas: main_canvas
        """
        return self.main_canvas

    def add_frame(self, frame):
        self.frames.append(frame)

    def _get_next_frame(self):
        return self.frames[-1]

    def _remove_current_frame(self):
        """Because each spirit and each drink have their own lists, 
        the current frame needs to be deleted when going back"""
        del self.frames[-1]

    def show_next_frame(self, frame: Frame | None = None, *args):
        if frame:
            frame = frame(self, *args)
            frame.grid(row=0, column=0, sticky="nsew")
        next_frame = self._get_next_frame()
        next_frame.tkraise()

    def show_previous_frame(self, *args):
        self._remove_current_frame()
        self.show_next_frame()

    def set_clicked_value(self, value):
        self.clicked_value = value



class BaseFrame(Frame):
    """A frame that sits on top of the main canvas. 
    It holds a canvas, which in turn holds the inner frame with all the widgets of the page.
    It is set up this way, so that canvas-only features like scrollbars and lines, etc. 
    can easily be added to a page
    BaseFrame sits in main canvas -> canvas sits in BaseFrame -> InnerFrame sits in canvas"""

    def __init__(self, controller: Controller):
        """Sets up a base frame with a canvas and inner frame over the main canvas.

        Args:
            controller (Controller): The controller being used. 
                The main canvas of this controller will be used as the frame's parent (master)
        """
        main_canvas = controller.get_main_canvas()
        super().__init__(main_canvas)
        self.grid(row=0, column=0, sticky="nsew")
        #self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.canvas = Canvas(self)
        self.inner_frame: Frame

        self.controller = controller

    def _setup_canvas(self):
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0, 0, window=self.inner_frame, anchor="nw")

    def get_canvas(self):
        return self.canvas

    def set_inner_frame(self, inner_frame):
        """Adds an inner frame to the canvas."""
        self.inner_frame = inner_frame
        self._setup_canvas()

    def get_inner_frame(self) -> None:
        """Returns the inner frame so that widgets and content can be added"""
        return self.inner_frame


class ScrollableBaseFrame(BaseFrame):
    """BaseFrame with a vertical scrollbar"""

    def __init__(self, controller: Controller, *args):
        """BaseFrame with a vertical scrollbar

        Args:
            controller (Controller): The controller being used. 
                The main canvas of this controller will be used as the frame's parent (master)
        """
        super().__init__(controller, *args)
        self.scrollbar = Scrollbar(self)

    def _setup_canvas(self):
        self.canvas.config(yscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.scrollbar.config(orient = "vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y", expand = FALSE)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(0, 0, window=self.inner_frame, anchor="nw")

    def update_scroll_region(self):
        """Updates what is scrollable within the canvas"""
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.inner_frame.bbox())


class InnerFrame(Frame):
    """All content (labels, buttons, etc) should be in this inner frame"""
    def __init__(self, controller: Controller, scrollable: bool = False):
        self.base_frame = self._make_base_frame(controller, scrollable=scrollable)
        self.scrollable = scrollable

        canvas = self.base_frame.get_canvas()
        super().__init__(canvas)
        self.base_frame.set_inner_frame(self)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def _button_clicked(self, button_info: dict) -> None:
        self.base_frame.controller.button_subject.notify_observers(button_info)

    def _make_base_frame(self, controller: Controller, scrollable: bool = False):
        if scrollable:
            return ScrollableBaseFrame(controller)
        return BaseFrame(controller)

    def add_header(self, text: str) -> None:
        label = Label(self, text=text, fg="#000000")
        label.grid(row=0, column=2, sticky="nsew")

    def add_back_button(self):
        back_button = self.add_button(
            text="< Back",
            width=10, height=2,
            button_info=("back", "back"),
            row=0, column=0)
        back_button.config(fg="blue")
    def add_button(self, text: str, width: int, height: int, button_info: tuple, row: int = 0, column: int = 0) -> Button:
        button = Button(
                self,
                text=text,
                width=width,
                height=height,
                command=partial(self._button_clicked, button_info),
            )
        button.grid(row=row, column=column)
        if self.scrollable:
            self.base_frame.update_scroll_region()
        return button
    
    def add_label(self, text: str, row: int = 1) -> None:
        label = Label(self, text=text, fg="#000000", justify="left")
        label.grid(row=row, column=1, sticky="nsew")
