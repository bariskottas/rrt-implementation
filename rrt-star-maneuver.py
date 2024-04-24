import tkinter as tk

from math import atan2
from math import cos
from math import degrees
from math import dist
from math import pi
from math import sin
from math import sqrt

from random import randint

class Node:
    x:int
    y:int
    cost:int
    
    isLower:bool
    heading:float

    id:int
    parent:int

    def __init__(self, x, y, id = 0, parent = -1):    
        self.x = x
        self.y = y
        self.cost = 0
        self.heading = 0

        self.id = id
        self.parent = parent
    
class Edge:
    node1:Node
    node2:Node

    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

class Shape:
    edges:list

    def __init__(self, edges):
        self.edges = edges

    def intersects(self, edge):
        return False
    
def drawCircle(canvas, x, y, color):
    a = canvas.create_oval(x - 4, y - 4, x + 4, y + 4, outline = color, fill = color, width = 0)
    canvas.pack()
    return a

def createMap(canvas, nodes, obstacles):
    #create starting node
    nodes.append(Node(50, 50, len(nodes)))

    drawCircle(canvas, 50, 50, "black")

    #create obstacles add to inObs
    snode1 = Node(500, 400)
    snode2 = Node(325, 550)
    snode3 = Node(675, 550)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode3)]))
    canvas.create_polygon([snode1.x, snode1.y, snode2.x, snode2.y, snode3.x, snode3.y], outline = "blue", fill = "blue", width = 0)

    snode1 = Node(150, 150)
    snode2 = Node(400, 150)
    snode3 = Node(150, 400)
    snode4 = Node(400, 400)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(150, 150, 150 + 250, 150 + 250, outline = "blue", fill = "blue", width = 0)

    snode1 = Node(600, 150)
    snode2 = Node(850, 150)
    snode3 = Node(600, 400)
    snode4 = Node(850, 400)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(600, 150, 600 + 250, 150 + 250, outline = "blue", fill = "blue", width = 0)

    snode1 = Node(150, 600)
    snode2 = Node(400, 600)
    snode3 = Node(150, 850)
    snode4 = Node(400, 850)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(150, 600, 150 + 250, 600 + 250, outline = "blue", fill = "blue", width = 0)

    snode1 = Node(600, 600)
    snode2 = Node(850, 600)
    snode3 = Node(600, 850)
    snode4 = Node(850, 850)
    obstacles.append(Shape([Edge(snode1, snode2), Edge(snode1, snode3), Edge(snode2, snode4), Edge(snode3, snode4)]))
    canvas.create_rectangle(600, 600, 600 + 250, 600 + 250, outline = "blue", fill = "blue", width = 0)

    #create goal
    canvas.create_rectangle(900, 900, 900 + 50, 900 + 50, outline = "green", fill = "green", width = 0)

    canvas.pack()

def inObs(node):
    if 150 <= node.x and node.x <= 400 and 150 <= node.y and node.y <= 400:
        return True
    
    if 600 <= node.x and node.x <= 850 and 150 <= node.y and node.y <= 400:
        return True

    if 150 <= node.x and node.x <= 400 and 600 <= node.y and node.y <= 850:
        return True

    if 600 <= node.x and node.x <= 850 and 600 <= node.y and node.y <= 850:
        return True

    return False

def inGoal(node):
    if 900 <= node.x and node.x <= 950 and 900 <= node.y and node.y <= 950:
        return True

    return False

def distance(node1, node2):
    return dist((node1.x, node1.y), (node2.x, node2.y))

def findClosestNode(nodes, node):
    closestDist = float('inf')
    closestNode = node

    for possibleNode in nodes:
        dist = distance(possibleNode, node)
        if dist <= closestDist:
            closestDist = dist
            closestNode = possibleNode

    if closestNode == node:
        return None

    return closestNode

def replaceWithCloserNode(node, closestNode):
    dist = distance(closestNode, node)

    if dist <= 50:
        return node
    
    ratio = 50 / dist

    return Node((1 - ratio) * closestNode.x + ratio * node.x, (1 - ratio) * closestNode.y + ratio * node.y, node.id)

def replaceWithProximalNode(node, closestNode, nodes):
    proximalNode = closestNode
    for possibleProximalNode in nodes:
        if possibleProximalNode.cost < proximalNode.cost and distance(possibleProximalNode, node) <= 150:
            proximalNode = possibleProximalNode
    
    return proximalNode

def thetaL(node1, node2):
    return atan2(node2.y - node1.y, node2.x - node1.x) - node1.heading

