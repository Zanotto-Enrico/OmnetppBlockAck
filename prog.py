import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from math import *



def smoothGraph(graph, w):
    newgraph = (graph[0][w:],[] )
    for i in range(w,len(graph[1])):
        newgraph[1].append(sum(graph[1][i-w:i])/w)
    return newgraph

    

def avgGraph(graphs):
    newgraph = (graphs[0][0],[])

    for i in range(0,len(newgraph[0])):
        sum = 0
        for graph in graphs:
            try:
                sum = sum + graph[1][i]
            except:
                sum = sum + 0
        newgraph[1].append(sum /len(graphs) )
    return newgraph



def parseVectors(csv):
    graphs = []

    for vector in csv["vecvalue"]:
        graph = ([],[])
        number = ""

        for value in vector:
            if value == " ":
                graph[1].append(float(number))
                number = ""
            else:
                number = number + value
        
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
        i= i+1
        graphs.append(graph)

    return graphs

def makePlot(figure, graphs, min, max, title):
    plot = figure.add_subplot()
    for graph in graphs:
        plot.plot(graph[0],graph[1])
    plot.set_ylim([min, max])
    plot.title.set_text(title)
    return 

##--------------------------------------------------------------##

SMOOTH_CONST = 5
MIN = 2000000
MAX = 4500000
FOLDER = "./noBAvs2BA"

medieAck = []
mediaNoAck = None

for i in range(1,11):

    noBA = pd.read_csv("./csv/noBlockAck.csv")
    yesBA = pd.read_csv("./csv/BlockAck" +str(i*2)+".csv")
    FOLDER = FOLDER = "./noBAvs"+str(i*2)+"BA/"

    plt.rcParams.update({'font.size': 22})
    plt.xlabel('xlabel', fontsize=18)
    plt.ylabel('ylabel', fontsize=16)
    print("Comparing NoBA run with " + str(i*2)+"BA run")


    ###############################

    graphs = parseVectors(noBA)

    fig = plt.figure(figsize=(12, 6)) 
    makePlot(fig,graphs,MIN,MAX,'Raw Data')
    fig.savefig(FOLDER + 'normalNoAck.png')
    plt.close(fig)

    ###############################

    smoothed = []
    for graph in graphs:
        smoothed.append(smoothGraph(graph,SMOOTH_CONST))

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,smoothed,MIN,MAX,'Smoothed')
    fig.savefig(FOLDER + 'smoothedNoAck.png')
    plt.close(fig)

    ###############################

    avgNoAck = avgGraph(smoothed)

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,[avgNoAck],MIN,MAX,'Average')
    fig.savefig(FOLDER + 'avgNoAck.png')
    plt.close(fig)

    ###########################################################################

    graphs = parseVectors(yesBA)

    fig = plt.figure(figsize=(12, 6)) 
    makePlot(fig,graphs,MIN,MAX,'Raw Data')
    fig.savefig(FOLDER + 'normalAck.png')
    plt.close(fig)

    ###############################

    smoothed = []
    for graph in graphs:
        smoothed.append(smoothGraph(graph,SMOOTH_CONST))


    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,smoothed,MIN,MAX,'Smoothed')
    fig.savefig(FOLDER + 'smoothedAck.png')
    plt.close(fig)

    ###############################

    avgAck = avgGraph(smoothed)
    medieAck.append(avgAck)

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,[avgAck],MIN,MAX,'Average')
    fig.savefig(FOLDER + 'avgAck.png')
    plt.close(fig)

    ###########################################################################


    fig = plt.figure(figsize=(12, 6))
    plt.plot(avgAck[0] ,avgAck[1])
    plt.plot(avgNoAck[0] ,avgNoAck[1])
    plt.ylim([MIN, MAX])
    plt.suptitle('Comparison', fontsize=24)
    plt.savefig(FOLDER + 'Comparison.png')    
    plt.close(fig)


###############################################################################


fig = plt.figure(figsize=(12, 6))
makePlot(fig,medieAck,MIN,MAX,'Comparison of BA sessions')
fig.savefig('ComparisonAllAvg.png')
plt.close(fig)


###############################################################################

medieDelleMedie = []
for g in medieAck:
    medieDelleMedie.append(sum(g[1])/len(g[1]))

figure = plt.figure(figsize=(12, 6))
plt.ylim([2500000, 4000000])
plt.suptitle('Comparison of BA sessions', fontsize=24)
plt.xticks([2,4,6,8,10,12,14,16,18,20])
colors = ['green', 'blue', 'purple', 'brown', 'teal', 'pink', 'red', 'orange', 'green', 'grey']
plt.bar(range(2,22,2),medieDelleMedie, color = colors)

plt.plot(range(0,24,2) ,[sum(avgNoAck[1])/len(avgNoAck[1])]*12,color = 'black')



plt.savefig('barChart.png')
plt.close(figure)



#
# prima studio il cambiamento usando pacchetti da 700B
#
# confronto quindi NoBA con BA utilizzando un thrashold 
# di attesa di frames di {2,4,6,8,10,12,16,18,20}
# in simulazioni di 6 secondi 
#
# confronto tutti i threshold nei 6 secondi in un grafico
# mostro in un histogramma le medie del loro throughput nei 6 secondi
#
# poi procedo e comincio a variare la dimensione dei frames
# e vedo quale configurazione ne rimette di più
#
# devo poi inventarmi qualcosa anche per la frammentazione


