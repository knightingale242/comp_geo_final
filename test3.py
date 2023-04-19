import turtle
import networkx as nx
import matplotlib as plt

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

    y_sorted = sorted(polygon, key = lambda x: x[1])
    print(f"this is polygon: {polygon}")
    print(f"this is sorted: {y_sorted}")
    
    for i in range(len(y_sorted)):
        flag1 = 0
        flag2 = 0
        # neighbors = list(graph.neighbors(y_sorted[i]))
        # neighbor1 = list(neighbors[0])
        # neighbor2 = list(neighbors[1])
        #determine type
        print(f"curr coord is: {y_sorted[i]}")
        if i == len(y_sorted) - 1:
            graph.nodes[y_sorted[i]]["type"] = "start"
        elif i == 0:
            graph.nodes[y_sorted[i]]["type"] = "end"

        else:
            neighbors = list(graph.neighbors(y_sorted[i]))
            for j in neighbors:
                temp = list(graph.neighbors(j))
                for t in graph.neighbors(j):
                    print(f"this is t: {t}")
                    print("test: ", list(graph.neighbors((t))))
                    if graph.nodes[t]["type"] and graph.nodes[t]["type"] == "split":
                        flag1 = 1
                    elif graph.nodes[t]["type"] and graph.nodes[t]["type"] == "merge":
                        flag2 = 1
            neighbor1 = neighbors[0]
            neighbor2 = neighbors[1]
            print(neighbor1[1])
            print(f"flag1 is {flag1}")
            print(f"flag is {flag2}")
            # print(f"the neighbors are: {neighbor1} and {neighbor2}")

            # cousin = list(graph.neighbors(neighbor1))
            # print(f"cousins are: {cousin}")
            # print(graph.nodes[cousin[0]]["type"])

            # neice = list(graph.neighbors(neighbor2))
            # neice1 = graph.nodes[neice[0]]["type"]
            # neice2 = graph.nodes[neice[1]]["type"]
            if neighbor1[1] > y_sorted[i][1] and neighbor2[1] > y_sorted[i][1]:
                print("in merge")
                if flag1 == 1:
                    graph.nodes[y_sorted[i]]["type"] = "start"
                else:
                    graph.nodes[y_sorted[i]]["type"] = "merge"
            
            elif neighbor1[1] < y_sorted[i][1] and neighbor2[1] < y_sorted[i][1]:
                print("in split")
                if flag2 == 1:
                    graph.nodes[y_sorted[i]]["type"] = "end"
                else:
                    graph.nodes[y_sorted[i]]["type"] = "split"

            else:
                graph.nodes[y_sorted[i]]["type"] = "good"

        index[y_sorted[i]] = i
        index2[i] = y_sorted[i]
        print(f"this is the index: {index}")

            

    
    print("printing the graph")
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

            pen.penup()
            pen.goto(node)
            pen.pendown()
            pen.goto(index2[temp - 1])
        
        sides = list(graph.neighbors(node))
        print(f"neighbors of {node}")
        for s in sides:
            print(s)
        

    
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

