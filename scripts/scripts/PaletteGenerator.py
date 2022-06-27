import image
from ByteComponent import ByteComponent
import matplotlib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

class PaletteGenerator:

    bytes = []

    ##Color IDs from Components
    colors = []

    ##RGB Colors where the index corresponds to the ID in colors
    colorsRGB = []

    ##key is the colorID, value is the count
    colorCounts = {}

    ##kmeans centers
    centers=[]
    centersHex=[]

    ##key is the colorID, value is a tuple of (closest color ID, diffR, diffG, diffB)
    colorDirects = {}

    def __init__(self, bytesArray):
        self.bytes = bytesArray

    def parsePalette(self):
        ####GET DEFAULT COLOR PALETTE FROM A COMPONENT
        for byte in self.bytes:
            self.colorCounts[byte.color] = self.colorCounts.get(byte.color, 0) + 1
        self.colors = [*self.colorCounts]
        print(self.colorCounts)

    def decodeGradient(self,hexColorArray, numCols):
        rgbColorArray = []
        #### map all hex colors to RGB
        for hexcolor in hexColorArray:
            rgb = matplotlib.colors.to_rgb(hexcolor)
            self.colorsRGB.append(rgb)
        print(self.colorsRGB)
        
        kmeans = KMeans(n_clusters=numCols, random_state=0).fit(self.colorsRGB)
        print(kmeans.cluster_centers_)
        print (kmeans.labels_)

        self.centers = kmeans.cluster_centers_
        for c in self.centers:
            self.centersHex.append(matplotlib.colors.to_hex(c))




        labels = kmeans.labels_

        for i in range (0, len(self.colorsRGB)):
            clusterIndex = labels[i]
            clusterRGB = self.centers[clusterIndex]
            currRGB = self.colorsRGB[i]
            diffR = (clusterRGB[0] - currRGB[0])/clusterRGB[0]
            diffG = (clusterRGB[1] - currRGB[1])/clusterRGB[1]
            diffB = (clusterRGB[2] - currRGB[2])/clusterRGB[2]

            self.colorDirects[self.colors[i]] = (clusterIndex,[diffR, diffG, diffB])
        print(self.colorDirects)

    def generateNewPalette(self, hexColorArray):
        if len(hexColorArray) != len(self.centers):
            print("Please only choose "+ len(self.centers) + " colors.")
            return
        else:
            newRGB = []
            for hexcolor in hexColorArray:
                rgb = matplotlib.colors.to_rgb(hexcolor)
                newRGB.append(rgb)

            generatedRGB = []
            for key in self.colorDirects:
                print(key)
                val = self.colorDirects.get(key)
                currRGB = newRGB[val[0]]
                direct = val[1]
                newR = currRGB[0] * (1-direct[0])
                if newR > 1:
                    newR = 1
                elif newR < 0:
                    newR = 0
                newG = currRGB[1] * (1-direct[1])
                if newG > 1:
                    newG = 1
                elif newG < 0:
                    newG = 0
                newB = currRGB[2] * (1-direct[2])
                if newB > 1:
                    newB = 1
                elif newB < 0:
                    newB = 0
                generatedRGB.insert(key,[newR, newG, newB])
            print(generatedRGB)

            generatedHex = []
            for rgbColor in generatedRGB:
                generatedHex.append(matplotlib.colors.to_hex(rgbColor))    
            print(generatedHex)
            print(self.centersHex)
            return generatedHex
        




    #     ##### get the most numCols most common colors
    #     sordtedCols = {k: v for k, v in sorted(colorCounts.items(), key=lambda item: item[1])}
    #     keys = sortedCols.keys()
    #     for i in range(0, numCols):
    #         topColors[i] = keys[i]

    #     #### for all of the rest, we will map the color index to the closest color and the difference in R, G, B from their closest color
    #     for i in range(numCols, len(keys)):
    #         closestColor = topColors[0]
    #         closestDist = 

    #         ##Calculate the closest color and create a colorDirects 
    #         for color in topColors:
    #             dist = calcDistance(rgbColorArray[keys[i]], rgbColorArray[color])
    #             if dist < closestDist:
    #                 closestDist = dist
    #                 closestColor = keys[i]