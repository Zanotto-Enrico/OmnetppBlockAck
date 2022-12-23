import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from math import *
import os
from functions import *

##---------------------------------------------------------------##
#
#   analizzo il guadagno in termini di output nell'utilizzo 
#   del Block Ack in funzione della dimensione del segmento
#
#   fisso il thrashold a 8,16,32,64 e testo il throughput con o senza
#   block ack di segmenti di dimensione  100B, 700B, 1000B, 2000B
#
##---------------------------------------------------------------##



plt.rcParams.update({'font.size': 22})
plt.xlabel('xlabel', fontsize=18)
plt.ylabel('ylabel', fontsize=16)

MIN = 100000
MAX = 4500000
RUNS = ["noBlockAck.csv","BlockAck4.csv",
        "BlockAck8.csv","BlockAck16.csv",
        "BlockAck32.csv","BlockAck64.csv"]
PKT_LENGTHS =[100,300,500,700,1000,1500,2000]                                    # All the UDP segment size tested
SMOOTH_CONST = 5

averages = []

for run in RUNS:
    average = []
    for pkt_lenght in PKT_LENGTHS:
        data = pd.read_csv("./csv/"+str(pkt_lenght)+"B/"+run)
        
        functions = parseVectors(data)

        smoothed = []
        for function in functions:
            smoothed.append(smoothGraph(function,SMOOTH_CONST))

        avg = avgGraph(smoothed)
        average.append(sum(avg[1])/len(avg[1]))

    averages.append(average)




figure = plt.figure(figsize=(12, 6))
plot = figure.add_subplot()

for average in averages:
    plot.plot(PKT_LENGTHS,average)
print(averages)
plot.title.set_text("Comparison BA runs vs Normal run")
figure.savefig("./ComparisonBAvsnoBA.png")
plt.close(figure)


