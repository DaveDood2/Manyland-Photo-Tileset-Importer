'''
Using PIL for Python image manipulation referenced from: https://stackoverflow.com/questions/138250/how-to-read-the-rgb-value-of-a-given-pixel-in-python
Code by: Dave Dood
'''

import sys
from PIL import Image
import math
import os # for isFile


def doExtractPixels(INPUT_FILE, roomName = ""):
    periodIndex = INPUT_FILE.index(".")
    if (periodIndex == -1):
        print("\tInvalid filename.")
        return
    OUTPUT_FILE = INPUT_FILE[0:periodIndex]
    print("\tOutputting to:", OUTPUT_FILE, ", Roomname: ", roomName)
    toOutput = "var imgData = [\n"
    im = Image.open(INPUT_FILE) # Can be many different formats.
    pix = im.load()
    isTransparent = False
    if (len(pix[0,0]) == 4):
        isTransparent = True
    print("\tTransparent?:", isTransparent)
    dimensions = im.size  # Get the width and hight of the image for iterating over
    width, height = dimensions[0], dimensions[1]
    cellWidth = 19 # Assuming cell width is same as cell height
    cellsNeeded = math.ceil(width / cellWidth) * math.ceil(height / cellWidth)
    print("\tRequired cells: {} to fit a {} x {} tileset.".format(cellsNeeded, width, height))
    for i in range(0, width):
        if (i == 0):
            toOutput += "\t["
        else:
            toOutput += ",\t["
        for j in range(0, height):
            if (j == 0):
                #print("Outputting:", pix[i,j])
                if (isTransparent):
                    toOutput += "\"{}:{}:{}:{}\"".format(pix[i,j][0], pix[i,j][1], pix[i,j][2], pix[i,j][3])
                else:
                    toOutput += "\"{}:{}:{}:{}\"".format(pix[i,j][0], pix[i,j][1], pix[i,j][2], 1)
            else:
                if (isTransparent):
                    toOutput += ",\"{}:{}:{}:{}\"".format(pix[i,j][0], pix[i,j][1], pix[i,j][2], pix[i,j][3])
                else:
                    toOutput += ",\"{}:{}:{}:{}\"".format(pix[i,j][0], pix[i,j][1], pix[i,j][2], 1)
        toOutput += "]\n"
    toOutput += "]\n"
    
    if (roomName == ""):
        changerCode = toChanger(toOutput)
        f = open("ROOMOutput\\TILE" + OUTPUT_FILE + ".js", "w")
    else:
        changerCode = toChanger(toOutput, roomName)
        f = open("ROOMOutput\\TILE" + roomName + ".js", "w")
    f.write(changerCode)
    f.close()
    print("\tFinished writing:", OUTPUT_FILE)
    return





def toChanger(pixelString, roomName = "defaultRoom"):
    strippedName = os.path.splitext(roomName)[0]
    changerCode = r"""/* Code is based on Death's PhotoDouble Changer.
All other changes made by me, Dave Dood.
*/

function change(creation) {
    return draw(creation);
}

function draw(creation){
    convertToFullColor(creation);
    creation.infoText = "the following is an imported white board drawing made by Dave dood!\n\nThe code used to import is based off of Death's photo changer.\n\nDill wanted to be in the credits so there they is!!"

    var cells = creation.cells;
    var width = cells[0].length;
    var height = cells[0][0].length;
    var x, y;
    var name = creation.name;
    var offsetX = 0;
    var offsetY = 0;
    if (name.includes("[") && name.includes("]")){
        //Find offset in name of the input dynamic
        //Get substring between two strings: stackoverflow.com/questions/14867835/get-substring-between-two-characters-using-javascript
        offsetX = name.substring(
            name.indexOf("[") + 1, 
            name.lastIndexOf(",")
        );
        offsetY = name.substring(
            name.indexOf(",") + 1,
            name.lastIndexOf("]")
        );
        console.log("offsetX:", offsetX, " offsetY:", offsetY);
        creation.name = " """ + strippedName + r""" " + "[" + offsetX + "," + offsetY + "]" ;
        offsetX = parseInt(offsetX) * 19 //Offset multiplied by 19 to account for the width/height of a block!
        offsetY = parseInt(offsetY) * 19
    }

    if (creation.type == enumType.changer){
        offsetX = 0;
        offsetY = 0;
    }
    
    /*if ((cells.length != 1) && (creation.type != enumType.changer)){
        creation.feedback = "Requires a 19x19 block.";
        return creation;
    }*/
    
    var n = creation.info.selectedCell
    
        var celly = 0;
        var cellx = 0;
        console.log(`Editing cell:${cellx}, ${celly}...`)
        for (var x = 0; x < width; x++) {
            for (var y = 0; y < height; y++) {
                cells[n][y][x] = colour(x, y, cellx, celly);
            }
        }   
    
    return creation;
        
        function colour(x, y, cellx, celly){
            var colourtext = getdata(x + cellx * 19, y + celly * 19);
            //var result = /^#?([a-f\\d]{2})([a-f\\d]{2})([a-f\\d]{2})$/i.exec(colourtext);
            let colorArray = colourtext.split(":")
            let result = {
                red: parseInt(colorArray[0], 10),
                green: parseInt(colorArray[1], 10),
                blue: parseInt(colorArray[2], 10),
                alpha: parseInt(colorArray[3], 10)
            }
            //console.log("result:", result)
            return result
        }
        
        function getdata(x, y){
            x = x + offsetY
            y = y + offsetX

            //pixelString goes here
            """ + pixelString + """

            if ((!imgData[y]) || (!imgData[y][x])){
                return "0:0:0:0";
            }
            return imgData[y][x];
        }
}"""
    return changerCode

def main(args):
    INPUT_FILE = "peasint.png"
    #OUTPUT_FILE = "output.txt"
    if len(args) >= 1:
        INPUT_FILE = args[0]
    '''if len(args) >= 2:
        OUTPUT_FILE = args[1]'''
    # Checking if file or directory: https://linuxize.com/post/python-check-if-file-exists/
    if os.path.isfile(INPUT_FILE):
        #Find last part of file path: https://stackoverflow.com/questions/3925096/how-to-get-only-the-last-part-of-a-path-in-python
        doExtractPixels(INPUT_FILE, os.path.basename(os.path.normpath(INPUT_FILE)))
    elif os.path.isdir(INPUT_FILE):
        # Iterating files in directory: https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
        print("List of files:", os.listdir(INPUT_FILE))
        for filename in os.listdir(INPUT_FILE):
            #if os.path.isfile(os.path.abspath(filename)):
                subInputFile = os.path.join(INPUT_FILE, filename)
                print("Running extract pixels on: ", subInputFile)
                doExtractPixels(subInputFile, filename)
            #else:
                #print("Skipping", filename, "...")

if __name__ == "__main__":
  main(sys.argv[1:])