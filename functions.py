import statistics
from math import *
from matplotlib import pyplot as plt

def smoothGraph(graph, w):
    newgraph = (graph[0][w:],[] )
    for i in range(w,len(graph[1])):
        newgraph[1].append(sum(graph[1][i-w:i])/w)
    return newgraph

    

def avgGraph(graphs):
    newgraph = [graphs[0][0],[]]

    for i in range(0,len(newgraph[0])):
        sum = 0
        for graph in graphs:
            try:
                sum = sum + graph[1][i]
            except:
                sum = sum + 0
        newgraph[1].append(sum /len(graphs) )
    return newgraph



def parseVectors(csv,startPoint=0):
    graphs = []

    for vector in csv["vecvalue"]:
        graph = [[],[]]
        number = ""

        for value in vector:
            if value == " ":
                graph[1].append(float(number)/1000000)
                number = ""
            else:
                number = number + value
        graph[1] = graph[1][startPoint:]
        graphs.append(graph)

    i = 0
    for vector in csv["vectime"]:
        graph = graphs[i]
        number = ""

        for value in vector:
            if value == " ":
                graph[0].append(float(number))
                number = ""
            else:
                number = number + value
        graph[0] = graph[0][startPoint:]
        i= i+1

    return graphs

def makePlot(figure, graphs, min, max, title):
    plot = figure.add_subplot()
    for graph in graphs:
        plot.plot(graph[0],graph[1])
    plot.set_ylim([min, max])
    plot.title.set_text(title)
    return 

def plotConfidenceInterval(x, values, z=1.96, color='#2187bb', horizontal_line_width=0.25):
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    confidence_interval = z * stdev / sqrt(len(values))

    left = x - horizontal_line_width / 2
    top = mean - confidence_interval
    right = x + horizontal_line_width / 2
    bottom = mean + confidence_interval
    plt.plot([x, x], [top, bottom], color=color)
    plt.plot([left, right], [top, top], color=color)
    plt.plot([left, right], [bottom, bottom], color=color)
    plt.plot(x, mean, 'o', color='#f44336')

    return mean, confidence_interval