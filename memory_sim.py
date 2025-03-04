#!/usr/bin/python3.5
import tkinter as tk
import random
import numpy as np

class MemorySimulation:
    def __init__(self, master):
        self.master = master
        master.title("Memory Simulation")
        
        # Main Frame to organize layout
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas for grid (left side)
        self.canvas = tk.Canvas(self.main_frame, width=460, height=460, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Right Frame for controls and stats
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky="n")
        
        # Control Frame (top-right)
        self.control_frame = tk.Frame(self.right_frame)
        self.control_frame.pack(fill="x", pady=(0, 10))
        
        # Buttons (horizontal layout)
        self.run_button = tk.Button(self.control_frame, text="Run", command=self.start_simulation, width=8)
        self.run_button.grid(row=0, column=0, padx=2)
        
        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.toggle_pause, state="disabled", width=8)
        self.pause_button.grid(row=0, column=1, padx=2)
        
        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_simulation, width=8)
        self.reset_button.grid(row=0, column=2, padx=2)
        
        # Iterations Entry
        self.iterations_label = tk.Label(self.control_frame, text="Iterations:")
        self.iterations_label.grid(row=1, column=0, pady=5)
        self.iterations_entry = tk.Entry(self.control_frame, width=10)
        self.iterations_entry.insert(tk.END, "10")
        self.iterations_entry.grid(row=1, column=1, columnspan=2, pady=5)
        
        # Speed Slider
        self.speed_label = tk.Label(self.control_frame, text="Speed (ms):")
        self.speed_label.grid(row=2, column=0, pady=5)
        self.speed_scale = tk.Scale(self.control_frame, from_=10, to=500, orient=tk.HORIZONTAL, length=100)
        self.speed_scale.set(100)
        self.speed_scale.grid(row=2, column=1, columnspan=2, pady=5)
        
        # Stats Frame (below controls, right side)
        self.stats_frame = tk.Frame(self.right_frame)
        self.stats_frame.pack(fill="x", pady=10)
        self.stats_label = tk.Label(self.stats_frame, text="Statistics:")
        self.stats_label.pack(anchor="w")
        self.stats_text = tk.Text(self.stats_frame, height=8, width=30)
        self.stats_text.pack(anchor="w")
        
        # Legend Frame (bottom-right)
        self.legend_frame = tk.Frame(self.right_frame)
        self.legend_frame.pack(fill="x")
        self.legend_label = tk.Label(self.legend_frame, text="Legend:")
        self.legend_label.pack(anchor="w")
        self.state_names = {0: "Defective", 1: "New", 2: "Normal", 3: "Aged"}
        for state, color in {0: "red", 1: "dark green", 2: "green", 3: "light green"}.items():
            tk.Label(self.legend_frame, text=self.state_names[state], bg=color, fg="white" if state == 0 else "black", width=15).pack(anchor="w", pady=2)
        
        # Colors
        self.color_dict = {0: "red", 1: "dark green", 2: "green", 3: "light green"}
        
        # Grid Setup
        self.grid_size = 21
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.reset_grid()
        
        # Simulation State
        self.running = False
        self.paused = False
        self.current_iteration = 0
        
        # Configure grid weights to fill space
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

    def reset_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.grid[i][j] = 1
        self.defective_cells = set()
        self.current_iteration = 0
        self.stats_text.delete("1.0", tk.END)
        self.draw_grid()

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.reset_button.config(state="disabled")
            try:
                self.max_iterations = int(self.iterations_entry.get())
            except ValueError:
                self.max_iterations = 10
            self.run_simulation()

    def run_simulation(self):
        if not self.running or self.paused:
            return
        if self.current_iteration < self.max_iterations:
            self.update_grid()
            self.update_stats_text(self.current_iteration + 1)
            self.current_iteration += 1
            self.master.after(self.speed_scale.get(), self.run_simulation)
        else:
            self.stop_simulation()

    def stop_simulation(self):
        self.running = False
        self.run_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="normal")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.run_simulation()

    def reset_simulation(self):
        self.stop_simulation()
        self.reset_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        cell_width = 20
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * cell_width
                y1 = i * cell_width
                x2 = x1 + cell_width
                y2 = y1 + cell_width
                color = self.color_dict[self.grid[i][j]]
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def update_grid(self):
        new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        total_defective = sum(row.count(0) for row in self.grid)
        total_cells = self.grid_size ** 2
        repair_prob = total_defective / total_cells if total_cells > 0 else 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                neighbors = self.get_neighbors(i, j)
                curr_state = self.grid[i][j]
                new_state = self.get_new_state(curr_state, neighbors, repair_prob)
                new_grid[i][j] = new_state
        self.grid = new_grid.copy()
        self.draw_grid()

    def update_stats_text(self, iteration):
        new_cells = normal_cells = defective_cells = aged_cells = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == 0:
                    defective_cells += 1
                elif self.grid[i][j] == 1:
                    new_cells += 1
                elif self.grid[i][j] == 2:
                    normal_cells += 1
                else:
                    aged_cells += 1
        total_cells = self.grid_size ** 2
        stats = f"Iteration {iteration}/{self.max_iterations}:\n"
        stats += f"New: {new_cells} ({new_cells / total_cells * 100:.2f}%)\n"
        stats += f"Normal: {normal_cells} ({normal_cells / total_cells * 100:.2f}%)\n"
        stats += f"Defective: {defective_cells} ({defective_cells / total_cells * 100:.2f}%)\n"
        stats += f"Aged: {aged_cells} ({aged_cells / total_cells * 100:.2f}%)\n"
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, stats)

    def get_neighbors(self, x, y):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.grid_size and 0 <= y + j < self.grid_size:
                    neighbors.append(self.grid[x + i][y + j])
        return neighbors

    def get_new_state(self, current_state, neighbor_states, repair_prob):
        n_defective = np.count_nonzero(np.array(neighbor_states) == 0)
        r = np.random.rand()
        if current_state == 1:  # New
            if r < 0.05:  # Lemon: 5%
                return 0  # Defective
            elif r < 0.45:  # Install: 40%
                return 2  # Normal
            return 1  # Stay New
        elif current_state == 2:  # Normal
            if r < 0.15:  # Prevention: 15%
                return 1  # New
            elif r < 0.20:  # Wear & Tear: 5%
                return 3  # Aged
            elif r < 0.40 and n_defective > 0:  # Neighbor: 20% if any defective neighbor
                return 0  # Defective
            return 2  # Stay Normal
        elif current_state == 0:  # Defective
            if r < repair_prob:  # Repair: % of total defective cells
                return 1  # New
            return 0  # Stay Defective
        else:  # Aged
            if r < 0.10:  # Decay: 10%
                return 0  # Defective
            return 3  # Stay Aged

root = tk.Tk()
my_gui = MemorySimulation(root)
root.mainloop()
