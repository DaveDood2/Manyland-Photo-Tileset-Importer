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
    dimensions = im.size  # Get the width and hight of the image for iterating over
    width, height = dimensions[0], dimensions[1]
    cellWidth = 29 # Assuming cell width is same as cell height
    cellsNeeded = math.ceil(width / cellWidth) * math.ceil(height / cellWidth)
    print("\tRequired cells: {} to fit a {} x {} image.".format(cellsNeeded, width, height))
    for i in range(0, width):
        if (i == 0):
            toOutput += "\t["
        else:
            toOutput += ",\t["
        for j in range(0, height):
            if (j == 0):
                #print("Outputting:", pix[i,j])
                toOutput += "\"{}:{}:{}:{}\"".format(pix[i,j][0], pix[i,j][1], pix[i,j][2], pix[i,j][3])
            else:
                toOutput += ",\"{}:{}:{}:{}\"".format(pix[i,j][0], pix[i,j][1], pix[i,j][2], pix[i,j][3])
        toOutput += "]\n"
    toOutput += "]\n"
    
    if (roomName == ""):
        changerCode = toChanger(toOutput)
        f = open("ROOMOutput\\ROOM" + OUTPUT_FILE + ".js", "w")
    else:
        changerCode = toChanger(toOutput, roomName)
        f = open("ROOMOutput\\ROOM" + roomName + ".js", "w")
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
        offsetX = parseInt(offsetX) * 87 //Offset multiplied by 87 to account for the width/height of a 3x3 dynamic!
        offsetY = parseInt(offsetY) * 87
    }

    if (creation.type == enumType.changer){
        offsetX = 75;
        offsetY = 75;
    }
    
    if ((cells.length != 9) && (creation.type != enumType.changer)){
        creation.feedback = "Requires a 3x3 grid of cells.";
        return creation;
    }
    
    for(var n = 0; n < creation.cells.length; n++){
        var celly = n % 3;
        var cellx = Math.floor(n / 3);
        console.log(`Editing cell:${cellx}, ${celly}...`)
        for (var x = 0; x < width; x++) {
            for (var y = 0; y < height; y++) {
                cells[n][y][x] = colour(x, y, cellx, celly);
            }
        }   
    }
    return creation;
        
        function colour(x, y, cellx, celly){
            var colourtext = getdata(x + cellx * 29, y + celly * 29);
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