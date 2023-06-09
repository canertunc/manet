import math
import sys
decraisingData = int(sys.argv[1])

def crnode(nodesDict,neighborhood,seperatedInstructions):
    nodesDict.update({seperatedInstructions[2] : [seperatedInstructions[3],seperatedInstructions[4],seperatedInstructions[5]]})
    neighborhood.update({seperatedInstructions[2]: []}) # First I just took nodes.
    print(f"         COMMAND *{seperatedInstructions[1]}*: New node {seperatedInstructions[2]} is created")

def createNeighborhood(nodesDict,neighborhood):
    for key,value in nodesDict.items():     
        coordinates = value[0].split(";")
        transfer = value[1].split(";")
        newTransfer = [[],[]]
        check = 0
        for i in range(4): # I returned 4 times because each node has 4 coordinates(east,west,nourth,south).
            if len(newTransfer[0]) == 2:
                if i == 2:
                    newTransfer[1].insert(1,int(coordinates[1]) + int(transfer[i]))
                else:
                    newTransfer[1].insert(0,int(coordinates[1]) - int(transfer[i]))
            else:
                if i == 0:
                    newTransfer[0].insert(1,int(coordinates[0]) + int(transfer[i]))
                else:
                    newTransfer[0].insert(0,int(coordinates[0]) - int(transfer[i]))
        for key2,value2 in nodesDict.items():
            if key2 != key:
                for mean in range(newTransfer[0][0],newTransfer[0][1]+1):
                    coordinates2 = value2[0].split(";")
                    if int(coordinates2[0]) == mean:
                        check +=1
                for mean in range(newTransfer[1][0],newTransfer[1][1]+1):
                    coordinates2 = value2[0].split(";")
                    if int(coordinates2[1]) == mean:
                        check +=1    
                if check == 2:
                    for user,neirg in neighborhood.items(): # In the code on the side, I added the neighbors according to the above calculations.
                        if key == user:
                            neirg.append(key2) 
                check = 0
            else:
                pass
    print("         NODES & THEIR NEIGHBORS:",end=" ")
    for key,value in neighborhood.items():
        if value == []:
            print(f"{key} -> ",end="| ")
        else:
            print(f"{key} ->",end=" ")
            for neigh in value:
                if value[-1] == neigh:
                    print(neigh,end=" | ")
                else:
                    print(neigh+",",end="")

def send(nodesDict,neighborhood,seperatedInstructions,remainingData):
    global packetNumber
    print(f"         COMMAND *{seperatedInstructions[1]}*: Data is ready to send from {seperatedInstructions[2]} to {seperatedInstructions[3]}\n         PACKET {packetNumber} HAS BEEN SENT")
    packetNumber += 1
    print(f"         REMAINING DATA SIZE: {remainingData} BYTE")
    createNeighborhood(nodesDict = nodesDict,neighborhood = neighborhood)

paths = []
def routePath(neighborhood,first,end): # I took "first" as a list when execute function in main function.
    for i in neighborhood[first[-1]]:  # because By adding neighbors to the path,I looked and added that neighbor's neighbors each time.
        if i == end:                   
            paths.append(first+[i])
        else:
            routePath(neighborhood,first+[i],end) 
    return paths

costs = []
def optimalRoute(nodesDict,paths):
    if paths != [] :
        for path in paths:
            cost = 0
            coordinates1 = []
            battery1 = []
            for node in path:
                for key,value in nodesDict.items():
                    if node != path[-1]:
                        if node == key:
                            seperated = value[0].split(";")
                            coordinates1.append(seperated[0])
                            coordinates1.append(seperated[1])
                        elif path[path.index(node)+1] == key:
                            battery1.append(nodesDict[key][2])
                    else:
                        if node == key:
                            seperated = value[0].split(";")
                            coordinates1.append(seperated[0])
                            coordinates1.append(seperated[1])
            for cord in range(int(len(coordinates1)/2)-1):
                cost +=  math.sqrt((float(coordinates1[2*cord]) - float(coordinates1[2*cord+2]))**2 + (float(coordinates1[2*cord+1]) - float(coordinates1[2*cord+3]))**2) / float(battery1[cord])
            costs.append(round(cost,4))

def optimalRoutePrint(nodesDict,remainingData,packetNumber,seperatedInstructions):
    print(f"\n         {len(paths)} ROUTE(S) FOUND:")
    for path in paths:
        str1 = ""
        for node in path:
            if node == path[-1]:
                str1 += node + " COST: " + str(costs[paths.index(path)])
            else:
                str1 += node+" -> "
        print(f"         ROUTE {paths.index(path)+1}: {str1}")
    
    if paths != []: # I checked the paths list to not print an empty list
        indexofOptimal = costs.index(min(costs))
        print(f"         SELECTED ROUTE (ROUTE {indexofOptimal+1}):",end=" ")
        for opt in paths[indexofOptimal]:
            if opt == paths[indexofOptimal][-1]:
                print(f"{opt}")
            else:
                print(f"{opt} ->",end=" ")
        if seperatedInstructions[1] != "CHBTTRY" and seperatedInstructions[1] != "RMNODE" : # I checked the equation on the side because we need to change the data and package
            for packet in range(len(nodesDict.keys())):                                     # according to the number of nodes in the commands other than these.
                remainingData -= decraisingData
                print(f"         PACKET {packetNumber} HAS BEEN SENT\n         REMAINING DATA SIZE: {remainingData} BYTE")
                packetNumber += 1
        else:
            print(f"         PACKET {packetNumber} HAS BEEN SENT\n         REMAINING DATA SIZE: {remainingData} BYTE")

