#txt file rotater
#rotate the text file counter clockwise

FILENAME = "maze11x11_2.txt"
mazeList=[]
mazeText=open("maze/original"+FILENAME)
for line in mazeText:
    rowList=[]
    for ch in line[:-1]:    #[:-1] all but the last char which is new line 
        rowList.append(ch)            
    mazeList.append(rowList)
mazeText.close()

rowMax = len(mazeList)
colMax = len(mazeList[0])
print("rowMax ")
print(rowMax)
print("colMax ")
print(colMax)

#rotation of original maze
rotatedMaze = list(reversed(list(zip(*mazeList))))

f = open("maze/r_"+FILENAME, "a")
for x in range(len(rotatedMaze[0])):
    for y in range(len(rotatedMaze)):
        f.write(rotatedMaze[x][y])
    f.write('\n')
f.close()
