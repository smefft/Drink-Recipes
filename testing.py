from tkinter import *

controller = Tk()
controller.geometry('1000x500')

main_canvas = Canvas(controller)
main_canvas.pack(side="top", fill="both", expand=True)
main_canvas.grid_rowconfigure(0, weight=1)
main_canvas.grid_columnconfigure(0, weight=1)

def update_scroll_region(canvas: Canvas, frame: Frame):
    canvas.update_idletasks()
    canvas.config(scrollregion=frame.bbox())

back_frame1 = Frame(main_canvas)
back_frame1.grid(row=0, column=0, sticky="nsew")

canvas1 = Canvas(back_frame1)
inner_1 = Frame(canvas1)
scroll_bar = Scrollbar(back_frame1)

canvas1.config(yscrollcommand=scroll_bar.set, highlightthickness=0)
scroll_bar.config(orient = "vertical", command=canvas1.yview)
scroll_bar.pack(side="right", fill="y", expand = FALSE)
canvas1.pack(side="left", fill="both", expand=True)
canvas1.create_window((0, 0), window=inner_1, anchor="nw")

for i in range(100):
    button = Button(inner_1, text=f"Button {i+1}")
    # HAS TO BE GRID
    button.grid(row=i, column=0)

update_scroll_region(canvas1, inner_1)
#back_frame1.grid(row=0, column=0, sticky="nsew")
back_frame1.tkraise()


# Frame 2

back_frame2 = Frame(main_canvas)

canvas2 = Canvas(back_frame2)
inner_2 = Frame(canvas2)
canvas2.pack(side="left", fill="both", expand=True)

canvas2.create_window((0, 0), window=inner_2, anchor="nw")
back_frame2.grid(row=0, column=0, sticky="nsew")

scroll_bar = Scrollbar(back_frame2)

canvas2.config(yscrollcommand=scroll_bar.set, highlightthickness=0)
scroll_bar.config(orient = "vertical", command=canvas2.yview)
scroll_bar.pack(side="right", fill="y", expand = FALSE)

for i in range(100):
    label = Label(inner_2, text=f"Label {i+1}")
    # HAS TO BE GRID
    label.grid(row=i, column=0)
update_scroll_region(canvas2, inner_2)

back_frame2.tkraise()
back_frame1.tkraise()

controller.mainloop()
