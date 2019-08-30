# make-and-solve-mazes
## maze_maker.py
Generates a maze in the form of a black-and-white PNG image, with black being walls and white being walkways<br>
The maze is surrounded by a 1-pixel-wide layer of black pixels (the outer walls), except for the entrance at the top and exit at the bottom<br><br>
Passing size parameters:

```bash
maze_maker.py 300 100
```
Creates a 300x100 maze, saves as "300x100_n.png", where n is the first available positive integer<br>
Without any parameters it creates a 400x400 maze

### Creation process
1. First creates the main path from entrance to exit
2. Fills the remaining space with randomly branching paths
3. Final cleaning, gets rid of unnecessary parts like 3x3 white squares, fills holes, etc


## maze_solver.py
Solves a maze that's in a format like maze_maker makes, by converting the maze to a graph and using A* to search for the shortest path<br><br>
Passing filename parameters:

```bash
maze_solver_.py 400x400_0.png
```

### Solving process

1. Converts the maze to a graph
2. This means junctions and turns are converted to graph nodes
3. Uses the A* algorithm to find the shortest path 
