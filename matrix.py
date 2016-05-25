import json

j = json.loads(open('generated.json').read())

listAuthor = []
listFiles = []
listRow = []
listColumn = []

class Files:

    def __init__( self, name ):
        self.listAuthors = []
        self.name = name

    def setAuthor( self, myAuthor ):
        self.listAuthors.append(myAuthor)

class Authors:

    def __init__( self, name ):
        self.name = name
        self.counts = 0
        self.rate = 0.0

    def setCounts( self, counts ):
        self.counts = counts

    def setRate( self, rate ):
        self.rate = rate

def doesExist( myStr, myList ):
    if len(myList) == 0:
        return 0
    for z in range(0, len(myList)):
        if myStr == myList[z].name:
            return 1
    return 0

def authorCount( myStr ):
    count = 0
    for z in range(0, len(j)):
        if myStr == j[z]['author']:
            count = count + 1
    return count


def doesExistinAuthorList( myStr, myList ):
    if len(myList) == 0:
        return 0
    for z in range(0, len(myList)):
        if myStr == myList[z]:
            return 1
    return 0

def authorsWorkedOn( myStr ):
    array = []
    for i in range(0, len(j)):
        for k in range(0, len(j[i]['files'])):
            if myStr == j[i]['files'][k]:
                array.append(i)
                break
    return array

def sumCommits( myList ):
    totalSum = 0
    for z in range(0, len(myList)):
        totalSum = totalSum + myList[z].counts
    return totalSum

def commitRate( total, individual ):
    rate = (float(individual) / float(total)) * 100
    return rate

def checkAdjacency( ind1, ind2, rowLen):
    totalEdges=0
    for i in range(0,rowLen):
        if Matrix[i][ind1]==1 and Matrix[i][ind2]==1:
            totalEdges=totalEdges+1
    return totalEdges

#Filling listFiles (which keeps all file names)
print "Filling listFiles.."
for i in range(0, len(j)):
    for k in range(0, len(j[i]['files'])):
        if doesExist(j[i]['files'][k], listFiles) == 0: #Check if we already have such a file in file list.
            f = Files(j[i]['files'][k])
            listFiles.append(f)
#Filling listFiles.listAuthors (which authors have worked on the same file)
print "Filling listFiles.listAuthors.."
for i in range(0, len(listFiles)):
    index = []
    index = authorsWorkedOn(listFiles[i].name) #indexes of authours who worked on given file name
    for k in range(0, len(index)):
        if doesExistinAuthorList(j[index[k]]['author'], listFiles[i].listAuthors) == 0:
            listFiles[i].listAuthors.append(j[index[k]]['author'])

#Filling listAuthor (which keeps all author names)
print "Filling listAuthors.."            
for i in range(0, len(j)):
    if doesExist(j[i]['author'], listAuthor) == 0:
        f = Authors(j[i]['author'])
        listAuthor.append(f)
        f.setCounts(authorCount(j[i]['author']))

commits = sumCommits( listAuthor )
print "Setting listAuthor.rate.."
for i in range(0, len(listAuthor)):
    rates = commitRate(commits, listAuthor[i].counts)
    listAuthor[i].setRate(rates)

listAuthor.sort(key = lambda author: author.counts, reverse = True)


percentage2 = 0.0
listTop = []
for i in range(0, len(listAuthor)):
    if percentage2 >= 80.0:
        break
    else:
        percentage2 = percentage2 + listAuthor[i].rate
        listTop.append(listAuthor[i])

for i in range(0, len(listFiles)):
    listRow.append(listFiles[i].name)

for i in range(0, len(listAuthor)):
    listColumn.append(listAuthor[i].name)

r = len(listRow) # Files
c = len(listColumn) # Authors

#Filling a matrix with 0s.
global Matrix
Matrix = [[0 for x in range(c)] for y in range(r)]

#Filling the matrix with - if author worked on that file '1' else 0
for i in range(0, r):
    for k in range(0, c):
        for l in range(0, len(listFiles[i].listAuthors)):
            if listColumn[k] == listFiles[i].listAuthors[l]:
                Matrix[i][k] = 1

adjMatrix = [[0 for x in range(c)] for y in range(c)]
print "Forming lower triangular adjacency matrix.."
for i in range(0,c): #row
    for k in range(0,c): #col
        outStr=str(i)+','+str(k)
        print outStr
        if k==i:
            break
        EdgeThickness=checkAdjacency( i, k, r)
        if (EdgeThickness>0):
            adjMatrix[i][k]=adjMatrix[i][k]+EdgeThickness
print "Filling upper triangular part of the matrix using symmetry property.."
for i in range(0,c): #row
    for k in range(0,c): #col
        if k>i:
            adjMatrix[i][k]=adjMatrix[k][i]
        


print "Writing adjacency matrix to file.."
fo = open("socio-weighted2.txt", "wb")

for i in range(0, c):
    for k in range(0, c):
        fo.write(str(adjMatrix[i][k]))
        if(k == (c-1)):
            break
        fo.write(",")
    fo.write("\n")
fo.close()

print "Writing authors to file.."
fo = open("authorsAndIndexes2.txt", "wb")
for i in range(0,c):
    outStr=str(i)+" "+listColumn[i].encode("utf-8")+"\n"
    fo.write(outStr)
fo.close()

