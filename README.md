# Sudoku-Solver
This is a simple Sudoku+ solver and generator which uses MiniSAT. Built as an assignment for CS202: Logic for Computer Science. Sudoku+ is an extended version of a normal Sudoku with the extra constraint that not only each row, each column and each 3x3 box, but also both main diagonals must contain distinct numbers from 1 to 9.
# Dependencies
You must have [MiniSAT](http://minisat.se) installed on your system. MiniSAT is a minimalistic, open-source SAT solver.
# Build and Run
1. Make sure that MiniSAT is installed on your system.
2. Run the python file sudoku.py:
```python sudoku.py```
3. Input whether you want to solve a sudoku+ or generate a new one.
4. Enter the name of file which contains the unsolved sudoku.
5. The solved sudoku or the generated minimal sudoku will be printed in the terminal.
