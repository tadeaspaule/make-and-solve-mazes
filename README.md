# make-and-solve-mazes
<b>maze_maker.py</b>
Generates a maze in the form of a black-and-white PNG image, with black being walls and white being walkways
You can pass it size parameters ('maze_maker.py 300 100' creates a 300x100 maze, 'maze_maker.py 200' creates a 200x200 maze)
Or you can just run 'maze_maker.py' and it will use a default value (400x400, though you can change that in the code)

Simplified, maze_maker first makes the main path from entrance to exit to ensure the maze is solveable, and then fills the remaining empty space with various branching paths and connections.


<b>maze_solver.py</b>
Solves a maze that's in a format like maze_maker makes, by converting the maze to a graph and using A* to search for the shortest path
You can pass it a filename parameter ('maze_solver.py 600x600_0.png' or 'maze_solver.py 600x600_0')
Or you can set a default filename and run it as-is
