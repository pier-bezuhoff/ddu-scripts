from math import sqrt, hypot
from copy import copy

class Circle:
    def __init__(self, x, y, r, color=0x000000, fill=False, visible=False, rule=""):
        # (x, y) = coordinates of the center
        self.x = x
        self.y = y
        self.r = r # radius
        self.color = color # hex RRGGBB format (like in CSS)
        self.fill = fill # if the inside should be colored
        self.visible = visible
        self.rule = [int(x) for x in rule]

    # invert *self* with respect to the *circle*
    def invert(self, circle):
        dx, dy = self.x - circle.x, self.y - circle.y
        d = sqrt(dx*dx + dy*dy)
        ratio = circle.r * circle.r / (d*d - self.r * self.r)
        self.x = circle.x + ratio * dx
        self.y = circle.y + ratio * dy
        self.r = abs(self.r * ratio)

    def show(self):
        pass # display the circle

def invert(x0, y0, r0, x, y, r) -> tuple[float, float, float]:
    "invert a circle w/ (x,y) and r with respect to a circle w/ (x0,y0) and r0"
    dx, dy = x - x0, y - y0
    d = hypot(dx, dy)
    ratio = r0 / (d*d - r*r)
    new_x = x0 + ratio * dx
    new_y = y0 + ratio * dy
    new_r = abs(r * ratio)
    return (new_x, new_y, new_r)


# repeat x=step(x) indefinitely
def step(circles):
    new_circles = [copy(circle) for circle in circles]
    for new_circle in new_circles:
        for j in new_circle.rule:
            new_circle.invert(circles[j])
        new_circle.show()
    return new_circles

# sample ddu (called "Winter" in Dodeca Meditation)
winter_ddu = [
    Circle(-920.753173828125, 1866.708740234375, 1859.665708492877),
    Circle(-901.8592529296875, 1878.81103515625, 1854.104930797163),
    Circle(468.9537048339844, 340.31658935546875, 339.07684691208505, rule="01"),
    Circle(468.5248718261719, 345.0711669921875, 335.5959384049609, rule="01"),
    Circle(1388.179443359375, -3772.58935546875, 4538.483459205404, rule="2301"),
    Circle(1767.4017333984375, -5054.71484375, 5872.806895318434, rule="2301"),
    Circle(677.2852783203125, 879.8759765625, 63.33096624273902, color=0x200020, fill=True, visible=True, rule="45452301"),
    Circle(663.2559814453125, 889.6435546875, 56.01607696333538, color=0x0000ff, fill=True, visible=True, rule="45452301"),
    Circle(369.8866882324219, 806.8751220703125, 299.7592443917674, color=0x80ffff, visible=True, rule="45452301")
]

