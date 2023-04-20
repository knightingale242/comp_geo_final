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
sides = 8

if sides <= 3:
    print("Must enter more than 3 sides.")
    turtle.bye()



##########################################################################################################################


def hard_code(x,y):
    pen.speed(3)
    for point in polygon:
        pen.color("black")
        pen.pendown()
        pen.goto(point)
    
    screen.onclick(pick_points)

def hard_monotone(x, y):
    pen.goto(0,0)


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

            pen.speed(1)
            pen.penup()
            pen.goto(prev)
            pen.color("red")
            pen.pendown()
            pen.goto(y_sorted[i])
            pen.dot(5, "black")
            pen.goto(input)
            pen.penup()
            pen.goto(0,0)

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
            d = check_line_polygon_edge_intersections((node, index2[temp]), polygon)
            print("trying to go to: ", index2[temp])
            print("diag: ", d)

            while True:
                if d == True: # if diagonal intersect
                    print("temp: ", temp)
                    d = check_line_polygon_edge_intersections((node, index2[temp]), polygon)
                    
                    print("diag inside: ", d)

                    if temp == 0:
                        break
                    else:
                        temp -= 1
                    #print("temp: ", temp)
                    #d = is_diagonal_interior(polygon, node, index2[temp])
                else:
                    print(f"the index of temp is{temp}")
                    print(index2[temp])
                    print("NO INTERSECTION")
                    break


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
            d = check_line_polygon_edge_intersections((node, index2[temp]), polygon)
            print("trying to go to: ", index2[temp])
            print("diag: ", d)
            
            while True:
                if d ==  True:
                    print("temp: ", temp)
                    d = check_line_polygon_edge_intersections((node, index2[temp]), polygon)

                    print("diag inside: ", d)

                    if temp >= len(polygon) - 1:
                        temp = 0
                    else:
                        temp += 1
                else:
                    print(f"the index of temp is{temp}")
                    print(index2[temp])
                    print("NO INTERSECTION")
                    break



            graph.add_edge(node, index2[temp - 1])

            pen.color("black")
            pen.penup()
            pen.goto(node)
            pen.pendown()
            pen.goto(index2[temp - 1])
        
        # sides = list(graph.neighbors(node))
        # print(f"neighbors of {node}")
        # for s in sides:
        #     print(s)

        pen.penup()
        pen.goto(polygon[6])
        pen.pendown()
        pen.goto(polygon[4])

        pen.penup()
        pen.goto(polygon[6])
        pen.pendown()
        pen.goto(polygon[3])

        pen.penup()
        pen.goto(polygon[7])
        pen.pendown()
        pen.goto(polygon[3])

        pen.penup()
        pen.goto(polygon[0])
        pen.pendown()
        pen.goto(polygon[2])

        pen.penup()
        pen.goto(polygon[5])
        pen.dot(10, "green")
        pen.goto(polygon[6])
        pen.dot(10, "blue")
        pen.goto(polygon[4])
        pen.dot(10, "red")
        pen.goto(polygon[7])
        pen.dot(10, "red")
        pen.goto(polygon[0])
        pen.dot(10, "green")
        pen.goto(polygon[1])
        pen.dot(10, "red")
        pen.goto(polygon[2])
        pen.dot(10, "blue")
        pen.goto(polygon[3])
        pen.dot(10, "green")
        pen.exit()


    nodes = list(graph.nodes())
    print(f"nodes are {nodes}")
    edges = list(graph.edges())
    print(f"edges are {edges}")
    triangles = triangulate_polygon(nodes, edges)
    print(f"triangles is {triangles}")
        
    for t in triangles:
        pen.speed(10)
        pen.penup()
        pen.goto(t[0])
        pen.pencolor("blue")
        pen.pendown()
        pen.goto(t[1])
        pen.goto(t[2])

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

######################testing new intersection code########################################################
def check_line_polygon_edge_intersections(line, polygon):
    line_start, line_end = line
    print(f"The start and end of the line are {line_start} and {line_end}")
    for edge in graph.edges():
        edge_start = edge[0]
        edge_end = edge[1]
        print(f"curr line being checked is {edge_start} to {edge_end}")
        check = do_lines_intersect(line_start, line_end, edge_start, edge_end)
        print(f"check is {check}")

        if check == True:
            return True
    print("no intersections")
    return False


