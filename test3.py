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
            print("HERE: ", neighbors)
            neighbor1 = neighbors[0]
            neighbor2 = neighbors[1]


            if prev == neighbor1:
                input = neighbor2
            else:
                input = neighbor1


            
            # THIS IS THE ANIMATION PART THAT TAKES EONS TO FINISH 
            #############################################################################
            #############################################################################

            # pen.speed(1)
            # pen.penup()
            # pen.goto(prev)
            # pen.color("red")
            # pen.pendown()
            # pen.goto(y_sorted[i])
            # pen.goto(input)
            # pen.penup()
            # pen.goto(0,0)

            #############################################################################
            #############################################################################
            #############################################################################







            print(f"the other input is {input}")
            

            print(f"neighbor 1 is : {neighbor1}")
            print(f"neighbor 2 is {neighbor2}")
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
                print("potential merge")

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
                print("potential split")

            
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


        index[y_sorted[i]] = i
        index2[i] = y_sorted[i]
        print(f"this is the index: {index}")
    
    pen.penup()
    pen.color("black")
    pen.goto(0,0)

            

    
    print("printing the graph")
    print(f"the order of the points are: {polygon}")
    for node in graph.nodes():
        neighbors = list(graph.neighbors(y_sorted[i]))
        print(node)
        print(graph.nodes[node]["type"])
    
    print("##########################################################")
    for node in graph.nodes():

        # neighbors = list(graph.neighbors(y_sorted[i]))
        # neighbor1 = neighbors[0]
        # neighbor2 = neighbors[1]
        
        print(f"curr node is {node}")
        if graph.nodes[node]["type"] == "merge":
            print("merge")
            curr = node[1]
            temp = index[node]
            temp -= 1
            print(f"the index of this node is {temp}")
            print(index2[temp - 1])


            # di = (node, index2[temp - 1])
            #diagonal(node,index2[temp - 1])
            d = is_diagonal_interior(polygon, node, index2[temp])
            print("trying to go to: ", index2[temp])
            print("diag: ", d)

            while d == False:
                print("temp: ", temp)
                d = is_diagonal_interior(polygon, node, index2[temp])
                
                print("diag inside: ", d)

                if temp == 0:
                    break
                else:
                    temp -= 1
                #print("temp: ", temp)
                #d = is_diagonal_interior(polygon, node, index2[temp])


            graph.add_edge(node, index2[temp])

            pen.penup()
            pen.goto(node)
            pen.pendown()
            pen.goto(index2[temp])
        
        if graph.nodes[node]["type"] == "split":
            print("split")
            curr = node[1]
            temp = index[node]
            if temp == len(polygon) - 1:
                temp = 0
            else:
                temp += 1
            # diagonal(node,index2[temp + 1])
            d = is_diagonal_interior(polygon, node, index2[temp])
            print("trying to go to: ", index2[temp])
            print("diag: ", d)
            
            while d ==  False:
                print("temp: ", temp)
                d = is_diagonal_interior(polygon, node, index2[temp])

                print("diag inside: ", d)

                if temp >= len(polygon) - 1:
                    temp = 0
                else:
                    temp += 1



            graph.add_edge(node, index2[temp])

            pen.color("black")
            pen.penup()
            pen.goto(node)
            pen.pendown()
            pen.goto(index2[temp])
        
        sides = list(graph.neighbors(node))
        print(f"neighbors of {node}")
        for s in sides:
            print(s)
        
        screen.onclick(exit)






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
    



def is_diagonal_interior(polygon, p1, p2):
    """
    Checks if a diagonal line (p1, p2) is interior to a polygon and intersects any of its edges.

    Args:
        polygon (list): List of tuples representing the vertices of the polygon in clockwise or counter-clockwise order.
        p1 (tuple): Tuple representing the starting point of the diagonal line.
        p2 (tuple): Tuple representing the ending point of the diagonal line.

    Returns:
        bool: True if the diagonal is interior to the polygon and intersects any of its edges, False otherwise.
    """
    def is_left(p, q, r):
        # print("CHECKING LEFT ", p, q, r)
        """
        Helper function to determine if point r is on the left side of the line formed by points p and q.

        Args:
            p (tuple): Tuple representing the starting point of the line.
            q (tuple): Tuple representing the ending point of the line.
            r (tuple): Tuple representing the point to be checked.

        Returns:
            bool: True if point r is on the left side of the line formed by points p and q, False otherwise.
        """

    
        # return (q[0] - p[0]) * (r[1] - p[1]) > (q[1] - p[1]) * (r[0] - p[0])
        # val = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

        val = (q[0] - p[0]) * (r[1] - p[1]) > (q[1] - p[1]) * (r[0] - p[0])
        # print("val: ", val)
        return val > 0

    def do_edges_intersect(p1, q1, p2, q2):
        
        # print("CHECKING INTERSECT", p1, q1, p2, q2)
        """
        Helper function to determine if two line segments formed by points (p1, q1) and (p2, q2) intersect.

        Args:
            p1 (tuple): Tuple representing the starting point of the first line segment.
            q1 (tuple): Tuple representing the ending point of the first line segment.
            p2 (tuple): Tuple representing the starting point of the second line segment.
            q2 (tuple): Tuple representing the ending point of the second line segment.

        Returns:
            bool: True if the two line segments intersect, False otherwise.
        """
        # return (is_left(p1, q1, p2) != is_left(p1, q1, q2)) and (is_left(p2, q2, p1) != is_left(p2, q2, q1))
        return (is_left(p1, q1, p2) != is_left(p1, q1, q2)) and (is_left(p2, q2, p1) != is_left(p2, q2, q1))
    
    # Check if the diagonal line (p1, p2) is interior to the polygon
    if not (is_left(polygon[0], polygon[1], p1) ^ is_left(polygon[0], polygon[1], p2)):
        # print("NOT INTERIOR")
        return False

    n = len(polygon)
    lo = 1
    hi = n - 1

    # Binary search to find the two edges of the polygon that the diagonal (p1, p2) intersects
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if is_left(polygon[0], p1, polygon[mid]) == is_left(polygon[0], p1, p2):
            lo = mid
        else:
            hi = mid

    # Check if the diagonal (p1, p2) intersects any of the edges of the polygon
    if do_edges_intersect(p1, p2, polygon[0], polygon[lo]) == True or do_edges_intersect(p1, p2, polygon[lo], polygon[hi]) == True or do_edges_intersect(p1, p2, polygon[hi], polygon[0]) == True:
        final = True
        # print("EDGES INTERSECTED")
    else:
        final = False

    return final


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

