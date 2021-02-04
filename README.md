Project 3
=========

Lagrangian Relaxation framework, and 2-TSP solution.

`report.pdf` is a full report on the solution, in Portuguese.

## Requirements
No Python libraries are explicitly required, but to run the main files `main.py` and `main1.py`, the following libraries are required:

- NumPy
- Pandas
- MatPlotLib
- NetworkX

## How to Run

### Single Method
`python3 main.py <n_points> <seed_value> <time_limit>`

The result is printed in the standard output.

### Bunch Method
`python3 main1.py`

It will run with various amounts of points, and save the results in a CSV file. Also runs an ILP model for the problem.


## Framework
This framework can be used for other problems as well, with new main files and creating different subclasses from `Problem.py`.
