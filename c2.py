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
    for i in range(0, len(ar)):
        temp=ar[i][:i]
        for j in range(0,len(temp)):
            if ar[i][j]==1:
                result.append([i,j])
    return result

def printAllHamCyc(g, v, visited, p, N):
    #jeśli wszsytkie wierzchołki zostaly odwiedzone to cykl istnieje
    if len(p) == N:
        #wrzuć cykl
        l.extend(p)
        return p
    #sprawdź czy każda krawedź zaczynając od v prowadzi do rozwiązania lub nie
    for w in g.adjList[v]:
        #sprawdź tylko nieodwiedzone wierzchołki, bo tak działa cykl hamiltona 
        if not visited[w]:
            visited[w] = True
            p.append(w)
            #sprawdź czy dodanie wierzchołka w do ścieżki doprowadza do rozwiązania
            printAllHamCyc(g, w, visited, p, N)
            #powrót
            visited[w] = False
            p.pop()

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
    if size==7:
        d=1.5
    elif size==8:
        d=3
    else:
        d=4
    for i in range(0, size):
        addEdge(i ,(i+1)%size)
    for n in range(0, int(requiredEdges/d)):
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

#wykresy + excel
elements=[]
test=[]
x=[]
for i in range(1, 20, 1):
    maxEdges=i*(i-1)/2
    if (maxEdges*0.5).is_integer():
        x.append(i)
print(x)
for i in range(0, len(x)):

    elements.append(x[i])

    matrix=[]
    makeGraph(x[i], 0.5)
    mtn=matrixToNumber(matrix)
    g=Graph(x[i], mtn)
    g.graphH = matrix
    for m in mtn:
        g.addEdge(m[0], m[1])
    #dodanie punktu startowego do ścieżki
    p = [0]
    #punkt startowy jako odwierdzony
    visited = [False] * x[i]
    visited[0] = True

    start=timer()
    l=[]
    printAllHamCyc(g, 0, visited, p, x[i])
    [l[n:n + x[i]] for n in range(0, len(l), x[i])]
    endtime=timer()-start
    test.append(endtime)
    print(x[i])
df = pd.DataFrame.from_dict(
    {
        'rozmiar zbioru'            :   elements, 
        'Hamilton'                  :   test, 
    }
)
df.to_excel('hm4.xlsx', header=True, index=False)