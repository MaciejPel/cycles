from collections import defaultdict

class Graph:
    def __init__(self, vertices, edges):
        #ilość wierzchołków
        self.V= vertices
        #domyślny słownik do grafu (lista sąsiedztwa)
        self.graph = defaultdict(list)
        #macierz do hamiltona
        self.graphH = [
            [0 for column in range(vertices)]
            for row in range(vertices)
        ]
        #lista list reprezentująca listę sąsiedztwa
        self.adjList = [[] for _ in range(vertices)]
        #dodaj krawędzie do nieskierowanego grafu
        for (src, dest) in edges:
            self.adjList[src].append(dest)
            self.adjList[dest].append(src)

    def addEdge(self,u,v):
        #dodawanie krawędzi grafu
        self.graph[u].append(v)
        self.graph[v].append(u)
   
    def DFSUtil(self,v,visited):
        #oznacz aktualny punkt jako odwiedzony
        visited[v]= True
        #Sprawdź wszystkie wierzchołki sąsiadujące do tego
        for i in self.graph[v]:
            if visited[i]==False:
                self.DFSUtil(i,visited)
   
    def isConnected(self):
        #metoda sprawdzająca czy wszystkie wierzchołki o stopniu większym od zera są połączone
        #oznacz wszsytkie wierzchołki jako nieoznaczone
        visited =[False]*(self.V)
        #znajdź wierzchołek o stopniu większym od zera
        for i in range(self.V):
            if len(self.graph[i]) > 1:
                break
        #jeśli nie ma krawędzi w grafie zwróć prawda
        if i == self.V-1:
            return True
        #rozpocznij przejście DFS od wierzchołka z niezerowym stopniem
        self.DFSUtil(i,visited)
        #sprawdź czy wszsytkie niezerowe wierzchołki zostały odwiedzone
        for i in range(self.V):
            if visited[i]==False and len(self.graph[i]) > 0:
                return False
        return True
  
    def isEulerian(self):
        #sprawdź czy wszystkie niezrowe wierzchołki są połączone
        if self.isConnected() == False:
            return 0
        else:
            #zlicz wierzchołki o nieparzystym stopniu
            odd = 0
            for i in range(self.V):
                if len(self.graph[i]) % 2 !=0:
                    odd +=1
            #odd=2 cykl eulera
            if odd == 0:
                return 2
            elif odd == 2:
                return 1
            elif odd > 2:
                return 0
  
    def test(self):
        #warunek dla pustych macierzy
        if self.V>0:
            res = self.isEulerian()
            if res == 2:
                return True
        else:
            return True
    
    def isSafe(self, v, pos, path):
        #sprawdź czy ten wierzchołek jest sąsiednim wierzchołkiem poprzednio dodanego wierzchołka i nie jest zawarty w wczęsniejszym cyklu
        #sprawdź czy pierwszy i ostatni wierzchołek są połączone
        if self.graphH[ path[pos-1] ][v] == 0: 
            return False
        #sprawdź czy aktualny wierzchołek nie jest już w cyklu
        for vertex in path: 
            if vertex == v: 
                return False
        return True
  
    def hamCycleUtil(self, path, pos): 
        #przypadek podstawowy- jeśli wszsytkie wierzchołki są w ścieżce
        if pos == self.V: 
            #ostatni i pierwszy wierzchołek muszą w ścieżce by zrobić cykl
            if self.graphH[ path[pos-1] ][ path[0] ] == 1: 
                return True
            else: 
                return False
        #spróbuj innych wierzchołków jako potencjalnych kandydatów do cyklu. Poza wierzchołkiem zero.
        for v in range(0,self.V): 
            if self.isSafe(v, pos, path) == True: 
                path[pos] = v 
                if self.hamCycleUtil(path, pos+1) == True: 
                    return True
                #usuń aktualny wierzchołek jeśli nie prowadzi do rozwiązania
                path[pos] = -1
        return False
  
    def hamCycle(self): 
        #wierzchołek 0 jako pierwszy wierzchołek ścieżki. jeśli jest cykl hamiltona to ścieżka może zaczynać się od każdego punktu cyklu bo graf jest nieskierowany
        path = [-1] * self.V
        path[0] = 0
        if self.hamCycleUtil(path,1) == False: 
            print ("\Brak rozwiązania\n")
            return False
  
        # self.printSolution(path) 
        return True
        
    # def printSolution(self, path): 
    #     for vertex in path: 

            # print (vertex+1, end = " ")
        # print (path[0]+1)

    def printEulerUtil(self, u):
        #wypisz ścieżkę zaczynając od u
        #przejdź po wszystkich wierzchołkach sąsiadujących z tym wierzchołkiem
        for v in self.graph[u]:
            #jeśli krawędź u-v nie jest usunięta i jest ważna/właściwa 
            if self.isValidNextEdge(u, v):
                # print("%d=>%d, " %(u+1,v+1), end='')
                self.rmvEdge(u, v)
                # self.printEulerUtil(v)
  
    def printEulerTour(self):
        #znajdź wierzchołek o stopniu nieparzystym
        u = 0
        for i in range(self.V):
            if len(self.graph[i]) %2 != 0 :
                u = i
                break
        #wypisz cykl zaczynając od nieparzystego
        self.printEulerUtil(u)

    def rmvEdge(self, u, v):
        #usuwanie krawędzi u-v z grafu
        for index, key in enumerate(self.graph[u]):
            if key == v:
                self.graph[u].pop(index)
        for index, key in enumerate(self.graph[v]):
            if key == u:
                self.graph[v].pop(index)
  
    def DFSCount(self, v, visited):
        #funkcja bazowana na DFS do zliczania możliwych wierzchołków z punktu v
        count = 1
        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                count = count + self.DFSCount(i, visited)         
        return count
  
    def isValidNextEdge(self, u, v):
        #funkcja sprawdzająca, czy krawędź u-v można uznać za następną w cyklu

        #jeśli v jest jedynym sąsiadem wierzchołka u
        if len(self.graph[u]) == 1:
            return True
        else:
            #jeśli jest kilku sąsiadów- to u-v nie jest łącznikiem
            #zlicz możliwe wierzchołki z u
            visited =[False]*(self.V)
            count1 = self.DFSCount(u, visited)
            #usuń krawędź u-v a potem zlicz możliwe wierzchołki z u
            self.rmvEdge(u, v)
            visited =[False]*(self.V)
            count2 = self.DFSCount(u, visited)
            #Dodaj krawędź z powrotem do grafu
            self.addEdge(u,v)
            #jeśli licznik1 jest większy od drugiego to krawędx u-v jest łącznikiem
            return False if count1 > count2 else True