def calculate_line_intersection(line_start, line_end, edge_start, edge_end):
    # Calculate the point of intersection between a line and an edge
    x1, y1 = line_start
    x2, y2 = line_end
    x3, y3 = edge_start
    x4, y4 = edge_end

    # Calculate the denominator of the line intersection formula
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom == 0:
        # The lines are parallel or collinear, so there is no intersection
        return None

    # Calculate the numerators of the line intersection formula
    num1 = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
    num2 = (x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)

    # Calculate the parameters t and u of the line intersection formula
    t = num1 / denom
    u = -num2 / denom

    if 0 <= t <= 1 and 0 <= u <= 1:
        # The lines intersect within the line segment, so calculate the point of intersection
        x = x1 + t * (x2 - x1)
        y = y1 + t * (y2 - y1)

        return (x, y)

    # The lines intersect outside the line segment, so there is no intersection
    return None


def point_on_edge(point, edge_start, edge_end):
    # Check if a point lies on an edge
    min_x = min(edge_start[0], edge_end[0])
    max_x = max(edge_start[0], edge_end[0])
    min_y = min(edge_start[1], edge_end[1])
    max_y = max(edge_start[1], edge_end[1])

    return min_x <= point[0] <= max_x and min_y <= point[1] <= max_y
###############################################################################################################################################






def do_lines_intersect(line1_start, line1_end, line2_start, line2_end):
    """
    Check if two lines intersect.

    Args:
        line1_start (tuple): Start point of line 1 as a tuple of (x, y) coordinates.
        line1_end (tuple): End point of line 1 as a tuple of (x, y) coordinates.
        line2_start (tuple): Start point of line 2 as a tuple of (x, y) coordinates.
        line2_end (tuple): End point of line 2 as a tuple of (x, y) coordinates.

    Returns:
        bool: True if the lines intersect, False otherwise.
    """
    # Extract coordinates from tuples
    x1, y1 = line1_start
    x2, y2 = line1_end
    x3, y3 = line2_start
    x4, y4 = line2_end

    # Calculate the slopes of the lines
    slope1 = (y2 - y1) * (x4 - x3) - (x2 - x1) * (y4 - y3)
    slope2 = (y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)

    # Check if the lines are parallel
    if slope1 == 0 and slope2 == 0:
        # Check if the lines lie on the same line segment
        if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2) or max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
            return False
        return True

    # Check if the lines intersect
    if slope1 != 0 and slope2 != 0 and (slope1 > 0) != (slope2 > 0):
        slope3 = (y4 - y3) * (x1 - x3) - (x4 - x3) * (y1 - y3)
        slope4 = (y4 - y3) * (x2 - x3) - (x4 - x3) * (y2 - y3)
        if slope3 != 0 and slope4 != 0 and (slope3 > 0) != (slope4 > 0):
            return True

    return False
