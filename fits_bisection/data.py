import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from support import *
from random import choice
from sinusoid_fit import *

class dataPoint:
    def __init__(self,angle,pos_sum,neg_sum):
        self.angle = angle
        self.pos_sum = pos_sum
        self.neg_sum = neg_sum

        self.fit_val = 0

    def get_difference(self):
        return self.pos_sum - self.neg_sum

    def get_fit(self):
        return self.fit_val

    def set_fit_val(self,val):
        self.fit_val = val

    def __repr__(self):
        return "{}:{}".format(self.pos_sum,self.neg_sum)

class dataForGalaxy:
    def __init__(self,name,total_sum):
        self.name = name
        self.total_sum = total_sum
        self.dataPoints = []

        self.max_abs_differ = 0
        self.occurs_at_angle = 0

        self.fit_amp = 0
        self.fit_phase = 0

    def check_max_abs_difference(self,dataPoint):
        normalized_diff = dataPoint.get_difference()/self.total_sum
        each_data_point = dataPoint
        if abs(normalized_diff) > abs(self.max_abs_differ):
            self.max_abs_differ = normalized_diff
            self.occurs_at_angle = dataPoint.angle
            

    def getAbsoluteDifference(self,normalized = True):
        if normalized:
            return self.greatestAbsoluteDifference / self.total
        else:
            return self.greatestAbsoluteDifference

    def getDifference(self,normalized = True):
        if normalized:
            return self.greatestDifference / self.total
        else:
            #return self.greatestDifference
            return self.max_abs_differ

    def addDataPoint(self,angle,pos_sum,neg_sum):
        theDataPoint = dataPoint(angle,pos_sum,neg_sum)
        self.check_max_abs_difference(theDataPoint)
        self.dataPoints.append(theDataPoint)

    def getDifferenceSum(self):
        return list(map(lambda x: x.get_difference()/self.total_sum,list(sorted(self.dataPoints, key = lambda x: x.angle))))

    def getDifferenceRepr(self):
        return list(sorted(self.dataPoints, key = lambda x: x.angle))

    def getDifferenceAngles(self):
        return map(lambda x: x.angle, list(sorted(self.dataPoints, key = lambda x: x.angle)))

    def getDataRepr(self):
        toReturn = [self.name,self.total_sum]
        toReturn.extend(self.getDifferenceRepr())
        return list(map(lambda x: str(x), toReturn))

    def getDataHeadingRepr(self):
        toReturn = ["name","total_sum"]
        toReturn.extend(self.getDifferenceAngles())
        return list(map(lambda x: str(x), toReturn))

    def __getitem__(self,key): #for test
        for each_data_point in self.dataPoints:
            if each_data_point.angle == key:
                return each_data_point
            
    def plot(self,file_path="",angle=""):
        x = []
        y = []
        y1 = []
        for each_data_point in self.dataPoints:
            x.append(each_data_point.angle)
            
            #y.append((each_data_point.get_difference())/self.total_sum) #(flux_side_0 - flux_side_1)/ (total_flux) [originally had this]
            #y.append((each_data_point.pos_sum-each_data_point.neg_sum)/(each_data_point.pos_sum+each_data_point.neg_sum)) #(flux_side_0 - flux_side_1)/ (flux_side_0 + flux_side_1) [called new flux]
            y.append((each_data_point.get_difference())) #(flux_side_0 - flux_side_1) [differece in flux]
            #y.append((each_data_point.get_difference()))
            y1.append(each_data_point.get_fit())
        #file_path = ""
        plotIt(x,y,self.name,y1,"actual {}".format(angle),"fit: y = {}*cos(x - {})".format(self.fit_amp,np.degrees(self.fit_phase)),file_path)

    def fitIt(self):
        x = []
        y = []
        for each_data_point in self.dataPoints:
            x.append(each_data_point.angle)
            #y.append((each_data_point.pos_sum-each_data_point.neg_sum)/self.total_sum) #(flux_side_0 - flux_side_1)/ (total_flux) [originally had this]
            #y.append((each_data_point.pos_sum-each_data_point.neg_sum)/(each_data_point.pos_sum+each_data_point.neg_sum)) #(flux_side_0 - flux_side_1)/ (flux_side_0 + flux_side_1) [called new flux]
            y.append((each_data_point.get_difference())) #(flux_side_0 - flux_side_1) [differece in flux]
            #y.append((each_data_point.pos_sum-each_data_point.neg_sum))
        (amp, phase) = fit(x,y)

        self.fit_amp = amp
        self.fit_phase = phase

        for each_data_point in self.dataPoints:
            each_data_point.set_fit_val(my_cosin(np.radians(each_data_point.angle),amp,phase))

def plotMaxs(maxs):
    plt.hist(maxs, range=[-91, 91], bins = 182)
    plt.title("Eliptical Galaxies: Amplitude")
    #plt.xlabel("Max Difference/ Total")
    plt.xlabel("Angle")
    plt.ylabel("Number of Galaxies")
    plt.show()

def writeToFile(theStr,writeToFile):
    with open(writeToFile, 'a') as f:
        f.write(theStr)
        f.write("\n")

def writeInfo(dataForGalaxy,writeHeader=False,file_path=""):
    if writeHeader:
            toWrite = " ".join(dataForGalaxy.getDataHeadingRepr())
            writeToFile(toWrite,file_path)
    writeToFile(" ".join(dataForGalaxy.getDataRepr()),file_path)

def readData(path):
    allData = []
    angles = []
    isHeader = True
    j = 0
    with open(path, 'r') as f:
        for each_line in f.readlines():
            if isHeader:
                toParse = each_line.strip().split(" ")
                angles = list(map(lambda x: float(x),toParse[3:]))
                isHeader = False
            else:
                toParse = each_line.strip().split(" ")
                name = toParse[0]
                #print(name)
                total_sum = float(toParse[1])
                total_area = float(toParse[2])

                thisGal = dataForGalaxy(name,total_sum,total_area)
                for i in range(len(toParse[3:])):
                    thisParse = list(map(lambda x: float(x),toParse[3+i].strip().split(":")))

                    angle = angles[i]
                    pos_sum = thisParse[0]
                    neg_sum = thisParse[1]
                    pos_area = thisParse[2]
                    neg_area = thisParse[3]

                    thisGal.addDataPoint(angle,pos_sum,neg_sum,pos_area,neg_area)
                    
                allData.append(thisGal)
            j +=  1
            #eliptical_graph
            #5341
            if j > 100:
                break
    return allData

def noramlize_data_points(original,div):
    original_sum = original.total_sum
    div_sum = div.total_sum

    normalized = dataForGalaxy(original.name,original_sum/div_sum)
    for each_angle in original.getDifferenceAngles():
        o = original[each_angle]
        d = div[each_angle]

        op = o.pos_sum
        on = o.neg_sum
        dp = d.pos_sum
        dn = d.neg_sum
        normalized.addDataPoint(each_angle,op/dp,on/dn)

    return normalized