def rxy(node1, node2):
    tmp = abs(2 * sin(thetaL(node1, node2)))
    if tmp == 0:
        return float('inf')
    
    return distance(node1, node2) / tmp

def L(node1, node2):
    tL = thetaL(node1, node2)

    tmp = sin(tL)
    if tmp == 0:
        return float('inf') 

    return distance(node1, node2) * tL / tmp

def steer(node1, node2):
    if rxy(node1, node2) < 75:
        return False
    
    return True

def findCenter(node1, node2):
    r = rxy(node1, node2)
    d = distance(node1, node2)
    
    if thetaL(node1, node2) >= 0:
        midX = (node1.x + node2.x) / 2 - sqrt(r ** 2 - (d / 2) ** 2) * (node1.y - node2.y) / d 
        midY = (node1.y + node2.y) / 2 - sqrt(r ** 2 - (d / 2) ** 2) * (node2.x - node1.x) / d
    else:        
        midX = (node1.x + node2.x) / 2 + sqrt(r ** 2 - (d / 2) ** 2) * (node1.y - node2.y) / d 
        midY = (node1.y + node2.y) / 2 + sqrt(r ** 2 - (d / 2) ** 2) * (node2.x - node1.x) / d 

    return Node(midX, midY)

def drawArc(canvas, node1, node2, outline = "black", width = 1):
    t = 2 * thetaL(node1, node2)
    if abs(t) < 1e-4:
        canvasItem = canvas.create_line(node1.x, node1.y, node2.x, node2.y, fill = outline, width = width)
        canvas.pack()
        return canvasItem

    extent = degrees(t)
    if extent > 180:
        return drawArc(canvas, node2, node1, outline, width)

    center = findCenter(node1, node2)
    # print("x ", center.x)
    # print("y ", center.y)
    r = rxy(node1, node2)
    # print("r ", r)
    start = degrees(atan2(center.y - node2.y, center.x - node2.x)) 
    # print("s ", start)
    # print("e ", extent)

    canvasItem = canvas.create_arc(center.x - r, center.y - r, center.x + r, center.y + r, start = start, extent = -extent, outline = outline, width = width, style = tk.ARC)
    canvas.pack()
    return canvasItem

root = tk.Tk()

root.title("RRT* Implementation")

windowSize = 1000

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()

centerX = int(screenWidth / 2 - windowSize / 2)
centerY = int(screenHeight / 2 - windowSize / 2)

root.geometry(f'{windowSize}x{windowSize}+{centerX}+{centerY}')
root.resizable(False, False)

canvas = tk.Canvas(root, width = windowSize, height = windowSize)

nodes = []
obstacles = []

createMap(canvas, nodes, obstacles)

# drawCircle(canvas, 50, 50, "red")
# drawCircle(canvas, 50, 100, "red")
# drawCircle(canvas, 100, 50, "red")
# drawCircle(canvas, 100, 100, "red")

# drawArc(canvas, Node(50, 50), Node(100, 100))
# drawArc(canvas, Node(100, 50), Node(50, 100))

pathNotFound = True
while True:
    root.winfo_exists()
    root.update()

    if pathNotFound:
        node = Node(randint(0, windowSize), randint(0, windowSize), len(nodes))
        closestNode = findClosestNode(nodes, node)
        node = replaceWithCloserNode(node, closestNode)

        if inObs(node):
            continue

        closestNode = replaceWithProximalNode(node, closestNode, nodes)
        
        steerResult = steer(closestNode, node)
        if not steerResult:   
            continue

        node.cost = closestNode.cost + L(closestNode, node)

        center = findCenter(closestNode, node)

        tmp = atan2(node.y - center.y, node.x - center.x)
        if tmp > 0:
            node.heading = tmp + pi / 2
        else:
            node.heading = tmp - pi / 2
        
        if node.heading >= pi - 0.001:
            node.heading -= pi

        if node.heading <= -pi + 0.001:
            node.heading += pi
        
        node.parent = closestNode.id

        edge = Edge(closestNode, node)
        intersectionExists = False
        for obstacle in obstacles:
            if type(obstacle) == Shape and obstacle.intersects(edge):
                intersectionExists = True
                break

        if intersectionExists:
            continue

        nodes.append(node)

        drawCircle(canvas, node.x, node.y, "red")
        drawArc(canvas, closestNode, node)

        if inGoal(node):
            pathNotFound = False

            currentNode = node.id
            while currentNode != 0:        
                drawArc(canvas, nodes[nodes[currentNode].parent], nodes[currentNode], "darkgoldenrod1", 3)
                currentNode = nodes[currentNode].parent
