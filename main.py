import turtle

def draw_n_lines(n):
    """Draws `n` lines connecting the last and current mouse positions"""

    # create a new Turtle graphics window
    screen = turtle.Screen()

    # create a turtle to draw with
    t = turtle.Turtle()

    # define a callback function for mouse clicks
    def on_click(x, y):
        """Called whenever the user clicks the mouse"""
        nonlocal t
        nonlocal last_pos

        # draw a line from the last position to the current position
        t.goto(x, y)

        # update the last position
        last_pos = (x, y)

    # register the callback function for mouse clicks
    screen.onclick(on_click)

    # get the initial position of the mouse
    last_pos = screen.onclick(on_click)

    # draw `n` lines connecting the last and current mouse positions
    for i in range(n):
        screen.onclick(on_click)
    
    # enter the main loop
    turtle.mainloop()

draw_n_lines(5)