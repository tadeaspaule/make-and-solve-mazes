# make-and-solve-mazes
<b>maze_maker.py</b><br>
Generates a maze in the form of a black-and-white PNG image, with black being walls and white being walkways<br>
The maze is surrounded by a 1-pixel-wide layer of black pixels (the outer walls), except for the entrance at the top and exit at the bottom<br>
You can pass it size parameters ('maze_maker.py 300 100' creates a 300x100 maze, 'maze_maker.py 200' creates a 200x200 maze)<br>
Or you can just run 'maze_maker.py' and it will use a default value (400x400, though you can change that in the code)
<br><br>
In a nutshell, maze_maker first makes the main path from entrance to exit to ensure the maze is solveable. It does this by 'moving' an x-and-y position through the maze by randomly picked movement until it gets to the exit. If it gets stuck and can't move anywhere, it retraces its steps and starts over from that spot, but leaves the path it took 'white' (labeled as a walkway), so some branching paths are already created.<br>
Then it fills the remaining empty space by branching paths, and lastly it fills any remaining small holes by short corridors and gets rid of unnecessary walkway tiles (for example, there is no point in there being a 3x3 all white square)

<br>
<br>
<b>maze_solver.py</b><br>
Solves a maze that's in a format like maze_maker makes, by converting the maze to a graph and using A* to search for the shortest path<br>
You can pass it a filename parameter ('maze_solver.py 600x600_0.png' or 'maze_solver.py 600x600_0')<br>
Or you can set a default filename and run it as-is.
<br><br>
In a nutshell, maze_solver first converts the maze to a <i>graph</i>, which is just a bunch of nodes with connections between them. Then it uses the A* algorithm to find the shortest path from the start node to the exit node.<br>A* works by using a queue of nodes to check. They are sorted by distance travelled so far + distance from the exit, so you're always checking nodes that you hope get you to the exit. A* takes the first item from the queue, checks if it's the exit, in which case it's done, and if not it adds all the nodes this one connects to the queue and puts the current item away to a pile of finished items. This iterates until the exit node is reached.
