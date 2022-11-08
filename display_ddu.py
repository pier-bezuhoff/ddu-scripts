#!/usr/bin/env python
import tkinter as tk
import analyze_ddu as ad
from time import sleep

x_shift = 400
y_shift = -200
line_width = 2
dt = 300/1000 *0 # sec

class App(tk.Tk):
    def __init__(self, ddu, update_callback=lambda _ddu: None):
        super().__init__()
        self.ddu = ddu
        self.update_callback = update_callback
        self.running = True
        self.canvas = tk.Canvas(self, width=1600, height=1000, bg="gray")
        self.canvas.bind("<1>", self.mouse_press)
        self.canvas.pack(fill="both", expand=True)

    def draw(self):
        for c in self.ddu.circles:
            if c.visible:
                x, y, r = c.x+x_shift, c.y+y_shift, c.r
                color = f"#{c.color:06X}"
                fill_color = color if c.fill else ""
                self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color, outline=color, width=line_width)

    def mouse_press(self, event):
        self._update()
        #if self.running:
        #    self.pause()
        #else:
        #    self.resume()

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False

    def _update(self):
        if self.running:
            self.draw()
            self.ddu.step()
            self.update_callback(self.ddu)
        #super().update()

    def loop(self):
        while True:
            if self.running:
                self.draw()
                self.ddu.step()
                sleep(dt)
            self.update_idletasks()
            self.update()

if __name__ == "__main__":
    ddu = ad.ddu_named("Winter")
    App(ddu).mainloop() # press = 1upd
    #App(ddu).loop() # continuous updates
