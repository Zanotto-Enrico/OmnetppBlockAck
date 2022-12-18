import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from math import *
from functions import *

##---------------------------------------------------------------##
#
# prima studio il cambiamento usando pacchetti da 700B
#
# confronto quindi NoBA con BA utilizzando un thrashold 
# di attesa di frames di {2,4,6,8,10,12,16,18,20}
# in simulazioni di 6 secondi 
#
# confronto tutti i threshold nei 6 secondi in un grafico mostro
# in un histogramma le medie del loro throughput nei 6 secondi
#
# poi procedo e comincio a variare la dimensione dei frames
# e vedo quale configurazione ne rimette di più
#
# devo poi inventarmi qualcosa anche per la frammentazione
#
##---------------------------------------------------------------##

SMOOTH_CONST = 5
MIN = 2000000
MAX = 4500000
FOLDER = "./noBAvs2BA"

medieAck = []
mediaNoAck = None

plt.rcParams.update({'font.size': 22})
plt.xlabel('xlabel', fontsize=18)
plt.ylabel('ylabel', fontsize=16)

noBA = pd.read_csv("./csv/noBlockAck.csv")

###############################

graphsNoBA = parseVectors(noBA)

smoothedNoBA = []
for graph in graphsNoBA:
    smoothedNoBA.append(smoothGraph(graph,SMOOTH_CONST))

avgNoBA = avgGraph(smoothedNoBA)

###############################




for i in range(1,11):

    yesBA = pd.read_csv("./csv/BlockAck" +str(i*2)+".csv")
    FOLDER = FOLDER = "./noBAvs"+str(i*2)+"BA/"

    
    print("Comparing NoBA run with " + str(i*2)+"BA run")


    ###########################################################################

    fig = plt.figure(figsize=(12, 6)) 
    makePlot(fig,graphsNoBA,MIN,MAX,'Raw Data')
    fig.savefig(FOLDER + 'normalNoAck.png')
    plt.close(fig)

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,smoothedNoBA,MIN,MAX,'Smoothed')
    fig.savefig(FOLDER + 'smoothedNoAck.png')
    plt.close(fig)

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,[avgNoBA],MIN,MAX,'Average')
    fig.savefig(FOLDER + 'avgNoAck.png')
    plt.close(fig)

    ###########################################################################

    graphsBA = parseVectors(yesBA)

    fig = plt.figure(figsize=(12, 6)) 
    makePlot(fig,graphsBA,MIN,MAX,'Raw Data')
    fig.savefig(FOLDER + 'normalAck.png')
    plt.close(fig)

    ###############################

    smoothedBA = []
    for graph in graphsBA:
        smoothedBA.append(smoothGraph(graph,SMOOTH_CONST))

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,smoothedBA,MIN,MAX,'Smoothed')
    fig.savefig(FOLDER + 'smoothedAck.png')
    plt.close(fig)

    ###############################

    avgBA = avgGraph(smoothedBA)
    medieAck.append(avgBA)

    fig = plt.figure(figsize=(12, 6))
    makePlot(fig,[avgBA],MIN,MAX,'Average')
    fig.savefig(FOLDER + 'avgAck.png')
    plt.close(fig)

    ###########################################################################


    fig = plt.figure(figsize=(12, 6))
    plt.plot(avgBA[0] ,avgBA[1])
    plt.plot(avgNoBA[0] ,avgNoBA[1])
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

plt.plot(range(0,24,2) ,[sum(avgNoBA[1])/len(avgNoBA[1])]*12,color = 'black')


plt.savefig('barChart.png')
plt.close(figure)