def move(nodesDict,seperatedInstructions,packetNumber,remainingData):
    for key,value in nodesDict.items():
        if seperatedInstructions[2] == key:
            nodesDict[key][0] = seperatedInstructions[3]
            print(f"         COMMAND *{seperatedInstructions[1]}*: The location of node {seperatedInstructions[2]} is changed\n         PACKET {packetNumber} HAS BEEN SENT\n         REMAINING DATA SIZE: {remainingData} BYTE")

def chbttry(nodesDict,node,newBattery,packetNumber,remainingData):
    for key,value in nodesDict.items():
        if key == node:
            nodesDict[key][2] = newBattery
    print(f"         PACKET {packetNumber} HAS BEEN SENT\n         REMAINING DATA SIZE: {remainingData} BYTE")
    
def rmnode(nodesDict,seperatedInstructions,remainingData,packetNumber):
    print(f"         COMMAND *{seperatedInstructions[1]}*: Node {seperatedInstructions[2]} is removed")
    print(f"         PACKET {packetNumber} HAS BEEN SENT\n         REMAINING DATA SIZE: {remainingData} BYTE")
    nodesDict.pop(seperatedInstructions[2])

def intrude(nodesDict,neighborhood,seperatedInstructions,remainingData,packetNumber):
    pass # intrude not added!

packetNumber = 1 
def main():
    global paths
    global costs
    nodesDict = {}
    neighborhood = {}
    remainingData = float(0)
    global packetNumber
    with open("commands.txt","r") as file:
        instructions = file.readlines()
        print("""********************************
AD-HOC NETWORK SIMULATOR - BEGIN
********************************""")
        print(f"SIMULATION TIME: 00:00:00")
        for i in instructions:
            seperatedInstructions = i.strip("\n").split("\t")
            if seperatedInstructions[1] == "CRNODE":
                crnode(nodesDict,neighborhood,seperatedInstructions)
                neighborhood.update({seperatedInstructions[2] : []})
            
            elif seperatedInstructions[1] == "SEND":
                remainingData += int(seperatedInstructions[4])
                remainingData -= decraisingData
                send(nodesDict,neighborhood,seperatedInstructions,remainingData)
                first = seperatedInstructions[2]
                end = seperatedInstructions[3]
                routePath(neighborhood,[first],end)
                optimalRoute(nodesDict,paths)
                
                if paths != []: # I checked the paths list to print "no route found".
                    optimalRoutePrint(nodesDict,remainingData,packetNumber,seperatedInstructions)
                else:
                    print(f"\n         NO ROUTE FROM {first} TO {end} FOUND.")
                    break
                remainingData -= len(nodesDict.keys())*decraisingData # I had to use in here to permanently replace remainingData and packetNumber.
                packetNumber += len(nodesDict.keys())

            elif seperatedInstructions[1] == "MOVE":
                remainingData -= decraisingData
                move(nodesDict,seperatedInstructions,packetNumber,remainingData)
                packetNumber +=1
                for key in neighborhood.keys():
                    neighborhood[key] = []
                createNeighborhood(nodesDict,neighborhood)
                paths = [] # I emptied the lists to rewrite.
                costs = []
                routePath(neighborhood,[first],end)
                optimalRoute(nodesDict,paths)
                if paths != []:  
                    optimalRoutePrint(nodesDict,remainingData,packetNumber,seperatedInstructions)
                else:
                    print(f"\n         NO ROUTE FROM {first} TO {end} FOUND.")
                    break
                remainingData -= len(nodesDict.keys())*decraisingData 
                packetNumber += len(nodesDict.keys())

            elif seperatedInstructions[1] == "CHBTTRY":
                node = seperatedInstructions[2]
                newBattery = seperatedInstructions[3]
                remainingData -= decraisingData
                chbttry(nodesDict,node,newBattery,packetNumber,remainingData)
                packetNumber += 1
                for key in neighborhood.keys():
                    neighborhood[key] = []
                createNeighborhood(nodesDict,neighborhood)
                paths = []
                costs = []
                routePath(neighborhood,[first],end)
                optimalRoute(nodesDict,paths)
                remainingData -= decraisingData
                if paths != []:
                    optimalRoutePrint(nodesDict,remainingData,packetNumber,seperatedInstructions)
                else:
                    print(f"\n         NO ROUTE FROM {first} TO {end} FOUND.")
                    break
                packetNumber += 1

            elif seperatedInstructions[1] == "RMNODE":
                remainingData -= decraisingData
                rmnode(nodesDict,seperatedInstructions,remainingData,packetNumber)
                packetNumber += 1
                for key in neighborhood.keys():
                    neighborhood[key] = []
                neighborhood.pop(seperatedInstructions[2])
                createNeighborhood(nodesDict,neighborhood)
                paths = []
                costs = []
                routePath(neighborhood,[first],end)
                optimalRoute(nodesDict,paths)
                remainingData -= decraisingData
                if paths != []:
                    optimalRoutePrint(nodesDict,remainingData,packetNumber,seperatedInstructions)
                else:
                    print(f"\n         NO ROUTE FROM {first} TO {end} FOUND.")
                    break
                packetNumber += 1

            elif seperatedInstructions[1] == "INTRUDE":
                pass
    
        print("""******************************
AD-HOC NETWORK SIMULATOR - END
******************************""")
main()