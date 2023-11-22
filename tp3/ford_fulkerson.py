import gzip
import time


class LinkedNode:
    def __init__(self,vtx):
        self.vtx = vtx
        self.next = None

class LinkedWeightedNode:
    def __init__(self, vtx, weight=0):
        self.vtx = vtx
        self.next = None
        self.weight = weight

class LinkedFlowNode:
    def __init__(self,vtx,capacity=0,flow=0,reverse_edge = None):
        self.vtx = vtx
        self.next = None
        self.capacity = capacity
        self.flow = flow
        self.reverse_edge = reverse_edge


class ArvoreGeradora:
    def __init__(self,vtx,pai,nivel):
        self.vtx = vtx
        self.pai = pai
        self.nivel = nivel

class Graph:
    def __init__(self, arquivo_relativo ,implementacao=1, directed = False):

        #utilizar apenas with open se for abrir a rede de colaboracao
        with gzip.open(arquivo_relativo, 'rt') as f:
            lines = f.readlines()
            lines = [line.rstrip() for line in lines]
            num_vtx = int(lines[0])
            lines.pop(0)
            for i in range(len(lines)):
                new_edge = lines[i].split()
                new_edge[0] = int(new_edge[0])
                new_edge[1] = int(new_edge[1])
                if(len(new_edge) == 3): #grafo com pesos
                    self.comPeso = True
                    new_edge[2] = float(new_edge[2])
                else:
                    self.comPeso = False
                lines[i] = new_edge

            self.num_vtx = num_vtx
            self.edges = lines
            self.directed = directed

        if(self.comPeso == False):

            self.implementacao = implementacao
            if self.implementacao == 2:
                self.graph_matrix = self.matriz_adjacencia()
            if self.implementacao == 1:
                self.graph_list = self.lista_adjacencia()
            self.graus = self.calcula_graus()
            self.componentes = self.contar_componentes()
            with open('info_grafo.txt', 'w') as f:
                f.write(f'Numero de vertices: {self.num_vtx}// Numero de arestas: {len(self.edges)}// gmin: {self.gmin()}// gmax:{self.gmax()}// N Componentes: {len(self.componentes[0])} // Maior: {max(self.componentes[1])} // Menor: {min(self.componentes[1])}')

        else:

            self.implementacao = 1
            self.graph_list = self.lista_adjacencia()
            print(f'Vertices: {self.num_vtx}, arestas: {len(self.edges)}')
            
    def matriz_adjacencia(self):
        colunas = self.num_vtx
        linhas = self.num_vtx
        matrix = []
        for i in range(linhas):
            linha = []
            for j in range(colunas):
                linha.append(0)
            matrix.append(linha)
        for edge in self.edges:
            linha = edge[0]
            coluna = edge[1]
            matrix[linha-1][coluna-1] = 1 # arestas começam no índice um
            matrix[coluna-1][linha-1] = 1 # matriz é simétrica
        return matrix

    def lista_adjacencia(self):

        if(self.comPeso == False):
            list = [None] * self.num_vtx
            for i in range(self.num_vtx):
                list[i] = LinkedNode(i+1)
            for edge in self.edges:
                vtx1 = edge[0]
                vtx2 = edge[1]
                
                node = list[vtx1-1]
                while node.next != None:
                    node = node.next
                node.next = LinkedNode(vtx2)

                node = list[vtx2-1]
                while node.next != None:
                    node = node.next
                node.next = LinkedNode(vtx1)
        else:
            if(self.directed == False):
                list = [None] * self.num_vtx
                for i in range(self.num_vtx):
                    list[i] = LinkedWeightedNode(i+1)
                for edge in self.edges:
                    vtx1 = edge[0]
                    vtx2 = edge[1]
                    weight = edge[2]

                    node = list[vtx1-1]
                    while node.next != None:
                        node = node.next
                    node.next = LinkedWeightedNode(vtx2,weight)

                    node = list[vtx2-1]
                    while node.next != None:
                        node = node.next
                    node.next = LinkedWeightedNode(vtx1,weight)
            else:
                list = [None] * self.num_vtx
                for i in range(self.num_vtx):
                    list[i] = LinkedFlowNode(i+1)
                for edge in self.edges:
                    vtx1 = edge[0]
                    vtx2 = edge[1]
                    capacity = edge[2]

                    node = list[vtx1-1]
                    while node.next != None:
                        node = node.next
                    node.next = LinkedFlowNode(vtx2,capacity)

        return list

    def addEdge(self,u,v,capacity,flow=0,reverse_edge=None):
        node = self.graph_list[u-1]
        while node.next != None:
            node = node.next
        node.next = LinkedFlowNode(v,capacity,flow,reverse_edge)
        return node.next

    def removeEdge(self,u,v):
        antecessor = self.graph_list[u-1]
        while antecessor.next.vtx != v:
            antecessor = antecessor.next
        edge = antecessor.next
        if edge.reverse_edge != None:
            edge.reverse_edge.reverse_edge = None
        antecessor.next = edge.next

    def BFS(self,vtx):
        marcado = [False] * self.num_vtx
        fila = []
        arvore_geradora = []
        pais = [None] * self.num_vtx
        niveis = [None] * self.num_vtx

        fila.append(vtx)
        marcado[vtx-1] = True 
        contador=0

        pais[vtx-1] = 0
        niveis[vtx-1] = 0

        while fila:
            vtx = fila.pop(0)
            contador +=1

            arvore_geradora.append(ArvoreGeradora(vtx,pais[vtx-1],niveis[vtx-1]))

            vizinhos_desmarcados = []
            if self.implementacao == 1:
                node = self.graph_list[vtx-1]
                while node.next != None:
                    node = node.next
                    if marcado[node.vtx - 1] == False:
                        vizinhos_desmarcados.append(node.vtx)
            if self.implementacao == 2:
                node = self.graph_matrix[vtx-1]
                for i in range(self.num_vtx):
                    if node[i] == 1:
                        if marcado[i] == False:
                            vizinhos_desmarcados.append(i+1)

            if len(vizinhos_desmarcados) > 0:
                
                vizinhos_desmarcados = sorted(vizinhos_desmarcados)
                for i in vizinhos_desmarcados:
                    fila.append(i)
                    marcado[i-1] = True
                    pais[i-1] = vtx
                    niveis[i-1] = niveis[vtx-1] + 1  
            
        with open('info_BFS.txt', 'w') as b:
            for k in arvore_geradora:
                b.write(f'Vertice: {k.vtx}, pai: {k.pai}, nivel:{k.nivel} //')
        return arvore_geradora, marcado, pais

   

    def calcula_distancia(self,vtx1,vtx2):
        BFS_vtx1 = self.BFS(vtx1)
        marcado = BFS_vtx1[1]
        if marcado[vtx2-1] == False:
            print('Nao existe caminho')
            return None
        else: 
          for i in BFS_vtx1[0] : #arvore_geradora
            if i.vtx == vtx2:
                print(f'A distancia e de {i.nivel} vertices')
                return i.nivel

    def get_caminho(self,fonte,destino):
        BFS_fonte = self.BFS(fonte)
        marcado = BFS_fonte[1]
        if marcado[destino-1] == False:
            return None
        else:
            pais = BFS_fonte[2]
            caminho = []
            while destino != fonte:
                caminho.append(destino)
                destino = pais[destino-1]
            caminho.append(fonte)
            caminho = list(reversed(caminho))
            return caminho


    def calcula_graus(self):
        if self.implementacao == 2:
            graus = []
            for linha in self.graph_matrix:
                soma = 0
                for i in range(self.num_vtx):
                    soma += linha[i]
                graus.append(soma)
            return graus
        if self.implementacao==1:
            graus = []
            for i in range(self.num_vtx):
                vizinhos = 0
                node = self.graph_list[i]
                while node.next != None:
                    node = node.next
                    vizinhos+=1
                graus.append(vizinhos)
            return graus
    
    
    def get_gargalo(self, aug_path):
        residual_capacities = []
        for i in range(len(aug_path)-1):
            u = aug_path[i]
            v = aug_path[i+1]
            edge1 = self.graph_list[u-1]
            while edge1.vtx != v:
                edge1 = edge1.next
            residual_capacity = edge1.capacity - edge1.flow
            residual_capacities.append(residual_capacity)
            if edge1.reverse_edge == None:
                if edge1.flow < 0: #aresta reversa -> original cheia
                    edge1.reverse_edge = self.addEdge(v,u,residual_capacity,residual_capacity,edge1)
                else:
                    edge1.reverse_edge = self.addEdge(v,u,0,0,edge1)
        gargalo = min(residual_capacities)
        return gargalo
        

    def ford_fulkerson(self, s=1, t=2):
        maxflow = 0
        G_f = self
        aug_path = G_f.get_caminho(s,t)
        while aug_path != None:
            gargalo = G_f.get_gargalo(aug_path)
            maxflow += gargalo
            for i in range(len(aug_path)-1):
                u = aug_path[i]
                v = aug_path[i+1]
                edge1 = G_f.graph_list[u-1]
                while edge1.vtx != v:
                    edge1 = edge1.next
                edge1.flow += gargalo
                edge1.reverse_edge.flow -= gargalo
                residual_capacity1 = edge1.capacity - edge1.flow
                residual_capacity2 = edge1.reverse_edge.capacity - edge1.reverse_edge.flow
                #remove aresta se diferença = 0
                if residual_capacity1 == 0:
                    G_f.removeEdge(u,v)
                if residual_capacity2 == 0:
                    G_f.removeEdge(v,u)
            aug_path = G_f.get_caminho(s,t)
        print(f'Maxflow: {maxflow}')
        return maxflow, G_f

    def flow_allocation(self, s=1, t=2):
        FF = self.ford_fulkerson(s,t)
        G_f = FF[1]
        for i in range(self.num_vtx):
            edge = G_f.graph_list[i]
            u = i+1
            while edge.next != None:
                v = edge.vtx
                residual_capacity = edge.capacity - edge.flow
                if edge.flow < 0:
                    if edge.reverse_edge == None:
                        edge.reverse_edge = G_f.addEdge(v,u,residual_capacity,residual_capacity,edge)
                    G_f.removeEdge(u,v)
                edge = edge.next
        with open('alocacao_fluxo.txt', 'w') as f:
            for i in range(self.num_vtx):
                edge = G_f.graph_list[i]
                u = i+1
                while edge.next != None:
                    v = edge.vtx
                    flow = edge.flow
                    capacity = edge.capacity
                    f.write(f'Aresta {u} - {v} , capacidade: {capacity} fluxo: {flow} \n')
                    edge = edge.next

