
import matplotlib
import tkinter
import shapely

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from IFSLibrary import *

class Application:
    def __init__(self, IFS = [], attractor = [], theta =[]):
        self.IFS = IFS
        self.attractor = attractor
        self.theta = theta

        self.iteration = 1
        
        self.root = tk.Tk()
        self.root.title("Graph IFS Plotter")
        
        # Create matplotlib plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.init_side_panel()
        
    def init_side_panel(self):
        # Create side panel
        self.panel = tk.Frame(self.root)
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ADD BUTTONS
        # Add previous button
        self.prev = tk.Frame(self.panel)
        self.prev.pack(side = tk.LEFT)
        self.prev.label = tk.Label(self.prev, text = "Previous iteration"); self.prev.label.pack(side=tk.TOP)
        self.prev.prev_button = tk.Button(self.prev, text="<<", command=self.prev_iteration)
        self.prev.prev_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Add next
        self.next = tk.Frame(self.panel)
        self.next.pack(side = tk.RIGHT)
        self.next.label = tk.Label(self.next, text = "Next iteration"); self.next.label.pack(side=tk.TOP)
        self.next.next_button = tk.Button(self.next, text=">>", command=self.next_iteration)
        self.next.next_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Add input field
        self.input_label = tk.Label(self.panel, text="Iteration:")
        self.input_label.pack(side=tk.TOP, padx=10, pady=5)
        
        self.input_entry = tk.Entry(self.panel)
        self.input_entry.pack(side=tk.TOP, padx=10, pady=5)
        
    def validate_input(self):
        value = self.input_entry.get()
        if value.isdigit() and 1 <= int(value) <= self.K and len(value) <= self.iteration+1:
            return True
        else:
            self.error_label.config(text="Input must be an integer between 1 and {} with at most {} digits".format(self.K, self.iteration+1))
            self.root.after(2000, self.clear_error)
            return False
        
    def clear_error(self):
        self.error_label.config(text="")
        
    def prev_iteration(self):
        if self.iteration > 1:
            self.iteration -= 1
            self.plot_iteration()
        
    def next_iteration(self):
        if self.iteration < self.K:
            if self.validate_input():
                self.iteration += 1
                self.plot_iteration()
                print("Iteration:", self.iteration)
        
    def plot_iteration(self):
        self.ax.clear()
        # Add your plotting code here
        self.ax.set_title("Iteration {}".format(self.iteration))
        self.canvas.draw()
        
    def run(self):
        # Add error label
        self.error_label = tk.Label(self.panel, fg='red')
        self.error_label.pack(side=tk.TOP, padx=10, pady=5)
        
        # Plot first iteration
        self.plot_iteration()
        
        # Start GUI loop
        self.root.mainloop()
        
if __name__ == "__main__":
    app = Application()
    app.run()
