
import numpy as np
import math
import heapq
import cv2
import pygame

def left(c_node):
    x = c_node[0]
    y = c_node[1]

    x = x - 1
    new_node = (x, y)

    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node


def down(c_node):
    x = c_node[0]
    y = c_node[1]

    y = y - 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node

def top(c_node):
    x = c_node[0]
    y = c_node[1]

    y = y + 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node

def right(c_node):
    x = c_node[0]
    y = c_node[1]

    x = x + 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node

def down_left(c_node):
    x = c_node[0]
    y = c_node[1]

    x = x - 1
    y = y - 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node

def top_left(c_node):
    x = c_node[0]
    y = c_node[1]

    x = x - 1
    y = y + 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node


def down_right(c_node):
    x = c_node[0]
    y = c_node[1]

    x = x + 1
    y = y - 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node


def top_right(c_node):
    x = c_node[0]
    y = c_node[1]

    x = x + 1
    y = y + 1
    new_node = (x, y)
    if x >= 0 and y >= 0:
        return new_node
    else:
        return c_node

def generateGraph(i, j):

    graph = {}

    if i == 0 and j == 0:
        graph[(i, j)] = {(i+1, j+1), (i+1, j), (i, j+1)}

    elif i == 400 and j == 0:
        graph[(i, j)] = {(i-1, j), (i-1, j+1), (i, j+1)}

    elif i == 400 and j == 250:
        graph[(i, j)] = {(i-1, j), (i-1, j-1), (i, j-1)}

    elif j == 400 and i == 0:
        graph[(i, j)] = {(i, j-1), (i+1, j-1), (i+1, j)}

    elif j == 250 and i != 0 and i != 400:
        graph[(i, j)] = {(i-1, j), (i+1, j), (i+1, j-1), (i, j-1), (i-1, j-1)}

    elif i == 0 and j != 0 and j != 400:
        graph[(i, j)] = {(i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)}

    elif i == 400 and j != 0 and j != 250:
        graph[(i, j)] = {(i, j-1), (i, j+1), (i-1, j-1), (i-1, j), (i-1, j+1)}

    elif j == 0 and i != 0 and i != 400:
        graph[(i, j)] = {(i-1, j), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)}

    else:
        graph[(i, j)] = {(i-1, j), (i-1, j+1), (i-1, j-1), (i+1, j-1), (i+1, j), (i+1, j+1), (i, j-1), (i, j+1)}

    return graph



def cost_calculation(graph):

    cost_dic = {}

    for key,value in graph.items():
        cost_dic[key]={}
        for n in value:

            if (n == top(key)) or (n == down(key)) or (n == left(key)) or (n == right(key)):
                cost_dic[key][n] = 1

            elif (n == down_left(key)) or (n == top_left(key)) or (n == down_right(key)) or (n == top_right(key)):
                cost_dic[key][n] = 1.4

    return cost_dic


backtracking = {}

visited = []


all_distance = {}

def dijkstra(graph, start):

    all_distance[start] = 0

    visited.append(start)

    for vertex, edge in graph.items():
        all_distance[vertex] = math.inf

    priority_queue = [(0, start)]

    check = 1

    while len(priority_queue) > 0 and check != 0:

        curr_dist,curr_vert = heapq.heappop(priority_queue)

        if curr_dist > all_distance[curr_vert]:
            continue
        for neighbour, cost in graph[curr_vert].items():

            distance = curr_dist + cost

            if distance < all_distance[neighbour]:
                backtracking[neighbour] = {}

                backtracking[neighbour][distance] = curr_vert
                all_distance[neighbour] = distance

                heapq.heappush(priority_queue, (distance, neighbour))

                if neighbour not in visited:

                    visited.append(neighbour)

                    if neighbour == goal:

                        check = 0

                        break
    return all_distance, visited,backtracking


def back_track (goal, start):

    back_track_list = []
    back_track_list.append(start)
    c = 0
    while c != 1:
        for k, v in backtracking.items():
            for k2, v2 in v.items():
                if k == start:
                    if v2 not in back_track_list:
                     back_track_list.append(start)
                     start = v2
                    if v2 == goal:
                        c = 1
                        break

    return back_track_list


def robot(size_x, size_y,start,goal):

    size_x += 1

    size_y += 1

    all_points = []
    for i in range(0,401):
        for j in range(251):
            all_points.append((i,j))

    list_of_all_obstacles = []

    for c in all_points:
        x = c[0]
        y = c[1]

        if (x-200)**2 + (y-185)**2 <= (40)**2:
            list_of_all_obstacles.append((x,y))
        if y <= 0.31*x and x>=36 and x<=115 and y >= 0.35*x:
            list_of_all_obstacles.append((x,y))
        if y <= -1.8*x and x>=36 and x<=105 and y >= -1.16*x:
            list_of_all_obstacles.append((x,y))
        if x >= 165 and x <= 235:
           if y >= -0.71*x and y >= 0.71*x and y <= 0.71*x + 20 and y <= -0.71*x + 20:
               list_of_all_obstacles.append((x,y))


    if goal in list_of_all_obstacles:
        exit()

    base_graph = {}
    for i in range(400, -1, -1):
        for j in range(250, -1, -1):
            graph = generateGraph(i,j)
            base_graph[(i,j)]=graph[(i,j)]

    for key,value in base_graph.items():
        value_copy = value.copy()
        for coordinates in value_copy:
            if coordinates in list_of_all_obstacles:
                value.remove(coordinates)
    base_graph_copy=base_graph.copy()
    for key,value in base_graph_copy.items():
        if key in list_of_all_obstacles:
            del base_graph[key]

    actual_graph = cost_calculation(base_graph)

    shortest_path, visited, backtracking = dijkstra(actual_graph,start)

    all_distance_copy = shortest_path.copy()
    for k,v in all_distance_copy.items():
        if all_distance_copy[k] == math.inf:
            del shortest_path[k]

    return shortest_path, visited, backtracking


x_start = int(input("enter the x coordinate of the origin:  "))
y_start = int(input("enter the y coordinate of the origin:  "))
x_goal = int(input("enter the x coordinate of the goal:  "))
y_goal = int(input("enter the y coordinate of the goal:  "))


start = (x_start,y_start)
goal = (x_goal,y_goal)

maze = []
for i in range(0,401):
    for j in range(251):
        maze.append((i, j))

all_distance, visited, backtrack = robot(400, 250, start, goal)


backtracked_final = back_track(start,goal)


new_canvas = np.zeros((401,251,3),np.uint8)

for c in backtracked_final:
    x = c[1]
    y = c[0]
    new_canvas[(x,y)]=[0,255,255]

new_canvas = np.flipud(new_canvas)

new_canvas_copy_backtrack = new_canvas.copy()

new_canvas_copy_visited = new_canvas.copy()
new_canvas_copy_visited = cv2.resize(new_canvas_copy_visited,(600,400))
cv2.imshow('new_canvas',new_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()



pygame.init()

display_width = 400
display_height = 250

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)

black = (0,0,0)
white = (0,255,255)

surf = pygame.surfarray.make_surface(new_canvas_copy_visited)

clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    gameDisplay.fill(black)
    for path in visited:
        if path not in new_canvas_copy_visited:

            x = path[0]
            y = abs(250-path[1])

            pygame.draw.rect(gameDisplay, white, [x,y,1,1])

            pygame.display.flip()
    for path in backtracked_final:

        pygame.time.wait(5)

        x = path[0]
        y = abs(250-path[1])

        pygame.draw.rect(gameDisplay, (0,0,255), [x,y,1,1])

        pygame.display.flip()

    done = True
pygame.quit()


