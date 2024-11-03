from tkinter import *

class Controller(Tk):
    """Controller class for controling the flow of the app and its frames"""

    def __init__(self, width = 1000, height = 600, title = "New App"):
        """Sets up the root window and controls of a new app

        Args:
            width: width of the root window (defaults to 1000)
            height: height of the root window (defaults to 600)
            title: title of the new app (defaults to "New App")     
    """
        Tk.__init__(self)
        self.geometry(f'{width}x{height}')
        self.title(title)

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

    def show_previous_frame(self):
        self._remove_current_frame()
        self.show_next_frame()



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

        self.controller = controller
        self.canvas = Canvas(self)
        self.inner_frame: Frame

    def _setup_canvas(self):
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window(500, 300, window=self.inner_frame, anchor="nw")

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
        self._configure_scrollable_canvas()

    def _configure_scrollable_canvas(self):
        self.canvas.config(yscrollcommand=self.scrollbar.set, highlightthickness=0)
        self.scrollbar.config(orient = "vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y", expand = FALSE)
        self.canvas.pack(side="left", fill="both", expand=True)

    def update_scroll_region(self):
        """Updates what is scrollable within the canvas

        Args:
            frame (Frame): The frame of the current page with all widgets that should be scrollable
        """
        self.update_idletasks()
        self.config(scrollregion=self.inner_frame.bbox())

class InnerFrame(Frame):
    def __init__(self, controller: Controller):
        self.base_frame = self._make_base_frame(controller)
        canvas = self.base_frame.get_canvas()
        super().__init__(canvas)
        self.base_frame.set_inner_frame(self)
        self.pack(fill="both", expand=True)

    def _make_base_frame(self, controller: Controller, scrollable: bool = False):
        if scrollable:
            return ScrollableBaseFrame(controller)
        return BaseFrame(controller)

    def add_header(self, text: str) -> None:
        label = Label(self, text=text, fg="#000000")
        label.pack(pady=4)

    def add_button(self, text: str, width: int, height: int, command: callable) -> None:
        button = Button(
                self,
                text=text,
                width=width,
                height=height,
                command=command,
            )
        button.pack(pady=4)
