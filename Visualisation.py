import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PlotApp:
    def __init__(self, K=10):
        self.K = K
        self.iteration = 1
        
        self.root = tk.Tk()
        self.root.title("Plot with side panel")
        
        # Create matplotlib plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Create side panel
        self.panel = tk.Frame(self.root)
        self.panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add buttons
        self.prev_button = tk.Button(self.panel, text="<< Previous iteration", command=self.prev_iteration)
        self.prev_button.pack(side=tk.TOP, padx=10, pady=10)
        
        self.next_button = tk.Button(self.panel, text="Next iteration >>", command=self.next_iteration)
        self.next_button.pack(side=tk.TOP, padx=10, pady=10)
        
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
    app = PlotApp(K=5)
    app.run()
