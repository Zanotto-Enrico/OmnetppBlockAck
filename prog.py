import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from math import *
import os
from functions import *

##-------------------------------------------------------------------------##
#
# prima studio il cambiamento usando pacchetti da 700B
#
# confronto quindi NoBA con BA utilizzando un thrashold 
# di attesa di frames di {4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64}
# in simulazioni di 6 secondi 
#
# confronto tutti i threshold nei 6 secondi in un grafico mostro
# in un histogramma le medie del loro throughput nei 6 secondi
#
# poi procedo e comincio a variare la frammentazione dei pacchetti
# e vedo quale configurazione ne rimette di più
#
##-------------------------------------------------------------------------##

SMOOTH_CONST = 5                                                    # smoothing constant
MAX = 37                                                            # lower bound for graphs
MIN = 7                                                            # higher bound for graphs
CSW_FOLDER = "./csv/"                                               # csv main folder location
GRAPHS_FOLDER = "./graphs/"                                         # graphs folder location
BA_THRESHOLDS = [4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64]     # All the BlockAck Thresholds tested
PKT_LENGTHS =[100,300,500,700,1000,1500,2000]                       # All the UDP segment size tested



plt.rcParams.update({'font.size': 22})
plt.xlabel('xlabel', fontsize=18)
plt.ylabel('ylabel', fontsize=16)


for pkt_length in PKT_LENGTHS:

    medieAck = []
    mediaNoAck = None
    allBaRuns = []
    noBA = pd.read_csv(CSW_FOLDER+str(pkt_length)+"B/noBlockAck.csv")

    ###############################

    graphsNoBA = parseVectors(noBA)

    smoothedNoBA = []
    for graph in graphsNoBA:
        smoothedNoBA.append(smoothGraph(graph,SMOOTH_CONST))

    avgNoBA = avgGraph(smoothedNoBA)

    ###############################

    for ba_threshold in BA_THRESHOLDS:

        yesBA = pd.read_csv("./csv/"+str(pkt_length)+"B/BlockAck" +str(ba_threshold)+".csv")
        GRAPHS_FOLDER = "./graphs/"+str(pkt_length)+"B/noBAvs"+str(ba_threshold)+"BA/"

        if not os.path.exists(GRAPHS_FOLDER):
            os.makedirs(GRAPHS_FOLDER)
        
        print("Comparing NoBA run with " + str(ba_threshold)+"BA run with packets len of " + str(pkt_length))


        ###########################################################################  GRAPHS WITHOUT BLOCK ACK

        fig , ax = plt.subplots(1,3, figsize=(28,6)) 
        ax[0].set_ylabel("Throughput (Mbps)")
        ax[1].set_xlabel("Time (Sec)")
        ax[0].xaxis.set_label_coords(0.5,-0.1)
        ax[0].yaxis.set_label_coords(-0.2,0.5)

        makePlot(ax[0],graphsNoBA,'Raw Data')                         # graph of all the runs without changes

        makePlot(ax[1],smoothedNoBA,'Smoothed')                       # graph of all the runs smoothed using
                                                                      # the SMOOTH_CONST constant
        makePlot(ax[2],[avgNoBA],'Average')                           # graph of a line rapresenting the average
        fig.savefig(GRAPHS_FOLDER + 'noBlockAck.png')                 # of all the runs
        plt.close(fig)

        ########################################################################### GRAPHS WITH BLOCK ACK

        graphsBA = parseVectors(yesBA)
        allBaRuns.append(graphsBA)

        fig , ax = plt.subplots(1,3, figsize=(28,6)) 
        ax[0].set_ylabel("Throughput (Mbps)")
        ax[1].set_xlabel("Time (Sec)")
        ax[0].xaxis.set_label_coords(0.5,-0.1)
        ax[0].yaxis.set_label_coords(-0.2,0.5)

        makePlot(ax[0],graphsBA,'RawData')                              # graph of all the runs without changes

        ###############################

        smoothedBA = []
        for graph in graphsBA:                                          # smoothing every graph
            smoothedBA.append(smoothGraph(graph,SMOOTH_CONST))

        makePlot(ax[1],smoothedBA,'Smoothed')                           # graph of all the runs smoothed using
                                                                        # the SMOOTH_CONST constant

        ###############################

        avgBA = avgGraph(smoothedBA)                                    # calculating the averages
        medieAck.append(avgBA)

        makePlot(ax[2],[avgBA],'Average')                               # graph of a line rapresenting the average
        fig.savefig(GRAPHS_FOLDER + 'BlockAck.png')                     # of all the runs
        plt.close(fig)

        ########################################################################### COMPARING BA RUNS WITH NoBA RUNS


        fig = plt.figure(figsize=(12, 6))
        plt.plot(avgBA[0] ,avgBA[1])
        plt.plot(avgNoBA[0] ,avgNoBA[1])
        plt.suptitle('Comparison', fontsize=24)                             # graph comparing the average of the runs
        plt.savefig(GRAPHS_FOLDER + 'Comparison.png')                              # with BlockAck to those without it 
        plt.close(fig)


    ############################################################################### COMPARO LE VARIE Block Ack RUNS


    fig , ax = plt.subplots(figsize=(12,6)) 
    makePlot(ax,medieAck,'Comparison of BA sessions')              # graph with the avereges of all the runs
    fig.savefig("./graphs/"+str(pkt_length)+"B/ComparisonAllAvg.png")       # by time based on the BA_THRESHOLDS
    plt.close(fig)                                                           


    ############################################################################### SCARTO I PRIMI 2 E L'ULTIMO VALORE

    for i in range(0,len(BA_THRESHOLDS)):
        medieAck[i][1] = medieAck[i][1][2:-1]
        medieAck[i][0] = medieAck[i][0][2:-1]

    ############################################################################### CREO IL GRAFICO A BARRE

    medieDelleMedie = []
    for g in medieAck:
        medieDelleMedie.append(sum(g[1])/len(g[1]))

    figure = plt.figure(figsize=(13, 6))                                # bar graph with the avereges of all the runs
    plt.suptitle('Comparison of BA sessions', fontsize=24)                     # based on the BA_THRESHOLDS
    plt.xticks(BA_THRESHOLDS)                                                  # added a line rappresenting the average of the
    colors = ['green', 'blue', 'purple',                                       # runs without BlockAck for comparison
              'brown', 'teal', 'pink', 
              'red', 'orange', 'green', 
              'grey','green', 'blue', 
              'purple', 'brown', 'teal']
    plt.bar(range(4,65,4),medieDelleMedie, color = colors,width=2)

    plt.plot(range(0,69,4) ,[sum(avgNoBA[1])/len(avgNoBA[1])]*18,color = 'black')


    plt.savefig("./graphs/"+str(pkt_length)+"B/barChart.png")
    plt.close(figure)

    ############################################################################### CONFIDENCE INTERVALS


    figure = plt.figure(figsize=(12, 12))
    plt.xticks(BA_THRESHOLDS)
    plt.title('Confidence Interval')
    for i in range(1,len(BA_THRESHOLDS)+1):
        sumOfAll = []                                                           # ToDo
        for n in allBaRuns[i-1]:
            sumOfAll = sumOfAll +n[1]
        plotConfidenceInterval(i*4, sumOfAll, z=1.96)
    plt.savefig("./graphs/"+str(pkt_length)+"B/confidence.png")
    plt.close(figure)




