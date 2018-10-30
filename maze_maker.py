from PIL import Image
import sys, random, time  

# -------------------------------------- Getting the desired dimensions ----------------------------------------------------------------------------
DEFAULT_SIZE = 400
if len(sys.argv) == 3:
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[2])
    except:
        print("Error parsing passed arguments, using ",DEFAULT_SIZE,"as width and height")
        width = DEFAULT_SIZE
        height = DEFAULT_SIZE
elif len(sys.argv) == 2:
    try:
        width = int(sys.argv[1])
        height = int(sys.argv[1])
    except:
        print("Error parsing passed argument, using ",DEFAULT_SIZE,"as width and height")
        width = DEFAULT_SIZE
        height = DEFAULT_SIZE
else:
    width = DEFAULT_SIZE
    height = DEFAULT_SIZE
steps = []
if width < 3:
    width = DEFAULT_SIZE
    print("Width was set to a number less than 3 (minimum), changing to",DEFAULT_SIZE)
if height < 3:
    height = DEFAULT_SIZE
    print("Height was set to a number less than 3 (minimum), changing to",DEFAULT_SIZE)
bigger_dimension = width if width > height else height
# -------------------------------------- Making the main path from entrance to exit ----------------------------------------------------------------------------
def generate_blank_maze(w,h):
    start = time.time()
    # This 2D array will be our maze representation. 0 = wall / black pixel, 1 = walkway / white pixel
    maze = [[0 for i in range(w)] for i2 in range(h)]

    # Sets positions of the entrance and exit. They're at the top and bottom respectively so no need to set Y
    entrance_x,exit_x = random.randint(1,width-2), random.randint(1,width-2)
    maze[0][entrance_x] = 1
    maze[1][entrance_x] = 1
    maze[-1][exit_x] = 1
    maze[-2][exit_x] = 1

    end = time.time()
    print("blank maze complete, time elapsed:")
    print(end-start,"s")
    
    return (maze,entrance_x,exit_x)

def make_main_path():
    start = time.time()
    x = entrance_x
    y = 1
    while not next_to_goal(x,y):
        x,y = move_in_maze(x,y)
        if (time.time() - start) > bigger_dimension / 100:
            # Sometimes the script takes way too long creating a main path
            # In that case we return out of this method and try again
            print("Starting over with main path, failed attempt took",(time.time()-start))
            return False
    end = time.time()
    print("Main path complete, time elapsed:")
    print(end-start,"s")
    return True

def next_to_goal(x,y):
    return (abs(x-exit_x)==1 and y == height-2) or (abs(y-height+2)==1 and x-exit_x == 0)

def ones_around(x,y):
    total = 0
    if maze[y+1][x] == 1:
        total += 1
    if maze[y-1][x] == 1:
        total += 1
    if maze[y][x+1] == 1:
        total += 1
    if maze[y][x-1] == 1:
        total += 1
    return total

def move_in_maze(x,y):
    # x,y = Position which we are trying to move to the exit, leaving 1's (maze walkways) in our path
    # We store an array of movement vectors (tuples), for ex (1,0) i.e. move 1 in x, 0 in y
    # We add all moves that we can make into this array and then randomly pick one
    moves = []

    if x > 1 and (next_to_goal(x-1,y) or ones_around(x-1,y) < 2):
        moves.append((-1,0))
    if x < width-2 and (next_to_goal(x+1,y) or ones_around(x+1,y) < 2):
        moves.append((1,0))
    if y < height-2 and (next_to_goal(x,y+1) or ones_around(x,y+1) < 2):
        moves.append((0,1))
    if y > 1 and (next_to_goal(x,y-1) or ones_around(x,y-1) < 2):
        moves.append((0,-1))
    
    if len(moves) == 0:
        # Nowhere to move from here, tracing back our steps for a new starting point
        # If possible, goes back 5 steps. Otherwise returns to the beginning
        global steps
        if (len(steps) > 5):
            for i in range(5):
                steps.pop()
        else:
            steps = [steps[0]]
        return (steps[-1][0],steps[-1][1])
        
    move = moves[random.randrange(0,len(moves))]
    x2 = x + move[0]
    y2 = y + move[1]
    steps.append((x2,y2))
    maze[y2][x2] = 1
    return (x2,y2)

maze,entrance_x,exit_x = generate_blank_maze(width,height)
steps = []
while not make_main_path():
    maze,entrance_x,exit_x = generate_blank_maze(width,height)
    steps = []
    
# -------------------------------------- Filling the rest of the maze ----------------------------------------------------------------------------
def ones_around_not_mine(x,y,steps_taken):
    total = 0
    if maze[y+1][x] == 1 and (maze[y+1][x] not in steps_taken):
        total += 1
    if maze[y-1][x] == 1 and (maze[y-1][x] not in steps_taken):
        total += 1
    if maze[y][x+1] == 1 and (maze[y][x+1] not in steps_taken):
        total += 1
    if maze[y][x-1] == 1 and (maze[y][x-1] not in steps_taken):
        total += 1
    return total

