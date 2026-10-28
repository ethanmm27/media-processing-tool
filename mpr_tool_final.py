import argparse
import csv
import sys

def readLines(fileName):
    with open(fileName, "r") as f:
        return f.read().splitlines()

def loadXytech(xytechFileName):
    xytechLines = readLines(xytechFileName)
    xytechFolderList = []
    header = {"Producer": "", "Operator": "", "Job": "", "Notes": ""}

    for i, line in enumerate(xytechLines):
        if "/" in line:
            xytechFolderList.append(line.strip())
        for key in header:
            if line.startswith(key + ":"):
                value = line.split(":", 1)[1].strip()
                if not value:
                    for nextLine in xytechLines[i + 1:]:
                        if nextLine.strip():
                            value = nextLine.strip()
                            break
                header[key] = value

    return header, xytechFolderList

def mapBaselightPaths(baselightFileList, xytechFolderList):
    columnOnePaths = []
    for line in baselightFileList:
        folderSpaces = line.strip().split(" ")
        folder = folderSpaces[0]
        thisFolder = folder.split("/")
        del thisFolder[0]
        del thisFolder[0]
        tempPath = "/".join(thisFolder)
        path = None
        for xytechLine in xytechFolderList:
            if tempPath in xytechLine:
                path = xytechLine
                break
            else:
                continue
        if path is None:
            print("Warning: no Xytech location found for " + folder, file=sys.stderr)
        columnOnePaths.append(path)
    return columnOnePaths

def getFrameStrings(baselightFileList):
    baselightRestStrings = []
    for line in baselightFileList:
        cleaned = line.strip()
        folderSpaces = cleaned.split(" ")
        del folderSpaces[0]
        baselightRestStrings.append(folderSpaces)
    return baselightRestStrings

def buildFrameRanges(baselightRestStrings, columnOnePaths):
    columnFinalList = []

    for i, string in enumerate(baselightRestStrings):
        if columnOnePaths[i] is None:
            continue

        firstNumber = None
        prevNumber = None
        for index, number in enumerate(string):
            int_number = int(number)
            if len(string) == 1:
                columnFinalList.append(columnOnePaths[i] + " " + str(int_number))
            if firstNumber is None:
                firstNumber = int_number
                continue
            if firstNumber is not None:
                if int_number == firstNumber + 1:
                    prevNumber = int_number
                    if index == len(string) - 1:
                        columnFinalList.append(columnOnePaths[i] + " " + str(firstNumber) + "-" + str(prevNumber))
                    continue
                if prevNumber is not None and int_number == prevNumber + 1:
                    prevNumber = int_number
                    if index == len(string) - 1:
                        columnFinalList.append(columnOnePaths[i] + " " + str(firstNumber) + "-" + str(prevNumber))
                    continue
                if prevNumber is not None:
                    columnFinalList.append(columnOnePaths[i] + " " + str(firstNumber) + "-" + str(prevNumber))
                else:
                    columnFinalList.append(columnOnePaths[i] + " " + str(firstNumber))
                firstNumber = None
                prevNumber = None
                if firstNumber is None:
                    firstNumber = int_number
                    if index == len(string) - 1:
                        columnFinalList.append(columnOnePaths[i] + " " + str(firstNumber))
                        firstNumber = None
                        prevNumber = None

    return columnFinalList

def writeCsv(outputFileName, header, columnFinalList):
    with open(outputFileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Producer', 'Operator', 'Job', 'Notes'])
        writer.writerow([header['Producer'], header['Operator'], header['Job'], header['Notes']])
        writer.writerow([])
        writer.writerow(['Location', 'Frames to Fix'])
        for element in columnFinalList:
            rowToWrite = element.split(" ")
            writer.writerow(rowToWrite)

def parseArgs():
    parser = argparse.ArgumentParser(
        description="Map a Baselight export to a Xytech work order and "
                    "write the frames to fix as a CSV."
    )
    parser.add_argument("baselight", nargs="?", default="Baselight_export_Fall2026.txt",
                        help="Baselight export file (default: %(default)s)")
    parser.add_argument("xytech", nargs="?", default="Xytech_Fall2026.txt",
                        help="Xytech work order file (default: %(default)s)")
    parser.add_argument("-o", "--output", default="MPR_Result.csv",
                        help="output CSV file (default: %(default)s)")
    return parser.parse_args()

def main():
    args = parseArgs()

    try:
        baselightFileList = [line for line in readLines(args.baselight) if line.strip()]
        header, xytechFolderList = loadXytech(args.xytech)
    except FileNotFoundError as e:
        sys.exit("Error: could not find file '" + e.filename + "'")

    columnOnePaths = mapBaselightPaths(baselightFileList, xytechFolderList)
    baselightRestStrings = getFrameStrings(baselightFileList)
    columnFinalList = buildFrameRanges(baselightRestStrings, columnOnePaths)

    writeCsv(args.output, header, columnFinalList)
    print("Wrote " + str(len(columnFinalList)) + " rows to " + args.output)

if __name__ == "__main__":
    main()
