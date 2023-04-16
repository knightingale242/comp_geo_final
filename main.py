import turtle

global screen
global count
global pen
count = 0
global state 
state = 0
global sides
global polygon
polygon = []

#get how many sides the polygon will be
sides = input("How many sides do you want the polygon to have?")
sides = int(sides)

if sides <= 3:
    print("Must enter more than 3 sides.")
    turtle.bye()

#draws the initial lines to build the poylygon
def draw_line(x, y):
    #initiating global vars
    global screen
    global pen
    global sides
    global polygon
    print("drawing line")
    global count
    count += 1 #increment count because mouse has been clicked
    # print(f"count is now {count}")
    print("count is now ", count)

    if count < sides: #checking to make sure they have only drawn the number of sides - 1 
        polygon.append((x, y)) #add point to our polygon array
        pen.pendown() # put the pen down to start drawing
        pen.goto(x, y) # move the turtle to the clicked position
        pen.penup() # lift the pen up to stop drawing
        return
    else:
        origin() #when there have been (sides - 1) sides made go to the origin 
        screen.onclick(pick_points) #change mouse click to picking points
        count = 0
        return

def pick_points(x, y):
    #initiating global vars
    global screen
    global count
    global pen
    global sides
    global state


    if state != 1 and count < sides: #if still in drawing state or the havent reached max number of cameras
        #making turtle go to point and make a dot there
        pen.penup()
        pen.goto(x, y)
        pen.dot(5, "red")
    else:
        # SHOULD BE GOING TO PARTITIONING FIRST
        # screen.onclick(triangulation)
        screen.onclick(mon_partition)
        screen.onclick(triangulation)
        print("done with placing cameras")
    
    try:
        check = input("Do you want to add another camera? (Y for yes and N for no)")

        #if user chooses n state will change to 1 and no more cameras will be placed
        if check.lower() != "y":
            state = 1
    except:
        count += 1
        return


# ========================================================================================
# ========================================================================================


def left_right(v1, v2, v3, dir):
    if dir == "L":
        return ((v2[0] - v1[0]) * (v3[1] - v1[1])) > ((v2[1] - v1[1]) * ( v3[0] - v1[0]))
    elif dir == "R":
        return ((v2[0] - v1[0]) * (v3[1] - v1[1])) < ((v2[1] - v1[1]) * ( v3[0] - v1[0]))



def mon_partition(x,y):

    upper = []
    lower = []

    print("in partition")
    print("polygon: ", polygon)
    
    y_sort = sorted(polygon, key=lambda x: x[1])
    print("Sorted: ", y_sort)

    for vert in y_sort:
        while len(upper) >= 2 and (left_right(upper[-2], upper[-1], vert, "R")):
            upper.pop()

        while len(lower) >= 2 and (left_right(lower[-2], lower[-1], vert, "L")):
            lower.pop()
        
        upper.append(vert)
        lower.append(vert)

    print("U: ", upper)
    print("L: ", lower)

    return
    # return (upper, lower)


#in the works
def triangulation(x, y):
    print("in triangulation")
    diag = []
    y_sort = sorted(polygon, key=lambda x: x[1])

    for vert in y_sort:

        while len(diag) >= 2 and (left_right(diag[-2], diag[-1, vert, "L"])):
            popped = diag.pop()
            # add diagonal (popped, vert)
        
        while len(diag) >= 2 and (left_right(diag[-2], diag[-1, vert, "R"])):
            popped = diag.pop()
            # add diagonal (popped, vert)
        
        diag.append(vert)
    
    while len(diag) >= 3:
        popped = diag.pop()
        # add diagonal (popped, diag[0])

    

# ========================================================================================
# ========================================================================================



def origin():
    global polygon
    polygon.append((0,0))
    print(polygon)
    global pen
    pen.pendown()
    pen.goto(0,0)

def close():
    global screen
    screen.bye()

pen = turtle.Turtle()
screen = turtle.Screen()
screen.onkeypress(close, "q")
screen.onclick(draw_line)
screen.mainloop()
