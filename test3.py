import turtle
import networkx as nx
import matplotlib as plt
import math
import numpy as np

global screen
global count
global pen
count = 0
global state 
state = 0
global sides
global polygon
polygon = []
global graph 
graph = nx.Graph()
global types
types = {}
global diagonals
diagonals = []
global index
index = {}
global index2
index2 = {}


##########################################################################################################################

#get how many sides the y_sorted will be
sides = input("How many sides do you want the y_sorted to have?")
sides = int(sides)

if sides <= 3:
    print("Must enter more than 3 sides.")
    turtle.bye()



##########################################################################################################################




#draws the initial lines to build the poylygon
def draw_line(x, y):
    #initiating global vars
    global screen
    global pen
    global sides
    global polygon
    global graph
    print("drawing line")
    global count
    count += 1 #increment count because mouse has been clicked
    # print(f"count is now {count}")
    print("count is now ", count)

    if count < sides: #checking to make sure they have only drawn the number of sides - 1 
        polygon.append((x, y)) #add point to our y_sorted array
        pen.pendown() # put the pen down to start drawing
        pen.goto(x, y) # move the turtle to the clicked position
        pen.penup() # lift the pen up to stop drawing


        ################################################################################
        # creating the graph in here since it has both nodes 
        ################################################################################

        if len(polygon) > 1:
            node_prev = polygon[-2]
        else:
            node_prev = 0

        node_curr = (x,y)

        if node_curr not in graph and node_prev != 0:
            print("add node")
            graph.add_node(node_curr, type = "None")
            graph.add_edge(node_prev,node_curr)
        elif node_curr not in graph and node_prev == 0:
            graph.add_node((0,0), type = "None")
            graph.add_node(node_curr, type = "None")
            graph.add_edge((0,0), node_curr)

        ################################################################################


        return
    else:
        graph.add_edge(polygon[-1], (0,0))
        pen.pendown()
        polygon.append((0,0))
        pen.goto(0, 0) #when there have been (sides - 1) sides made go to the origin 
        screen.onclick(pick_points) #change mouse click to picking points
        count = 0
        return




##########################################################################################################################





def pick_points(x, y):
    #initiating global vars
    global screen
    global count
    global pen
    global sides
    global state
    global graph


    # for node in graph.nodes():
    #     print(node)
    # for edge in graph.edges():
    #     node1, node2 = edge
    #     print(f"Edge: {node1} - {node2}, Nodes: {node1}, {node2}")
    # for edge in graph.edges():
    #     print(edge)

    if state != 1 and count < sides: #if still in drawing state or the havent reached max number of cameras
        #making turtle go to point and make a dot there
        pen.penup()
        pen.goto(x, y)
        pen.dot(5, "red")
    else:
        # SHOULD BE GOING TO PARTITIONING FIRST
        # screen.onclick(triangulation)
        screen.onclick(mon_partition)
        print("done with placing cameras")
    
    count += 1

    try:

        check = input("Do you want to add another camera? (Y for yes and N for no)")

        #if user chooses n state will change to 1 and no more cameras will be placed
        if check.lower() != "y":
            state = 1
    except:
        # count += 1
        print("continue")
        return


