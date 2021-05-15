from    timeit          import default_timer as timer
from    graph           import Graph
import  random
import  sys
import  pandas as pd
import  xlsxwriter
sys.setrecursionlimit(1000000000)

def matrixToNumber(ar):
    #transfer macierzy sąsiadującej na incydencji 
    result=[]
    l=0
    z=0
    for i in range(0, len(ar)):
        temp=ar[i][:i]
        for j in range(0,len(temp)):
            z+=1
            if ar[i][j]==1:
                result.append([i,j])
                l+=1
    return result, l,z

def deconstructor():
    #do odpalania z pliku
    with open('euler.txt', 'r') as f:
        r=[]
        for line in f:
            line=line.replace('\n', '')
            line=line.split(' ')
            line = [ int(x) for x in line ]
            r.append(line)
        return matrixToNumber(r), len(r), r

######################################################################
#wywołanie przez plik
# temp=deconstructor()
# g=Graph(temp[1], temp[0])
# g.graphH = temp[2]
# for i in temp[0]:
#     g.addEdge(i[0], i[1])
# print('Cykl Eulera [', end='')
# result=g.printEulerTour()
# print(']\nCykl Hamiltona ', end='')
# g.hamCycle(); 
######################################################################

def addEdge(x,y):
    #wstaw krawędzie do macierzy sąsiadującej
    matrix[x][y]=1
    matrix[y][x]=1

def makeGraph(size, saturation):
    #zbuduj graf na podstawie rozmiaru i na nasycenia
    #nieskierowanie>nasycenie
    maxEdges=size*(size-1)/2
    requiredEdges=maxEdges*saturation
    for i in range(0, size):
        matrix.append([])
        for j in range(0, size):
            matrix[i].append(0)
    #brakujące krawędzie
    requiredEdges=requiredEdges-size
    for i in range(0, size):
        addEdge(i ,(i+1)%size)
    for n in range(0, int(requiredEdges/4)):
        while True:
            x1=random.randrange(0, size)
            x2=random.randrange(0, size)
            y1=random.randrange(0, size)
            y2=random.randrange(0, size)
            if x1==y1 or x2==y2:
                continue
            if x1==y2 or x2==y1:
                continue
            if x1==x2 or y1==y2:
                continue
            if (matrix[x1][y1] or matrix[x1][y2] or matrix[x2][y1] or matrix[x2][y2]):
                continue
            break
        addEdge(x1, y1)
        addEdge(x1, y2)
        addEdge(x2, y1)
        addEdge(x2, y2)

#do wykresów + excel
elements=[]
thirtyEuler=[]
seventyEuler=[]
thirtyHamilton=[]
seventyHamilton=[]
x=[]
for i in range(5, 100, 1):
    maxEdges=i*(i-1)/2
    if (maxEdges*0.3).is_integer() and (maxEdges*0.7).is_integer():
        x.append(i)

for i in range(0, len(x)):
    elements.append(x[i])

    matrix=[]
    makeGraph(x[i], 0.7)
    mtn=matrixToNumber(matrix)
    g=Graph(x[i], mtn[0])
    g.graphH = matrix
    for m in mtn[0]:
        g.addEdge(m[0], m[1])
    start=timer()
    result=g.printEulerTour()
    endtime=timer()-start
    seventyEuler.append(endtime)

    if len(matrix)>0:
        start=timer()
        g.hamCycle()
        endtime=timer()-start
        seventyHamilton.append(endtime)
    else:
        start=timer()
        endtime=timer()-start
        seventyHamilton.append(endtime)
        
    matrix=[]
    makeGraph(x[i], 0.3)
    mtn=matrixToNumber(matrix)

    g=Graph(x[i], mtn[0])
    g.graphH = matrix
    for m in mtn[0]:
        g.addEdge(m[0], m[1])

    start=timer()
    result=g.printEulerTour()
    endtime=timer()-start
    thirtyEuler.append(endtime)

    if len(matrix)>0:
        start=timer()
        g.hamCycle()
        endtime=timer()-start
        thirtyHamilton.append(endtime)
    else:
        start=timer()
        endtime=timer()-start
        thirtyHamilton.append(endtime)

df = pd.DataFrame.from_dict(
    {
        'rozmiar zbioru'     :   elements, 
        'SE'                 :   seventyEuler, 
        'TE'                 :   thirtyEuler, 
        'SH'                 :   seventyHamilton, 
        'TH'                 :   thirtyHamilton, 
    }
)
df.to_excel('euhm.xlsx', header=True, index=False)