import tkinter as tk
from shapely.geometry import Polygon, MultiPolygon
from tkinter import filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from IFSLibrary import *
from Parser import Parser
from Tiling import Tiling

FONT = ("Helvetica", 12)

def colourMap(n, name = 'hsv'):
    return plt.cm.get_cmap(name, n)


class Application:
    def __init__(self, IFS = [], attractor = [], theta = []):
        self.IFS = IFS
        self.A = attractor
        self.theta = theta

        self.iteration = 0
        self.tiling = Tiling(self.IFS, self.A, self.theta)
        
        self.root = tk.Tk()
        self.root.title("Graph IFS Plotter")
        
        # Create matplotlib plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH)

        # Create side panel
        self.panel = tk.Frame(self.root)
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.init_side_panel(self.panel)
        
    def init_side_panel(self, frame):
        ###############################
        # Iteration Control
        self.iteration_frame = tk.Frame(frame)
        self.iteration_frame.pack(side = tk.TOP, fill = tk.X)
        self.init_iteration_control(self.iteration_frame)
        
        ####################
        # IFS Controlling
        self.control_frame = tk.Frame(frame)
        self.control_frame.pack(side = tk.TOP)
        tk.Label(self.control_frame, text="Theta Input:").pack(side=tk.TOP, padx=10, pady=5)
        self.input_theta = tk.Entry(self.control_frame)
        self.input_theta.pack(side=tk.TOP, padx=10, pady=5)


        # IFS Inputting
        self.inputFrame = tk.Frame(frame)
        self.inputFrame.pack(side = tk.BOTTOM)
        self.ifs_input = IFSInput(self.inputFrame)
        self.ifs_input.upload_button.config(command = lambda : self.updateIFS(self.ifs_input.upload()))

    def init_iteration_control(self, frame):
        # Add previous button
        prev_frame = tk.Frame(frame)
        prev_frame.pack(side = tk.LEFT)
        tk.Label(prev_frame, text = "Previous iteration").pack(side=tk.TOP)
        self.prev_button = tk.Button(prev_frame, text="<<", command=self.prev_iteration)
        self.prev_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Add next button
        next_frame = tk.Frame(frame)
        next_frame.pack(side = tk.RIGHT)
        tk.Label(next_frame, text = "Next iteration").pack(side=tk.TOP)
        self.next_button = tk.Button(next_frame, text=">>", command=self.next_iteration)
        self.next_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Add a jump to iteration button
        jump_frame = tk.Frame(frame)
        jump_frame.pack(side = tk.LEFT, fill = tk.X)
        tk.Label(jump_frame, text="Jump to Iteration:").pack(side = tk.TOP, padx=10, pady=5)
        self.iter_entry = tk.Entry(jump_frame)
        self.iter_entry.pack(side=tk.TOP, padx=10, pady=5)
        def iter_jump():
            if self.validate_input():
                self.set_iteration(int(self.iter_entry.get()))
                self.iter_entry.delete(0, tk.END)

        self.jump_iter_button = tk.Button(jump_frame, text = "=>", command = iter_jump)
        self.jump_iter_button.pack(side = tk.BOTTOM)

    def updateIFS(self, ifs_parameters):
        IFS, A, theta = ifs_parameters
        if len(IFS) > 1:
            self.IFS = IFS
            self.A = A
            self.theta = theta
        else: 
            self.IFS.append(IFS[0])
        self.tiling = Tiling(IFS, A, theta)
        self.set_iteration(0)

    def validate_input(self):
        value = self.iter_entry.get()
        if value.isdigit() and 0 <= int(value) <= len(self.theta) and len(value) <= self.iteration+1:
            return True
        else:
            self.error_label.config(text="Input must be an integer between 0 and {}".format(len(self.theta)))
            self.root.after(2000, self.clear_error)
            return False
        
    def clear_error(self):
        self.error_label.config(text="")

    def set_iteration(self, iteration):
        if iteration > len(self.theta):
            self.error_label.config(text="ERROR: Iteration at maximum")
            self.root.after(2000, self.clear_error)
            print("ERROR: Iteration at maximum")
        elif iteration < 0:
            self.error_label.config(text="ERROR: Iteration at minimum")
            self.root.after(2000, self.clear_error)
            print("ERROR: Iteration at minimum")
        else:
            self.iteration = iteration
            self.plot_iteration(iteration)
        
    def prev_iteration(self):
        if self.iteration > 0:
            self.set_iteration(self.iteration - 1)
        
    def next_iteration(self):
        if self.iteration < len(self.theta):
            self.set_iteration(self.iteration + 1)
        
    def plot_iteration(self, iteration):
        self.ax.clear()
        self.ax.set_title("Iteration {}".format(self.iteration))

        # Plot each of the polygons provided in the 
        tiles = self.tiling.getIteration(iteration)
        for i, tile in enumerate(tiles):
            poly = tile.polygon
            if type(poly) == Polygon: 
                pltPoly = plt.Polygon(poly.exterior.coords[:-1], facecolor = np.random.rand(3,), alpha = 0.5)
            elif type(poly) == MultiPolygon:
                col = np.random.rand(3,)
                for pol in poly.geoms:
                    pltPoly = plt.Polygon(pol.exterior.coords[:-1], facecolor = col, alpha = 0.5)
            self.ax.add_patch(pltPoly)

        self.canvas.draw()
        
    def run(self):
        # Add error label
        self.error_label = tk.Label(self.panel, fg='red')
        self.error_label.pack(side=tk.TOP, padx=10, pady=5)
        
        # Plot first iteration
        self.plot_iteration(0)
        
        # Start GUI loop
        self.root.mainloop()
        
class IFSInput:
    def __init__(self, frame):
        self.frame = frame
        tk.Label(self.frame, text = "IFS Input", font = (FONT[0], 18)).grid(row = 0, column = 0, columnspan = 2)
        
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
        self.submit_button = tk.Button(self.frame, text="Submit", command=self.submit)
        self.submit_button.grid(row=4, column=1)
    
        # Create upload button
        self.upload_button = tk.Button(self.frame, text="Upload", command=self.upload)
        self.upload_button.grid(row=5, column=1)

    def submit(self):
        entries = [self.rotation, self.scaling, self.translation]
        values = [entry.get()  for entry in entries]
        for e in entries: # Clear the entries (TODO: only clear if successful entry)
            e.delete(0, tk.END)
        print(values)

    def upload(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("JSON files", "*.json"),))
        if filename:
            return Parser.parse(filename)


if __name__ == "__main__":
    default = "ExIFS.json"
    [IFS, attractor, theta] = Parser.parse(default)
    app = Application(IFS, attractor, theta)
    app.run()