def mon_partition(x, y):
    global polygon
    global y_sorted
    global types
    global index
    global index2
    global diagonals

    clockwise_index = {}
    clockwise_index_val = {}

    for i in range(len(polygon)):
        clockwise_index[polygon[i]] = i
        clockwise_index_val[i] = polygon[i]

    


    y_sorted = sorted(polygon, key = lambda x: x[1])
    print(f"this is polygon: {polygon}")
    print(f"this is sorted: {y_sorted}")
    print(clockwise_index)
    print(clockwise_index_val)
    
    for i in reversed(range(len(y_sorted))):
        # start_flag = 0 #determines if any neighbors are starts
        # end_flag = 0 #determines if any neighbors are ends
        
        # neighbors = list(graph.neighbors(y_sorted[i]))
        # neighbor1 = list(neighbors[0])
        # neighbor2 = list(neighbors[1])
        #determine type
        print()
        print(f"curr coord is: {y_sorted[i]}")
        temp = clockwise_index[y_sorted[i]]
        if temp == 0:
            prev = clockwise_index_val[len(polygon) - 1]
        else:
            prev = clockwise_index_val[temp - 1]
        print(f"The index of curr in polygon is {temp}")
        print(f"the current prev is: {prev}")

        if i == len(y_sorted) - 1:
            graph.nodes[y_sorted[i]]["type"] = "end"
        elif i == 0:
            graph.nodes[y_sorted[i]]["type"] = "start"

        else:
            """
            neighbors = list(graph.neighbors(y_sorted[i]))
            for j in neighbors:
                temp = list(graph.neighbors(j))
                for t in graph.neighbors(j):
                    print(f"this is t: {t}")
                    print("test: ", list(graph.neighbors((t))))
                    if graph.nodes[t]["type"] and graph.nodes[t]["type"] == "split":
                        start_flag = 1
                    elif graph.nodes[t]["type"] and graph.nodes[t]["type"] == "merge":
                        end_flag = 1
            neighbor1 = neighbors[0]
            neighbor2 = neighbors[1]
            print(neighbor1[1])
            print(f"start_flag is {start_flag}")
            print(f"flag is {end_flag}")
            """

            neighbors = list(graph.neighbors(y_sorted[i]))
            neighbor1 = neighbors[0]
            neighbor2 = neighbors[1]

            if prev == neighbor1:
                input = neighbor2
            else:
                input = neighbor1
            
            pen.speed(1)
            pen.penup()
            pen.goto(prev)
            pen.color("red")
            pen.pendown()
            pen.goto(y_sorted[i])
            pen.goto(input)

            print(f"the other input is {input}")
            

            print(f"neighbor 1 is : {neighbor1}")
            print(f"neighbor 2 is {neighbor2}")
            check = is_clockwise((neighbor2, y_sorted[i], neighbor1))
            print(f"the points {prev}, {y_sorted[i]} and {input} are clockwise is {check}")
            print(f"the current previous value is {prev}")

            # for n in neighbors:
            #     cousins = list(graph.neighbors(n))
                
            #     for c in cousins:
            #         typeval = graph.nodes[c]['type']
            #         print("Node: ", c, " type: ", typeval)
            #         if typeval == "start":
            #             start_flag = 1
            #         if typeval == "end":
            #             end_flag = 1
            #         print(f"The curr start_flag is {start_flag}")
            #         print(f"The curr end_flag is {end_flag}")



            # print(f"the neighbors are: {neighbor1} and {neighbor2}")

            # cousin = list(graph.neighbors(neighbor1))
            # print(f"cousins are: {cousin}")
            # print(graph.nodes[cousin[0]]["type"])

            # neice = list(graph.neighbors(neighbor2))
            # neice1 = graph.nodes[neice[0]]["type"]
            # neice2 = graph.nodes[neice[1]]["type"]
            if neighbor1[1] > y_sorted[i][1] and neighbor2[1] > y_sorted[i][1]:
                # print("in merge")
                # if start_flag == 1:
                #     graph.nodes[y_sorted[i]]["type"] = "start"
                # else:
                #     graph.nodes[y_sorted[i]]["type"] = "merge"

                test = is_split_vertex(prev, y_sorted[i], input)
                print(f"the function say it is {test}")
                toret = calculate_angle(prev, y_sorted[i], y_sorted[i], input)
                print("potential merge")
                print(f"the function say it is {test}")
                print("angle: ", toret, "##########################################")

                # if is_reflexive_or_convex(prev, y_sorted[i], input) == 'r':
                #     graph.nodes[y_sorted[i]]["type"] = "merge"
                # else:
                #     graph.nodes[y_sorted[i]]["type"] = "end"
                
                if test == True:
                    graph.nodes[y_sorted[i]]["type"] = "merge"
                else:
                    graph.nodes[y_sorted[i]]["type"] = "end"
            
            elif neighbor1[1] < y_sorted[i][1] and neighbor2[1] < y_sorted[i][1]:
                # print("in split")
                # if end_flag == 1:
                #     graph.nodes[y_sorted[i]]["type"] = "end"
                # else:
                #     graph.nodes[y_sorted[i]]["type"] = "split"
                test = is_split_vertex(prev, y_sorted[i], input)
                print(f"the is split function say it is {test}")
                toret = calculate_angle(prev, y_sorted[i], y_sorted[i], input)
                print("potential split")
                print("angle: ", toret, "##########################################")
            
                # if is_reflexive_or_convex(prev, y_sorted[i], input) == 'r':
                #     graph.nodes[y_sorted[i]]["type"] = "split"
                # else:
                #     graph.nodes[y_sorted[i]]["type"] = "start"
                if test == True:
                    graph.nodes[y_sorted[i]]["type"] = "split"
                else:
                    graph.nodes[y_sorted[i]]["type"] = "start"

            else:
                print("regular")
                graph.nodes[y_sorted[i]]["type"] = "regular"

                toret = calculate_angle(prev, y_sorted[i], y_sorted[i], input)
                print("angle: ", toret, "##########################################")

        index[y_sorted[i]] = i
        index2[i] = y_sorted[i]
        print(f"this is the index: {index}")
    
    pen.penup()
    pen.color("black")
    pen.goto(0,0)

            

    
    print("printing the graph")
    print(f"the order of the points are: {polygon}")
    for node in graph.nodes():
        print(node)
        print(graph.nodes[node]["type"])
    
    print("##########################################################")
    for node in graph.nodes():
        print(f"curr node is {node}")
        if graph.nodes[node]["type"] == "merge":
            print("merge")
            curr = node[1]
            temp = index[node]
            print(f"the index of this node is {temp}")
            print(index2[temp + 1])
            graph.add_edge(node, index2[temp - 1])

            pen.penup()
            pen.goto(node)
            pen.pendown()
            pen.goto(index2[temp - 1])
        
        if graph.nodes[node]["type"] == "split":
            print("split")
            curr = node[1]
            temp = index[node]
            graph.add_edge(node, index2[temp + 1])

            pen.color("black")
            pen.penup()
            pen.goto(node)
            pen.pendown()
            pen.goto(index2[temp - 1])
        
        sides = list(graph.neighbors(node))
        print(f"neighbors of {node}")
        for s in sides:
            print(s)
        
        screen.onclick(exit)

