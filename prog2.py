import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import gridspec
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
RUNS = ["noBlockAck.csv","BlockAck8.csv", "BlockAck64.csv"]
NAMES = ["No BlockAck","BlockAck 8", "BlockAck 64"]
PKT_LENGTHS =[100,300,500,700,1000,1500,2000]                                    # All the UDP segment size tested
NAMES2 =["100B","300B","500B","700B","1000B","1500B","2000B"] 
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


############################################################################

figure = plt.figure(figsize=(24, 12))
plot = figure.add_subplot()
plt.ylabel("Average Throughput (Mbps)")
plt.xlabel("UDP segment length (Byte)")
plot.xaxis.set_label_coords(0.5, -0.1)
plot.yaxis.set_label_coords(-0.05, 0.5)
plt.xticks(PKT_LENGTHS)     
plt.grid()

it = iter(NAMES)
for average in averages:
    plot.plot(PKT_LENGTHS,average,label=next(it),linewidth=4)
    
plt.legend(loc="upper left")
plot.title.set_text("Comparison BA runs vs Normal run")
figure.savefig("./ComparisonBAvsnoBA.png")
plt.close(figure)

############################################################################

gains = []
for i in range(0,len(PKT_LENGTHS)):
    gains.append(round(((averages[2][i]-averages[0][i])/averages[0][i])*100, 1))
    
spec = gridspec.GridSpec(ncols=1, nrows=1,hspace=0.4,wspace=0.1 )
spec.update(left=0.2)

figure = plt.figure(figsize=(12, 12))                 
plot = figure.add_subplot(spec[0])            

plt.suptitle('Block Ack gains per packet length', fontsize=24)                    
ind = np.arange(len(PKT_LENGTHS))                                      
colors = ['green', 'blue', 'purple',                                       
            'brown', 'teal', 'pink', 'red']
plt.grid()
plt.barh(ind,gains, color = colors)
plot.set_xticks([*range(0,180,20)], ["0%","20%","40%","60%","80%","100%","120%","140%","160%"])
plot.set_yticks(ind, NAMES2)
plot.set_axisbelow(True)

plt.ylabel("UDP segment length")
plt.xlabel("throughput gains ")
plot.xaxis.set_label_coords(0.5, -0.08)
plot.yaxis.set_label_coords(-0.18, 0.5)

figure.savefig("./BlockAckGains.png")
plt.close(figure)
print(gains)
