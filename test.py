import turtle
import math
import networkx as nx
import matplotlib as plt
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


##########################################################################################################################

#get how many sides the polygon will be
sides = input("How many sides do you want the polygon to have?")
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
        polygon.append((x, y)) #add point to our polygon array
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
            graph.add_node(node_curr, c = 0)
            graph.add_edge(node_prev,node_curr)
        elif node_curr not in graph and node_prev == 0:
            graph.add_node((0,0), c = 0)
            graph.add_node(node_curr, c = 0)
            graph.add_edge((0,0), node_curr)

        ################################################################################


        return
    else:
        graph.add_edge(polygon[-1], (0,0))
        origin() #when there have been (sides - 1) sides made go to the origin 
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


        # screen.onclick(mon_partition)
        screen.onclick(triangulation)
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



##########################################################################################################################


def left_right(p, q, r):

    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])



    if val == 0:
        # print("Collinear")
        return 0
    elif val > 0:
        # print("Left")
        return 1
    elif val < 0:
        # print("Right")
        return 2
    
    # s1 = (v2[0] - v1[0]) * (v3[1] - v1[1])
    # s2 = (v2[1] - v1[1]) * ( v3[0] - v1[0])

    # if s1 < s2: 
    #     print("up")
    # elif s1 > s2:
    #     print("low")
    # elif s1 == s2:
    #     print("idk")

    # if dir == "L":
    #     return ((v2[0] - v1[0]) * (v3[1] - v1[1])) > ((v2[1] - v1[1]) * ( v3[0] - v1[0]))
    # elif dir == "R":
    #     return ((v2[0] - v1[0]) * (v3[1] - v1[1])) < ((v2[1] - v1[1]) * ( v3[0] - v1[0]))
    # elif dir == "F":
    #     # return ((v2[0] - v1[0]) * (v3[1] - v1[1])) == ((v2[1] - v1[1]) * ( v3[0] - v1[0]))
    #     return (v2[0] - v1[0]) * (v3[1] - v1[1]) == (v2[1] - v1[1]) * (v3[0] - v1[0]) and (v2[0] - v1[0]) * (v3[0] - v1[0]) + (v2[1] - v1[1]) * (v3[1] - v1[1]) > 0


##########################################################################################################################

def in_tri(p, t):

    o1 = left_right(t[0], t[1], p)
    o2 = left_right(t[1], t[2], p)
    o3 = left_right(t[2], t[0], p)

    if (o1 == o2) and (o2 == o3):
        return True
    else:
        return False


##########################################################################################################################


def reflexive(A, B, C):
    vector_AB = (B[0] - A[0], B[1] - A[1])
    vector_BC = (C[0] - B[0], C[1] - B[1])

    dot_product = vector_AB[0] * vector_BC[0] + vector_AB[1] * vector_BC[1]

    cross_product = (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])

    if cross_product > 0:
        # counter - WE HAVE THIS
        print("Counter")

        magnitude_AB = ((vector_AB[0]) ** 2 + (vector_AB[1]) ** 2) ** 0.5
        magnitude_BC = ((vector_BC[0]) ** 2 + (vector_BC[1]) ** 2) ** 0.5

        if magnitude_AB == 0 or magnitude_BC == 0:
            print("Error: Zero magnitude detected.")
            return True

        cosine_angle = dot_product / (magnitude_AB * magnitude_BC)

        angle_radians = math.acos(cosine_angle)
        angle_degrees = math.degrees(angle_radians)

        if cosine_angle > 0:
            print(f"The angle is reflexive with an angle of {angle_degrees} degrees.")
            return True
        else:
            print(f"The angle is not reflexive with an angle of {angle_degrees} degrees.")
            return False
        

    elif cross_product < 0:
        # clock
        if dot_product > 0:
            print("reflexive")
            return True
        else:
            print("not reflexive!!!!!!!!!!!!")
            return False
        
        # if cosine_angle < 0:
        #     print(f"The angle is reflexive with an angle of {angle_degrees} degrees.")
        #     return True
        # else:
        #     print(f"The angle is not reflexive with an angle of {angle_degrees} degrees.")
        #     return False

    

    # angle_radians = math.atan2(vector_BC[1], vector_BC[0]) - math.atan2(vector_AB[1], vector_AB[0])
    # angle_degrees = math.degrees(angle_radians)

    # if angle_degrees > 180:
    #     return True
    # else:
    #     return False
    

##########################################################################################################################



def shoelace(p1, p2, p3):
    
    # area = 0.5 * abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    area = (p1[0] * p2[1] + p2[0] * p3[1] + p3[0] * p1[1]) - (p2[0] * p1[1] + p3[0] * p2[1] + p1[0] * p3[1])
    print("area: ", area)

    if area >= 0:
        return True
    else:
        return False

    #return (x1 * y2 + x2 * y3 + x3 * y1) - (x2 * y1 + x3 * y2 + x1 * y3)