def is_reflexive_or_convex(coord1, coord2, coord3):
    # Extract x and y values from the coordinates
    x1, y1 = coord1
    x2, y2 = coord2
    x3, y3 = coord3

    # Compute the cross product
    cross_product = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)

    print(f"the cross product of these angles are {cross_product}")

    # if cross_product == 0:
    #     # If cross product is 0, points are collinear
    #     return 'c'
    if cross_product < 0:
        # If cross product is negative, points are convex
        print("is reflexive")
        return 'r'
    elif cross_product > 0:
        # Otherwise, points are neither reflexive nor convex
        print("is not reflexive")
        return 'c'

def is_clockwise(points):
    """
    Determines if a set of points are arranged in clockwise order.

    Args:
        points (list): A list of tuples representing the points as (x, y) coordinates.

    Returns:
        bool: Returns True if the points are arranged in clockwise order, False otherwise.
    """
    n = len(points)
    signed_area = 0

    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]  # Wrap around to the first point for the last point
        signed_area += (x2 - x1) * (y2 + y1)
    if signed_area < 0:
        print("clockwise")
    else:
        print("counter clockwise")
    return signed_area < 0

def calculate_angle(A, B, C, D):
    """
    Calculates the angle between two edges based on their vertex coordinates.

    Args:
        A (tuple): Coordinates of the first vertex of Edge 1 as (x, y) or (x, y, z).
        B (tuple): Coordinates of the second vertex of Edge 1 as (x, y) or (x, y, z).
        C (tuple): Coordinates of the first vertex of Edge 2 as (x, y) or (x, y, z).
        D (tuple): Coordinates of the second vertex of Edge 2 as (x, y) or (x, y, z).

    Returns:
        float: Angle between the two edges in degrees.
    """
    # Calculate vectors
    AB = (B[0] - A[0], B[1] - A[1])
    CD = (D[0] - C[0], D[1] - C[1])

    # Calculate dot product
    dot_product = AB[0] * CD[0] + AB[1] * CD[1]
    # dot_product = np.dot(A, B)

    # Calculate magnitudes
    magnitude1 = math.sqrt(AB[0]**2 + AB[1]**2)
    magnitude2 = math.sqrt(CD[0]**2 + CD[1]**2)

    # Calculate cosine of angle
    cosine_theta = dot_product / (magnitude1 * magnitude2)

    # Calculate angle in radians
    theta_rad = math.acos(cosine_theta)

    # Convert angle to degrees
    angle_degrees = math.degrees(theta_rad)

    return angle_degrees

def is_split_vertex(vertex, prev_vertex, next_vertex):
    """
    Check if a vertex is a split vertex based on cross product sign.
    """
    # Calculate cross product using coordinates of three vertices
    cross_product = (vertex[0] - prev_vertex[0]) * (next_vertex[1] - vertex[1]) - (vertex[1] - prev_vertex[1]) * (next_vertex[0] - vertex[0])

    # Check if cross product changes sign
    if cross_product > 0:
        print("1")
        return True  # Split vertex
    else:
        print("2")
        return False  # Not a split vertex
    
def diagonal(diagonal, v1, v2):
    
    """
    get edge before and after v1
    take cross product of edges
    if > 0 --> cross each edge with the diagonal about to be drawn
                if both <= 0, return false
    else:
        cross each edge with the diagonal about to be drawn
        if both <= 0, return false

    repeat for v2

    completely after all this: return True

    """
    v1_n = list(graph.neighbors(v1))
    v1_e1 = v1_n[0]

def exit(x, y):
    global screen
    screen.bye()

    
    #print(diagonals)

    # for d in diagonals:
    #     pen.penup()
    #     pen.goto(d[0])
    #     pen.pendown()
    #     pen.goto(d[1])




    
    print(types)

pen = turtle.Turtle()
screen = turtle.Screen()
screen.onclick(draw_line)
screen.mainloop()

