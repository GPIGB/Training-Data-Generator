import csv
import math
import random
import copy
from statistics import mean
from operator import add
import time

########

def randomNewPos():
    centre = [53.958365,-1.080271]
    radius = 0.00810135
    pos = [0,0]
    while ((math.pow(pos[0] - centre[0],2) + math.pow(pos[1] - centre[1],2)) > math.pow(radius,2)):
        pos = [random.uniform(53.9493635,53.9673665),random.uniform(-1.0892725,-1.0712695)]
    return pos

#

def distance(p1,p2):
    return(math.sqrt(math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2)))

#

def distributor_fuction(distances,totalToDistribute):
    final_distribution =  []
    ind_weights = []
    dists_total = 0

    for i in range(len(distances)):
        dists_total = dists_total + (1/math.exp(distances[i]))

    for i in range(len(distances)):
        ind_weights.append((1/math.exp(distances[i])/dists_total))
        final_distribution.append(totalToDistribute * ind_weights[i])
        
    return final_distribution

########

#list of location names/positions:

genLocationsDict = {"Parliament Street": [53.958901,-1.081244],
                    "Coney Street": [53.959327,-1.084198],
                    "Stonegate": [53.960815,-1.083520],
                    "Micklegate": [53.957305,-1.086630],
                    "Church Street": [53.959973,-1.081135],
                    "Parliament Street at M&S": [53.958372,-1.080276]}

####

#initializations:

start = time.time()

bin_count = 10
bin_positions = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
for i in range(bin_count):
            bin_positions[i] = randomNewPos()

with open('inputdata.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)[1::]

for i in range(len(data)):
    # data preprocessing
    if (data[i][2] == ''):
        data[i][2] = 0
    else:
        data[i][2] = int(data[i][2])

    day = copy.copy(data[i][0][0:2])
    month = copy.copy(data[i][0][3:5])
    year = copy.copy(data[i][0][6:10])
    data[i][0] = year + "/" + month + "/" + day + data[i][0][10::]

timesteps = list(dict.fromkeys([i[0] for i in data]))
timesteps.sort()

####

#primary loop:

with open('output.csv', 'w', newline='') as dataout:
    outwriter = csv.writer(dataout, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outwriter.writerow(["Bin ID", "Time", "Bin Position Y", "Bin Position X", "Received"])
    
    for t in timesteps:
        temp_gens = []
        gen_footfall_proportions = []
        gen_footfall_final_values = []
        bin_fills = [0] * bin_count
        
        for i in data:
            if i[0] == t: temp_gens.append(i)

        gens_total = sum([j[2] for j in temp_gens])
        avg_footfall = mean([j[2] for j in temp_gens]) #estimate the average footfall within city centre

        for i in range(len(temp_gens)):
            gen_footfall_proportions.append(temp_gens[i][2]/gens_total)
            gen_footfall_final_values.append(avg_footfall * gen_footfall_proportions[i])

        for i in range(bin_count):
            if (random.randint(0,99) < 5):
                bin_positions[i] = randomNewPos()

        for i in range(len(temp_gens)):
            #for each generating point
            bin_gen_distances = []
            
            for j in range(bin_count):
                #for each bin
                bin_gen_distances.append((distance(genLocationsDict[temp_gens[i][1]],bin_positions[j]))*200)

            bin_fills = list(map(add,distributor_fuction(bin_gen_distances,gen_footfall_final_values[i]),bin_fills))

        for k in range(bin_count):
            outwriter.writerow([k,t,bin_positions[k][0],bin_positions[k][1],(round(bin_fills[k]))])

end = time.time()

total_time = end - start

print("Complete. Time elapsed: " + str(total_time) + "s")
input("Press any key to continue...")
