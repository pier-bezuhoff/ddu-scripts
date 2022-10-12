from math import sqrt
from copy import copy
import tkinter as tk


# Invert realization using 'Circle' class and 'step' function
class Circle:
    def __init__(self, x, y, r, color="#000000", fill=False, visible=False, rule=""):
        """Initialize the circle with given parameters"""
        # (x, y) — coordinates of the center of the circle
        self.x = x
        self.y = y
        self.r = r  # radius of the circle
        self.color = color  # color of the outline of circle (in hex format, write with sharp symbol: "#RRGGBB")
        self.fill = fill  # whether the circle should be filled with the outline color or not
        self.visible = visible  # whether the circle should be visible or not
        self.rule = [int(x) for x in rule]  # rule for invert steps

    def invert(self, circle):
        """Invert *self* circle relative to the input *circle*"""
        dx, dy = self.x - circle.x, self.y - circle.y
        d = sqrt(dx*dx + dy*dy)
        ratio = circle.r * circle.r / (d*d - self.r * self.r)
        self.x = circle.x + ratio * dx
        self.y = circle.y + ratio * dy
        self.r = abs(self.r * ratio)

    def show(self, visible=True):
        """Make the circle (in)visible"""
        self.visible = visible

    def fill(self, fill=True):
        """Make the circle (un)filled"""
        self.fill = fill

    def recolor(self, color="#000000"):
        """Change the color of the circle"""
        self.color = color


def step(circles):
    """Inverts the circles in the input list according to their rules and returns the updated list"""
    new_circles = [copy(circle) for circle in circles]
    for new_circle in new_circles:
        for j in new_circle.rule:
            new_circle.invert(circles[j])
    return new_circles


# .ddu sample
# It is called "Winter" in Dodeca Meditation
winter_ddu = [
    Circle(-920.753173828125, 1866.708740234375, 1859.665708492877),
    Circle(-901.8592529296875, 1878.81103515625, 1854.104930797163),
    Circle(468.9537048339844, 340.31658935546875, 339.07684691208505, rule="01"),
    Circle(468.5248718261719, 345.0711669921875, 335.5959384049609, rule="01"),
    Circle(1388.179443359375, -3772.58935546875, 4538.483459205404, rule="2301"),
    Circle(1767.4017333984375, -5054.71484375, 5872.806895318434, rule="2301"),
    Circle(677.2852783203125, 879.8759765625, 63.33096624273902, color="#200020", fill=True, visible=True, rule="45452301"),
    Circle(663.2559814453125, 889.6435546875, 56.01607696333538, color="#0000ff", fill=True, visible=True, rule="45452301"),
    Circle(369.8866882324219, 806.8751220703125, 299.7592443917674, color="#80ffff", visible=True, rule="45452301")
]
# You can use your own samples, just make add them as a list of circles (in winter_ddu format)


# Visual implementation using Tkinter module
class App(tk.Tk):
    """Tkinter app for visualization"""
    def __init__(self, ddu_sample):
        super().__init__()

        # Parameters for the app
        self.title("Dodeka is a lie")
        self.width = 800
        self.height = 800

        # You have to input the sample you chose when calling an instance of the app,
        # So you can't use different samples in one app currently
        self.sample = ddu_sample

        # Canvas and label initialization
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="gray")
        self.label = tk.Label(self)

        # Binds for interaction with the app
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<1>", self.mouse_press)
        self.canvas.bind("<MouseWheel>", self.mouse_press)
        self.canvas.bind("<3>", self.clear)

        # Canvas and label packing
        self.canvas.pack(fill="both", expand=True)
        self.label.pack(fill="both")

    def clear(self, event):
        """Clear previous iterations of the circles from the canvas"""
        self.canvas.delete("all")
        self.draw_sample()

    def draw_sample(self):
        """Draw the current iteration of the circles"""
        for circle in self.sample:
            if circle.visible:
                if circle.fill:
                    self.canvas.create_oval(circle.x-circle.r, circle.y-circle.r, circle.x+circle.r, circle.y+circle.r,
                                            fill=circle.color, outline=circle.color)
                else:
                    self.canvas.create_oval(circle.x-circle.r, circle.y-circle.r, circle.x+circle.r, circle.y+circle.r,
                                            outline=circle.color)

    def mouse_press(self, event):
        """Draw a new iteration of the circles"""
        self.sample = step(self.sample)
        self.draw_sample()

    def mouse_motion(self, event):
        """Change the text at the bottom to show the position of the mouse on canvas"""
        x, y = event.x, event.y
        text = f"Позиция курсора: ({x}, {y})"
        self.label.config(text=text)


# Main loop for the app
if __name__ == "__main__":
    app = App(winter_ddu)  # Change "winter_ddu" here with your .ddu sample (use winter_ddu's format)
    app.mainloop()
