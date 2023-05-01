import tkinter as tk
# import shapely
from tkinter import filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from IFSLibrary import *
from Tiling import Tiling

FONT = ("Helvetica", 12)

def colourMap(n, name = 'hsv'):
    return plt.cm.get_cmap(name, n)


class Application:
    def __init__(self, IFS = [], attractor = [], theta = []):
        self.IFS = IFS
        self.attractor = attractor
        self.theta = theta

        self.iteration = 1

        self.tiling = Tiling(IFS, attractor, theta)
        
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
        tk.Label(self.prev, text = "Previous iteration").pack(side=tk.TOP)
        self.prev.prev_button = tk.Button(self.prev, text="<<", command=self.prev_iteration)
        self.prev.prev_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Add next
        self.next = tk.Frame(self.panel)
        self.next.pack(side = tk.RIGHT)
        tk.Label(self.next, text = "Next iteration").pack(side=tk.TOP)
        self.next.next_button = tk.Button(self.next, text=">>", command=self.next_iteration)
        self.next.next_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        tk.Label(self.panel, text="Iteration:").pack(side=tk.TOP, padx=10, pady=5)
        self.input_entry = tk.Entry(self.panel)
        self.input_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.inputFrame = tk.Frame(self.panel)
        self.inputFrame.pack(side = tk.BOTTOM)
        self.ifs_input = IFSInput(self.inputFrame)
        
    def validate_input(self):
        value = self.input_entry.get()
        if value.isdigit() and 1 <= int(value) <= len(self.theta) and len(value) <= self.iteration+1:
            return True
        else:
            self.error_label.config(text="Input must be an integer between 1 and {} with at most {} digits".format(len(self.theta), self.iteration+1))
            self.root.after(2000, self.clear_error)
            return False
        
    def clear_error(self):
        self.error_label.config(text="")
        
    def prev_iteration(self):
        if self.iteration > 1:
            self.iteration -= 1
            self.plot_iteration()
        
    def next_iteration(self):
        if self.iteration < len(self.theta):
            if self.validate_input():
                self.iteration += 1
                self.plot_iteration()
                print("Iteration:", self.iteration)
        
    def plot_iteration(self, iteration):
        self.ax.clear()
        self.ax.set_title("Iteration {}".format(self.iteration))

        # Plot each of the polygons provided in the 
        polys = self.tiling.getIteration(iteration)
        colours = colourMap(len(polys))
        for i, poly in enumerate(polys):
            pltPoly = plt.Polygon(poly.exterior.xy, facecolor = colours[i], alpha = 0.5)
            self.ax.add_path(pltPoly)

        self.canvas.draw()
        
    def run(self):
        # Add error label
        self.error_label = tk.Label(self.panel, fg='red')
        self.error_label.pack(side=tk.TOP, padx=10, pady=5)
        
        # Plot first iteration
        self.plot_iteration(1)
        
        # Start GUI loop
        self.root.mainloop()
        
class IFSInput:
    def __init__(self, frame):
        self.frame = frame
        tk.Label(self.frame, text = "IFS Input", font = (FONT[0], 18)).grid(row = 0, column = 0, columnspan = 2)
        self.entries = []
        
        # Create input labels and fields
        rotation_label = tk.Label(self.frame, text="Rotation")
        rotation_label.grid(row=1, column=0)
        self.rotation = tk.Entry(self.frame)
        self.rotation.grid(row=1, column=1)
        
        scaling_label = tk.Label(self.frame, text="Scaling")
        scaling_label.grid(row=2, column=0)
        self.scaling = tk.Entry(self.frame)
        self.scaling.grid(row=2, column=1)
        
        translation_label = tk.Label(self.frame, text="Translation")
        translation_label.grid(row=3, column=0)
        self.translation = tk.Entry(self.frame)
        self.translation.grid(row=3, column=1)
        
        # Create submit button
        submit_button = tk.Button(self.frame, text="Submit", command=self.submit)
        submit_button.grid(row=4, column=1)
    
        # Create upload button
        upload_button = tk.Button(self.frame, text="Upload", command=self.upload)
        upload_button.grid(row=5, column=0, columnspan=2)

    def submit(self):
        entries = [self.rotation, self.scaling, self.translation]
        values = [entry.get()  for entry in entries]
        for e in entries: # Clear the entries (TODO: only clear if successful entry)
            e.delete(0, tk.END)
        print(values)

    def upload(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("JSON files", "*.json"),))
        if filename:
            print(filename)
            with open(filename, "r") as f:
                data = json.load(f)
                self.entries[0].insert(0, str(data.get("rotation", "")))
                self.entries[1].insert(0, str(data.get("scaling", "")))
                self.entries[2].insert(0, str(data.get("translation", "")))

if __name__ == "__main__":
    app = Application()
    app.run()
