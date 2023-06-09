import tkinter as tk
from shapely.geometry import Polygon, MultiPolygon, Point
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
    def __init__(self, IFSgraph = [], theta = []):
        self.IFSgraph = IFSgraph
        self.theta = theta

        self.iteration = 0
        self.tiling = Tiling(self.IFSgraph, self.theta)
        
        self.root = tk.Tk()
        self.root.title("Graph IFS Plotter")
        
        # Create matplotlib plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.xb = [-1, 3]
        self.yb = [-1, 3]

        # Create side panel
        self.panel = tk.Frame(self.root)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.panel, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack(side=tk.TOP)
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)
        self.init_side_panel(self.panel)
        self.toolbar._message_label.pack_forget()
        self.setup_address_hover(self.panel)

    def setup_address_hover(self, frame):
        self.addr_label = tk.Label(frame, text="Polygon Address: ")
        self.addr_label.pack(side = tk.TOP)

        def update_polygon_info(event, text):
            # Get the coordinates of the mouse pointer
            x, y = event.xdata, event.ydata
            if x == None or y == None: return
            p = Point(x,y)

            # Check if the mouse pointer is inside any polygon
            t = self.tiles.copy()
            t.reverse()
            for tile in t:
                if tile.polygon.contains(p):
                    text.config(text=f"Polygon Address: {tile.address}")
                    return

            # If no polygon is under the mouse pointer, clear the info label
            text.config(text="Polygon Address: ")
        self.canvas.mpl_connect("motion_notify_event", lambda ev : update_polygon_info(ev, self.addr_label))


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

    def xlim(self, x_bounds):
        return self.ax.set_xlim(x_bounds[0], x_bounds[1])

    def ylim(self, y_bounds):
        return self.ax.set_ylim(y_bounds[0], y_bounds[1])

    def updateIFS(self, ifs_parameters):
        IFSgraph, theta = ifs_parameters
        self.IFSgraph = IFSgraph
        self.theta = theta
        self.tiling = Tiling(IFSgraph, theta)
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
        self.xb = self.ax.get_xlim(); print(self.xb)
        self.yb = self.ax.get_ylim();print(self.yb)
        self.ax.clear()
        self.ax.set_title("Iteration {}".format(self.iteration))

        # Plot each of the polygons provided in the 
        self.tiles = self.tiling.getIteration(iteration)
        self.tiles.reverse()
        for i, tile in enumerate(self.tiles):
            poly = tile.polygon
            if type(poly) == Polygon: 
                pltPoly = plt.Polygon(poly.exterior.coords[:-1], facecolor = np.random.rand(3,), alpha = 1)
            elif type(poly) == MultiPolygon:
                col = np.random.rand(3,)
                for pol in poly.geoms:
                    pltPoly = plt.Polygon(pol.exterior.coords[:-1], facecolor = col, alpha = 0.5)
            else:
                print(type(poly))
            self.ax.add_patch(pltPoly)

        self.xlim(self.xb); self.ylim(self.yb)
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
        #print(values)

    def upload(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("JSON files", "*.json"),))
        if filename:
            [IFS, A, theta] = Parser.parse(filename)
            IFSgraph = Parser.convert(IFS,A)
            return (IFSgraph, theta)

if __name__ == "__main__":
    default = "ExampleIFS/IFSRobinsonTriangles.json"
    [IFS, A, theta] = Parser.parse(default)
    IFSgraph = Parser.convert(IFS,A)
    app = Application(IFSgraph, theta)
    app.run()
