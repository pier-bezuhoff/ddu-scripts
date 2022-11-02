import tkinter as tk
import analyze_ddu as ad

class App(tk.Tk):
    def __init__(self, ddu):
        super().__init__()
        self.ddu = ddu
        self.running = False
        self.canvas = tk.Canvas(self, width=800, height=800, bg="white")
        self.canvas.bind("<1>", self.mouse_press)
        self.canvas.pack(fill="both", expand=True)

    def draw(self):
        for c in self.ddu.circles:
            if c['visible']:
                x, y, r = c['x'], c['y'], c['r']
                color = c['color']
                if c['fill']:
                    self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
                else:
                    self.canvas.create_oval(x - r, y - r, x + r, y + r, outline=color)

    def mouse_press(self, event):
        if self.running:
            self.pause()
        else:
            self.resume()

    def resume():
        self.running = True

    def pause():
        self.running = False

    def loop():
        while True:
            if self.running:
                self.ddu.step()
                self.draw()
            self.update_idletasks()
            self.update()

if __name__ == "__main__":
    app = App(winter_ddu)  # Change "winter_ddu" here with your .ddu sample (use winter_ddu's format)
    app.mainloop()