############################################################################################################################
def triangulate_monotone_polygon(vert_nodes, poly_edges):
    """
    Triangulate a random polygon that has gone through monotone partitioning.
    
    Args:
        vert_nodes (list): List of vertices of the polygon as tuples of (x, y) coordinates.
        poly_edges (list): List of edges of the polygon as tuples of vertex indices.
        
    Returns:
        list: List of triangles as tuples of vertex indices.
    """

    print("vertices inside*****************: ", vert_nodes)
    # Sort vertices by y-coordinate
    sorted_vertices = sorted(vert_nodes, key=lambda v: (v[1], v[0]))

    # Create a stack to keep track of vertices
    vertex_stack = []

    # Initialize the triangulation result as an empty list
    triangles = []

    # Loop through each vertex in the sorted list
    for vertex in sorted_vertices:
        # Check if the vertex is a left or right vertex
        is_left_vertex = False
        for edge in poly_edges:
            print(f"vertex is {vertex} and edge is {edge}")
            if edge[0] == vertex:
                print("is left")
                is_left_vertex = True
                break
            elif edge[1] == vertex:
                print("not left")
                is_left_vertex = False
                break

        print("************************len1: ", len(vertex_stack))

        if len(vertex_stack) < 2:
            print("NOT ENOUGH POINTS YETTTTTTTTTTTTTTTTTTT")
            vertex_stack.append(vertex)
        else:
        
            # If the vertex is a left vertex, perform triangulation
            if is_left_vertex:
                print("IN THE LEFTTTTTTTTTTTTTTTTTTTTTTTT")
                # Pop vertices from the stack and triangulate
                while len(vertex_stack) > 1:
                    v1 = vertex_stack[-1]
                    v2 = vertex_stack[-2]
                    
                    # Check if the diagonal v1-v2 is inside the polygon and does not intersect other edges
                    print("is inside poly?????????????? ", is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices))
                    print("itersecting things?????????????????????? ", check_line_polygon_edge_intersections((v1, v2), poly_edges))

                    # if is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices) and not check_line_polygon_edge_intersections((v1, v2), poly_edges):
                    if is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices):
                        print("HELLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO 1")
                        triangles.append((v1, v2, vertex))
                        vertex_stack.pop()
                    else:
                        print("nope no bueno")
                        break
                
                # Push the current vertex onto the stack
                vertex_stack.append(vertex)
                print("the current vertex stack is ", vertex_stack)
                print("******************************len2: ", len(vertex_stack))
            
            # If the vertex is a right vertex, pop vertices from the stack and triangulate
            else:
                print("RIGHTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                while len(vertex_stack) > 1:
                    v1 = vertex_stack[-1]
                    v2 = vertex

                    print("is inside poly?????????????? ", is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices))
                    print("itersecting things?????????????????????? ", check_line_polygon_edge_intersections((v1, v2), poly_edges))
                    # Check if the diagonal v1-v2 is inside the polygon and does not intersect other edges
                    # if is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices) and not check_line_polygon_edge_intersections((v1, v2), poly_edges):
                    if is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices):
                        # print("is inside poly?????????????? ", is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices))
                        # print("itersecting things?????????????????????? ", check_line_polygon_edge_intersections((v1, v2), poly_edges))

                        print("HELLLOOOOOOOOOOOOOOOOOOOOOOOOOOOO 2")
                        triangles.append((v1, v2, vertex))
                        vertex_stack.pop()
                    else:
                        print("nah this aint it")
                        break
        
        print("in func tri: ", triangles)
    
    return triangles

def is_diagonal_inside_polygon(v1, v2, vertex, sorted_vertices):
    """
    Check if a diagonal is inside a polygon.

    Args:
        v1 (tuple): First vertex of the diagonal as a tuple of (x, y) coordinates.
        v2 (tuple): Second vertex of the diagonal as a tuple of (x, y) coordinates.
        vertex (tuple): Third vertex of the diagonal as a tuple of (x, y) coordinates.
        sorted_vertices (list): List of vertices of the polygon sorted by y-coordinate.

    Returns:
        bool: True if the diagonal is inside the polygon, False otherwise.
    """
    # Get the index of the vertex in the sorted list
    vertex_index = sorted_vertices.index(vertex)

    # Get the previous and next vertices in the sorted list
    prev_vertex = sorted_vertices[vertex_index - 1]
    next_vertex = sorted_vertices[(vertex_index + 1) % len(sorted_vertices)]

    # Check if the diagonal is inside the polygon by checking the orientation of the triangle formed by v1, v2, and vertex
    # If the orientation is counter-clockwise, the diagonal is inside the polygon
    # If the orientation is clockwise, the diagonal is outside the polygon
    orientation_v1_v2_vertex = orientation(v1, v2, vertex)
    orientation_v1_v2_prev = orientation(v1, v2, prev_vertex)
    orientation_v1_v2_next = orientation(v1, v2, next_vertex)

    return (
        (orientation_v1_v2_vertex == "CCW")
        and (orientation_v1_v2_prev != "CCW")
        and (orientation_v1_v2_next != "CCW")
    )


def orientation(p, q, r):
    """
    Check the orientation of three points.

    Args:
        p (tuple): First point as a tuple of (x, y) coordinates.
        q (tuple): Second point as a tuple of (x, y) coordinates.
        r (tuple): Third point as a tuple of (x, y) coordinates.

    Returns:
        str: "CW" if the orientation is clockwise, "CCW" if the orientation is counter-clockwise, "COLLINEAR" if the points are collinear.
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

    if val == 0:
        return "COLLINEAR"
    elif val > 0:
        return "CW"
    else:
        return "CCW"
    



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