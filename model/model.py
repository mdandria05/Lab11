import networkx as nx
from networkx.classes import neighbors

from database.dao import DAO
from model.rifugio import Rifugio

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.rifugio_dict = {}
        self.connessioni_list = []

    def getRifugi(self):
        self.rifugio_list = DAO.getAllrifugi()
        for r in self.rifugio_list:
            self.rifugio_dict[r.id] = r

    def getConnessioni(self,year : int):
        self.connessioni_list = DAO.getAllconnessioni_for_year(year)

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        self.G.clear()
        self.getRifugi()
        self.getConnessioni(year)
        for c in self.connessioni_list:
            self.G.add_edge(self.rifugio_dict[c.id_rifugio1],self.rifugio_dict[c.id_rifugio2])
        return self.G


    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        result = []
        for r in self.G.nodes():
            result.append(r)
        result.sort(key=lambda x: x.id)
        return result

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        neighbors = self.G.neighbors(node)
        count = 0
        for n in neighbors:
            count += 1
        return count

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        componenti = list(nx.connected_components(self.G))
        return len(componenti)

    def get_reachable_bfs_tree(self,start):
        tree_list = []
        tree = nx.bfs_tree(self.G, start)
        count = False
        for t in tree:
            if count: tree_list.append(t)
            else: count = True
        return tree_list

    def get_reachable_dfs_tree(self, start):
        tree_list = []
        tree = nx.dfs_tree(self.G, start)
        count = False
        for t in tree:
            if count:
                tree_list.append(t)
            else:
                count = True
        return tree_list

    def get_reachable_recursive(self, start, visited):
        if visited is None:
            visited = set()
        visited.add(start)
        for neighbor in self.G[start]:
            if neighbor not in visited:
                self.get_reachable_recursive(neighbor, visited)
        return visited

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
        adfs = self.get_reachable_dfs_tree(start)
        abfs = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_recursive(start, None)
        b.remove(start)

        return b