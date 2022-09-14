# Snake AI and Hamiltonian Cycle Visualizer

The goal was to create a perfect agent that could beat the game every time. To achieve this result, it first search for the Hamiltonian Cycle that begins in the starting position of the snake. Then the snake has to simply follow the path.

# Hamiltonian Cycle

A Hamiltonian Cycle is a cycle in a graph that visits every single vertex only one time. This concept applies to the game of Snake because we can see the grid as an undirected graph, whose vertices are the cells and they are connected by an edge if they share a side of the square.  
The Hamiltonian Cycle visits every single cell, including the one with the apple, before the restart of the cycle. In this way, the snake can't hit his body because he can reach the tail only when its length is equal to the number of cells in the grid, so when the game is won.  
Determining if the cycle exists is an NP-complete problem, so using the creation of the Hamiltonian Cycle time expensive. Some possible settings to see the unfolding of the algorithm, but have a solution in a relatively short time are:

```Python
# in costant_screen.py
NUM_OF_ROWS = 4
NUM_OF_COLUMNS = 5
```

```Python
# in main.py
TIME_SLEEP_HAMILTONIAN = 0.05
```

# Technology

-   Python version. 3.10.7
-   pygame version: 2.1.2

# Program logic

The code is structured in a way that could be read top to bottom starting with the `main()`.  
To understand the code it is important to note the difference between the class `Point` and the class `Position`. The former is used to reference a pixel of the screen and the latter is used to reference a cell in a grid.

# References

Inspired by the work of [JOHN TAPSELL](https://johnflux.com/)  
<a href="https://www.flaticon.com/free-icons/arrow" title="arrow icons">Arrow icons created by Freepik - Flaticon</a>  
<a href="https://www.flaticon.com/free-icons/trophy" title="trophy icons">Trophy icons created by Freepik - Flaticon</a>