def triangulation(x,y):

    global pen 
    global graph 
    global polygon
    
    # left = []
    # right = []

    v_stack = []
    triangles = []


    print("in triangulation")
    print("polygon: ", polygon)

    if left_right(polygon[0], polygon[1], polygon[2]) == 2:

        polygon.reverse()
        print("Rev needed -----------------------------------")
    
    # y_sort = sorted(polygon, key=lambda x: x[1])
    y_sort = sorted(polygon)
    print("Sorted: ", y_sort) 

    for vert in y_sort:
        print("Vert1: ", vert)
        while len(v_stack) > 1 and left_right(v_stack[-2], v_stack[-1], vert) != 1:
            t = (v_stack[-2], v_stack[-1], vert)
            triangles.append(t)
            v_stack.pop()
        
        v_stack.append(vert)
        print("stack: ", v_stack)
        print("Tri: ", triangles)

    v_stack.reverse()
    print("reversed stack: ", v_stack)

    for vert in y_sort:
        print("Vert2: ", vert)

        while len(v_stack) > 1 and left_right(v_stack[-2], v_stack[-1], vert) != 1:
            t = (v_stack[-2], v_stack[-1], vert)

            if t not in triangles:
                triangles.append(t)
            v_stack.pop()
        
        v_stack.append(vert)
        print("stack: ", v_stack)
        print("Tri: ", triangles)

    while len(v_stack) > 2:

        v = v_stack.pop()
        print("Vert3: ", v)

        t = (v_stack[-1], v_stack[-2], v)

        if t not in triangles:
            triangles.append(t)
        
        print("Tri: ", triangles)


    encountered = set()
    tri_final = []

    # for i in range(len(triangles)):
    #     for j in range(i+1, len(triangles)):
    #         for k in range(j+1, len(triangles)):
    #             p1 = triangles[i]
    #             p2 = triangles[j]
    #             p3 = triangles[k]

    #             print("TEST: ", p1)
    #             # area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    #             area = 0.5 * abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
    #             if area > 0:
    #                 tri_final.append((p1, p2, p3))

 
    # print("BEFORE LOOP: ", triangles)
    for t in triangles:

        t_set = frozenset(t)
        # print("tset: ", t_set)
        print("t: ", t)

        ref = reflexive(t[0], t[1], t[2])
        print("Ref: ", ref)

        shoe = shoelace(t[0], t[1], t[2])
        print("shoe: ",shoe)

        val = in_tri(t[-1], t)
        # if (val == True) or (ref == True):
        #     triangles.remove(t)
        print("val: ", val)
        
        if (t_set not in encountered) and (val == False) and (ref == False):
            encountered.add(t_set)
            tri_final.append(t)
            print("IN TRIANGLE ==============================")

        

    print("triangles: ", tri_final)


##########################################################################################################################


"""
def mon_partition(x,y):
    global pen
    global graph

    upper = []
    lower = []


    print("in partition")
    print("polygon: ", polygon)
    
    y_sort = sorted(polygon, key=lambda x: x[1])
    print("Sorted: ", y_sort)

    for vert in y_sort:
        print("Vert: ", vert)
        print("U: ", upper)
        print("L: ", lower)

        while len(upper) >= 2 and (left_right(upper[-2], upper[-1], vert, "R") or left_right(upper[-2], upper[-1], vert, "F")):
            print("1")
            upper.pop()

        while len(lower) >= 2 and (left_right(lower[-2], lower[-1], vert, "L") or left_right(lower[-2], lower[-1], vert, "F")):
            #if (left_right(lower[-2], lower[-1], vert, "L")):
            print("2")
            lower.pop()
        
        upper.append(vert)
        lower.append(vert)

    # if len(upper) < 2:
    #     upper = []

    # if len(lower) < 2:
    #     lower = []

    print("U: ", upper)
    print("L: ", lower)

    for u in upper:
        pen.penup()
        pen.goto(u)
        pen.dot(10, "blue")
    
    for l in lower:
        pen.penup()
        pen.goto(l)
        pen.dot(10, "green")

    screen.onclick(triangulation)

    return
    # return (upper, lower)




##########################################################################################################################




#in the works
def triangulation(x, y):
    global graph 

    print("in triangulation")
    diag = []
    y_sort = sorted(polygon, key=lambda x: x[1])

    for vert in y_sort:

        while len(diag) >= 2 and (left_right(diag[-2], diag[-1], vert, "L")):
            popped = diag.pop()
            graph.add_edge(popped,vert)
            # add diagonal (popped, vert)
        
        while len(diag) >= 2 and (left_right(diag[-2], diag[-1], vert, "R")):
            popped = diag.pop()
            graph.add_edge(popped,vert)
            # add diagonal (popped, vert)
        
        diag.append(vert)
    
    while len(diag) >= 3:
        popped = diag.pop()
        graph.add_edge(popped,diag[0])
        # add diagonal (popped, diag[0])

    three_color()


"""
##########################################################################################################################



def three_color():
    global graph

    count = [0,0,0]
    # use a.remove(#)

    for node in graph.nodes():

        print("Node: ", node)
        
        available = [1,2,3]

        color = graph.nodes[node]['c']
        if color == 0:
            homies = list(graph.neighbors(node))

            bud1 = homies[0]
            bud2 = homies[1]

            print("neighbors: ", bud1, bud2)

            c1 = graph.nodes[bud1]['c']
            c2 = graph.nodes[bud2]['c']

            print("Colors: ", c1, c2)

            if c1 in available:
                available.remove(c1)
            if c2 in available:
                available.remove(c2)
            
            print("available: ", available)
            
            if len(available) > 1:
                col_curr = count.index(min(count)) + 1
            elif len(available) == 1:
                col_curr = available[0]
            
            count[col_curr-1] += 1

            print("color assigned: ", col_curr)
            graph.nodes[node]['c'] = col_curr
    
    print("Colors count: ", count)
    print("End ========================================")
    

            




    
##########################################################################################################################



def origin():
    global polygon
    polygon.append((0,0))
    print(polygon)
    global pen
    pen.pendown()
    pen.goto(0,0)


##########################################################################################################################



def close():
    global screen
    screen.bye()


##########################################################################################################################


pen = turtle.Turtle()
screen = turtle.Screen()
screen.onkeypress(close, "q")
screen.onclick(draw_line)
screen.mainloop()