def move_branching_path(x,y,steps_taken):
    # Returns a tuple in the form of (new x position, new y position, updated steps_taken array, whether it's done)
    # Basically, moves the x,y and makes walkways until it 'hits' another walkway
    moves = []
    if x > 1 and ones_around_not_mine(x-1,y,steps_taken) < 2:
        moves.append((-1,0))
    if x < width-2 and ones_around_not_mine(x+1,y,steps_taken) < 2:
        moves.append((1,0))
    if y < height-2 and ones_around_not_mine(x,y+1,steps_taken) < 2:
        moves.append((0,1))
    if y > 1 and ones_around_not_mine(x,y-1,steps_taken) < 2:
        moves.append((0,-1))
    if len(moves) == 0:
        return (y,x,None,True)
    move = moves[random.randrange(0,len(moves))]
    x = x + move[0]
    y = y + move[1]
    steps_taken.append((x,y))
    if maze[y][x] == 1:
        # Here is where it hits the walkway
        maze[y][x] = 1
        return (x,y,None, True)
    maze[y][x] = 1
    return (x,y,steps_taken,False)

start = time.time()

# First step: combs through the maze with a 3x3 square
# If it finds a place where the whole square is 0's, starts a branch there that stops upon connecting to the maze
def empty_spot_here(x,y):
    total = 0
    for yy in range(y-1,y+2):
        for xx in range(x-1,x+2):
            total += maze[yy][xx]
    return total == 0
for y in range(2,height-2,3):
    for x in range(2,width-2,3):
        if empty_spot_here(x,y):
            xx,yy,steps_taken,done = x,y,[],False
            maze[yy][xx] = 1
            while not done:
                xx,yy,steps_taken,done = move_branching_path(xx,yy,steps_taken)

# Second step: getting rid of odd small gaps
# Combs through the maze with a 2x2 square
# -> if it finds it empty, 'plugs' it with a 1x2 walkway that connects to other walkways
# -> if it finds it full, tries to remove any redundant walkway tiles
def fill_crack(x,y):
    s = maze[y][x]+maze[y+1][x]+maze[y][x+1]+maze[y+1][x+1]
    if s == 0:
        # blank 2x2 square
        if (maze[y-1][x] == 0 or maze[y-1][x+1] == 0) and (maze[y][x-1] == 1 or maze[y][x+2] == 1):
            # horizontal up
            maze[y][x] = 1
            maze[y][x+1] = 1
        elif (maze[y+2][x] == 0 or maze[y+2][x+1] == 0) and (maze[y+1][x-1] == 1 or maze[y+1][x+2] == 1):
            # horizontal down
            maze[y+1][x] = 1
            maze[y+1][x+1] = 1
        elif (maze[y][x-1] == 0 or maze[y+1][x-1] == 0) and (maze[y-1][x] == 1 or maze[y+2][x] == 1):
            # vertical, left
            maze[y][x] = 1
            maze[y+1][x] = 1
        elif maze[y][x+2] == 0 or maze[y+1][x+2] == 0:
            # vertical, right
            maze[y][x+1] = 1
            maze[y+1][x+1] = 1
    elif s == 4:
        # full 2x2 square
        if maze[y][x-1] == 0 and maze[y-1][x] == 0:
            # removing top left square because it isn't next to any tiles outside the 2x2 square
            maze[y][x] = 0
            
        if maze[y][x+2] == 0 and maze[y-1][x+1] == 0:
            # removing top right square because it isn't next to any tiles outside the 2x2 square
            maze[y][x+1] = 0
            
        if maze[y+1][x-1] == 0 and maze[y+2][x] == 0:
            # removing bottom left square because it isn't next to any tiles outside the 2x2 square
            maze[y+1][x] = 0
            
        if maze[y][x+2] == 0 and maze[y+2][x+1] == 0:
            # removing bottom right square because it isn't next to any tiles outside the 2x2 square
            maze[y+1][x+1] = 0
     
for y in range(1,height-2):
    for x in range(1,width-2):
        fill_crack(x,y)

end = time.time()
print("Rest of the maze complete, time elapsed:")
print(end-start,"s")

# -------------------------------------- Making the maze image ----------------------------------------------------------------------------
def create_image(w,h):
    # Makes square, black image, in black/white mode, in the size provided
    image = Image.new("1", (w,h), "black")
    return image

start = time.time()
img = create_image(width,height)
for y in range(height):
    for x in range(width):
        img.putpixel((x,y),maze[y][x])

# Finding an 'index' that hasn't been used by an image of this size already
i = 0
while True:
    p = str(width)+"x"+str(height)+"_"+str(i)+".png"
    try:
        tmp = Image.open(p)
        tmp.close()
        
    except:
        break
    i += 1
path = str(width)+"x"+str(height)+"_"+str(i)+".png"
img.save(path)
end = time.time()
print("Saving image complete, time elapsed:")
print(end-start,"s")
img.show()