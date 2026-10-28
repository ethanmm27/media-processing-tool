import csv

baselightFile = open("Baselight_export_Fall2026.txt", "r")
baselightRead = baselightFile.read()
baselightFileList = baselightRead.splitlines()
baselightFile.close()

xytechFile = open("Xytech_Fall2026.txt", "r")
xytechFolderList = []
xytechRead = xytechFile.read()
xytechLines = xytechRead.splitlines()
for line in xytechLines:
    if "/" in line:
        xytechFolderList.append(line)
xytechFile.close()

columnOnePaths = []
for line in baselightFileList:
    folderSpaces = line.split(" ")
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
    columnOnePaths.append(path)

baselightRestStrings = []
for line in baselightFileList:
    cleaned = line.strip()
    folderSpaces = cleaned.split(" ")
    del folderSpaces[0]
    baselightRestStrings.append(folderSpaces)

columnFinalList = []

for i, string in enumerate(baselightRestStrings):
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

with open('Project_1.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Producer', 'Operator', 'Job', 'Notes'])
    writer.writerow(['Elizabeth Holmes', 'Tom Cruise', 'Dirtfixing', 'Please clean files noted per Colorist Jacob from Twilight'])
    writer.writerow([])
    writer.writerow(['Location', 'Frames to Fix'])
    for element in columnFinalList:
        rowToWrite = element.split(" ")
        writer.writerow(rowToWrite)