def BFS_mil(G):
    inicio = time.time()
    for i in range(1000):
        i = i % G.num_vtx
        G.BFS(i)   
    fim = time.time()
    tempo_medio = (fim - inicio) / 1000
    print(f'Tempo de execução: {tempo_medio} ')
    return tempo_medio

def DFS_mil(G):
    inicio = time.time()
    for i in range(1000):
        i = i % G.num_vtx
        G.DFS(i)
    fim = time.time()
    tempo_medio = (fim - inicio) / 1000
    print(f'Tempo de execução: {tempo_medio} ')
    return tempo_medio

def dijkstra_100(G):
    inicio = time.time()
    for i in range(100):
        G.dijkstra(i)
    fim = time.time()
    tempo_medio = (fim - inicio) / 100
    print(f'Tempo de execução: {tempo_medio} ')
    return tempo_medio

def dijkstra_heap_100(G):
    inicio = time.time()
    for i in range(100):
        G.Dijkstra_heap(i)
    fim = time.time()
    tempo_medio = (fim - inicio) / 100
    print(f'Tempo medio de execução: {tempo_medio} ')
    return tempo_medio

def ford_fulkerson_10(G):
    inicio = time.time()
    for i in range(10):
        G.ford_fulkerson()
    fim = time.time()
    tempo_medio = (fim - inicio) / 10
    print(f'Tempo medio de exec: {tempo_medio} ')
    return tempo_medio

def ford_fulkerson_time(G):
    inicio = time.time()
    G.ford_fulkerson()
    fim = time.time()
    tempo = (fim - inicio)
    print(f'Tempo de execução: {tempo} ')
    return tempo

RF = Graph(r'ci/graph_files/graphs_tp3/grafo_rf_1.txt.gz',1,True)
RF.flow_allocation()
ford_fulkerson_time(RF)

