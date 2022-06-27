from copy import copy
from fileinput import filename
import image
from ByteComponent import ByteComponent
from PaletteGenerator import PaletteGenerator

byteComponents = []
colors = []
colorsRGB = []
bounds = [0,0,0,0] # TopY, RightX, BottomY, LeftX
redPixel = image.Pixel(255, 0, 0)

def parseImg(img):
    """ (Image object) -> Image object
    Returns a copy of img where the blue and green have been filtered
    out and only red remains.
    """
    myImg = img.copy() # create copy to manipulate
    for x in range(bounds[3],(bounds[1] - 20),20): # iterate through all (x, y) pixel pairs
        for y in range(bounds[0],(bounds[2] - 20),20):
            pixel = img.getPixel(x, y)
            red = pixel.getRed()
            green = pixel.getGreen()
            blue = pixel.getBlue()
            pixelRGB = [red, green, blue]
            finalRGB = colorGrouping(pixelRGB)
            color = '#%02x%02x%02x' % (finalRGB[0], finalRGB[1], finalRGB[2])
            if color not in colors:
                colors.append(color)
            newByte = ByteComponent(x, y, x+20, y+20)
            newByte.setColor(colors.index(color))
            newByte.setLength(1)
            byteComponents.append(newByte)
            newPixel = image.Pixel(finalRGB[0], finalRGB[1], finalRGB[2])
            for i in range(x, x+20):
                    for j in range(y, y + 20):
                        myImg.setPixel(i, j, newPixel)
    myImg.save("generatedImages/smooth")          

def colorGrouping(pixelRGB):
    pixelRed = pixelRGB[0]
    pixelGreen = pixelRGB[1]
    pixelBlue = pixelRGB[2]
    if len(colorsRGB) == 0:
        colorsRGB.append(pixelRGB)
        return pixelRGB
    
    for RGB in colorsRGB:
        if abs(pixelRed - RGB[0]) <= 10 and abs(pixelGreen - RGB[1]) <= 10 and abs(pixelBlue - RGB[2]) <= 10:
            return RGB
        
    colorsRGB.append(pixelRGB)
    return pixelRGB
        
def getBoundary(img, copyImg):
    bounds[0] = getTopY(img, copyImg)
    bounds[1] = getRightX(img, copyImg)
    bounds[2] = getBottomY(img, copyImg)
    bounds[3] = getLeftX(img, copyImg)

def getTopY(img, copyImg):
    w = img.getWidth()
    h = img.getHeight()
    for y in range(h):
        for x in range(w):
            pixel = img.getPixel(x, y)
            red = pixel.getRed()
            green = pixel.getGreen()
            blue = pixel.getBlue()
            color = '#%02x%02x%02x' % (red, green, blue)
            if color != '#000000':
                for i in range(x, x+20):
                    for j in range(y, y + 20):
                        copyImg.setPixel(i, j, redPixel)
                copyImg.save("generatedImages/withred")
                return y

def getLeftX(img, copyImg):
    w = img.getWidth()
    h = img.getHeight()
    for x in range(w):
        for y in range(h):
            pixel = img.getPixel(x, y)
            red = pixel.getRed()
            green = pixel.getGreen()
            blue = pixel.getBlue()
            color = '#%02x%02x%02x' % (red, green, blue)
            if color != '#000000':
                for i in range(x, x+20):
                    for j in range(y, y + 20):
                        copyImg.setPixel(i, j, redPixel)
                copyImg.save("generatedImages/withred")            
                return x

def getBottomY(img, copyImg):
    w = img.getWidth()
    h = img.getHeight()
    for y in range(h-1,0,-1):
        for x in range(w):
            pixel = img.getPixel(x, y)
            red = pixel.getRed()
            green = pixel.getGreen()
            blue = pixel.getBlue()
            color = '#%02x%02x%02x' % (red, green, blue)
            if color != '#000000':
                for i in range(x, x+20):
                    for j in range(y, y -20,-1):
                        copyImg.setPixel(i, j, redPixel)
                copyImg.save("generatedImages/withred")
                return y     

def getRightX(img, copyImg):
    w = img.getWidth()
    h = img.getHeight()
    for x in range(w-1,0,-1):
        for y in range(h):
            pixel = img.getPixel(x, y)
            red = pixel.getRed()
            green = pixel.getGreen()
            blue = pixel.getBlue()
            color = '#%02x%02x%02x' % (red, green, blue)
            if color != '#000000':
                for i in range(x, x-20, -1):
                    for j in range(y, y + 20):
                        copyImg.setPixel(i, j, redPixel)
                copyImg.save("generatedImages/withred")
                return x      

def buildBytes():
    componentsToBytes = bytearray()
    for component in byteComponents:
        componentsToBytes.append(component.length)
        componentsToBytes.append(component.color)
    return bytes(componentsToBytes)

def printBytes():
    for byte in byteComponents:
        byte.toString()

def bytesToSvg(bytes, palette, name):
    filename = str(name) + ".svg"
    svgFile = open(filename, "w")
    height = abs(bounds[0]-bounds[2])
    width = abs(bounds[3]-bounds[1])
    header = '<svg width="'+str(width)+'" height="'+str(height)+'" viewbox ="'+str(bounds[3])+' '+str(bounds[0])+' '+str(width)+' ' +str(height)+'" xmlns="http://www.w3.org/2000/svg" shape-rendering="crispEdges">'
    svgFile.write(header)
    for byte in bytes:
        svgFile.write(byte.toSVG(palette))
    svgFile.write('</svg>')



def main():
    """ () -> NoneType
    Main Program that load image(s) from file(s) and performs
    transformations to those images as required for HW 04. The images
    are then displayed.
    """
    fileName = input("enter image filename: ")
    myImg = image.FileImage(fileName)
    copyImg = myImg.copy()
    getBoundary(myImg, copyImg)
    parseImg(myImg)
    # printBytes()
    print("bounds: ", bounds)
    print("ammmount of rects: ", len(byteComponents))
    print("ammount of colorsHEX:", len(colors))
    print(buildBytes())

    paletteGen = PaletteGenerator(byteComponents)
    paletteGen.parsePalette()

    
    paletteGen.decodeGradient(colors, 1)
    generatedPalette = paletteGen.generateNewPalette(["#E60B9B"])
    bytesToSvg(byteComponents, generatedPalette, str(filename))

if __name__ == "__main__":
    main()