# Memory Simulation

A Python-based GUI simulation of memory cell evolution, built with `tkinter` and `NumPy`. Inspired by cellular automata like Conway’s Game of Life, it models memory degradation and repair in an interactive 21x21 grid—perfect for exploring system dynamics!

## Project Overview

The simulation represents a disk’s memory as a 21x21 grid of cells, rendered within a 460x460 pixel canvas window. Each cell evolves daily according to specific transition probabilities, reflecting concepts like wear, decay, and repair. The GUI includes interactive controls to run, pause, and reset the simulation, real-time statistics, and a clear legend for an engaging exploration of state changes and system behavior.

## Features

- **Interactive Grid Visualization**: A 21x21 grid (displayed in a 460x460 canvas) where each cell’s state is color-coded:
  - **Defective**: Red
  - **New**: Dark Green
  - **Normal**: Green
  - **Aged**: Light Green
- **Control Panel**:
  - **Run**: Starts the simulation for a user-defined number of iterations.
  - **Pause/Resume**: Toggles the simulation mid-run, with dynamic button text.
  - **Reset**: Restores all cells to "New" state.
  - **Iterations**: Input field to set simulation cycles (default: 10).
  - **Speed Slider**: Adjusts update speed from 10ms to 500ms per iteration.
- **Real-Time Statistics**: Displays counts and percentages of each state after every iteration.
- **Legend**: Labeled guide mapping colors to states (Defective, New, Normal, Aged).
- **State Transitions**: Cells evolve based on these probabilities:
  - **Install**: 40% (New → Normal)
  - **Wear & Tear**: 5% (Normal → Aged)
  - **Decay**: 10% (Aged → Defective)
  - **Repair**: % of total defective cells (Defective → New)
  - **Prevention**: 15% (Normal → New)
  - **Lemon**: 5% (New → Defective)
  - **Neighbor**: 20% (Normal → Defective if any of 8 neighbors is defective)

## Usage

1. **Start the Simulation**:
   - Run the script to open the GUI.
2. **Configure Settings**:
   - Enter the number of iterations in the "Iterations" field.
   - Slide the speed control to set the pace of updates.
3. **Interact**:
   - Click "Run" to begin the simulation.
   - Use "Pause" to halt (changes to "Resume" when paused) and continue.
   - Hit "Reset" to restart with all cells as "New."
4. **Analyze**:
   - Watch the 21x21 grid update and observe state changes.
   - Check the stats panel for detailed breakdowns of cell states.

## Code Structure

- **`MemorySimulation` Class**:
  - `__init__`: Initializes the GUI layout, grid, and controls.
  - `reset_grid`: Resets the 21x21 grid to all "New" cells and clears stats.
  - `start_simulation`/`run_simulation`: Drives the simulation loop.
  - `toggle_pause`/`stop_simulation`: Manages pausing and stopping.
  - `draw_grid`: Renders the grid with color-coded cells.
  - `update_grid`: Updates cell states based on rules.
  - `update_stats_text`: Refreshes the statistics display.
  - `get_neighbors`/`get_new_state`: Implements state transition logic.

## Screenshots

- Initial state: All cells new (dark green):
<img width="600" alt="Screenshot 2025-03-04 at 9 04 23 AM" src="https://github.com/user-attachments/assets/f4facd36-7c0a-4731-8151-b37b1ec2165d" />

** **

- After 100 iterations: Mixed states with defective (red) spread:
<img width="600" alt="Screenshot 2025-03-04 at 9 07 32 AM" src="https://github.com/user-attachments/assets/57ab10a0-81f8-402b-9220-8872f880861b" />

** **
## Dependencies

- **`tkinter`**: Python’s standard GUI library, used for the interactive interface and canvas rendering.
- **`numpy`**: Handles efficient array operations and random number generation for state transitions.

## Notes

- **Probability Implementation**: Transition probabilities in `get_new_state()` are hardcoded to define the simulation rules, using `np.random.rand()` for randomness.

## Installation Guide

To run the simulation locally:
1. **Ensure Python 3.5+**: The script requires a Python version with `tkinter` support (download from [python.org](https://www.python.org/downloads/) if needed).
2. **Install NumPy**: Open a terminal and run:
```bash
pip install numpy
```
3. **Run the Script**: Navigate to the project directory and execute:
```bash
python memory_sim.py
```
