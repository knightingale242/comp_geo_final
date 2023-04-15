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
sides = input("how mamy sides do you want the polygon to have")
sides = int(sides)

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
    print(f"count is now {count}")

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
        screen.onclick(triangulation)
        print("done with placing cameras")
    
    try:
        check = input("do you want to add another camera. (Y for yes and N for no)")

        #if user chooses n state will change to 1 and no more cameras will be placed
        if check.lower() != "y":
            state = 1
    except:
        count += 1
        return


#in the works
def triangulation(x, y):
    print("in triangulation")
    


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
