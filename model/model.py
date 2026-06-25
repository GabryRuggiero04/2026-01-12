import copy
from cmath import inf

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._bestDiff = None
        self._listConstructors = None
        self._allEdges = None
        self._allNodes = None
        self._graph= nx.Graph()
        self._allConstructors= DAO.getAllConstructors()
        self._idMap={}
        for c in self._allConstructors:
            self._idMap[c.constructorId]= c

    def fillYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year1, year2):
        self._graph.clear()
        self._allNodes=DAO.getAllNodes(year1, year2)
        for node in self._allNodes:
            self._graph.add_node(self._idMap[node])
        self.allEdges(year1, year2)
        self.setOlderDriver(year1, year2)

    def allEdges(self, year1, year2):
        self._allEdges= DAO.getAllEdges(year1,year2)
        for e in self._allEdges:
            self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2])

    def getGraph(self):
        return self._graph

    def detailsGraph(self):
        return len(self._allEdges), len(self._allNodes)

    def getConnectedComponents(self):
        return list(nx.connected_components(self._graph))

    def getNumberConnComponents(self):
        return nx.number_connected_components(self._graph)

    def setOlderDriver(self, year1, year2):
        DAO.setOlderDriver(self._idMap, year1, year2)

    def getRicorsione(self, k ):
        self._listConstructors = []
        self._bestDiff = inf
        self._dimensione=k
        if self.getNumberConnComponents() < self._dimensione:
            return self._listConstructors, self._bestDiff
        self._compConn = self.getConnectedComponents()
        for i in range(len(self._compConn)):
            for n in self._compConn[i]:
                self.ricorsione([n], i)
        return self._listConstructors, self._bestDiff


    def ricorsione(self, consParziale, indiceComp):
        if len(consParziale)==self._dimensione:
            diff=self.calcoloDifferenzaTraVeterani(consParziale)
            if diff<self._bestDiff:
                self._bestDiff = diff
                self._listConstructors= copy.deepcopy(consParziale)
        else:
            for nextConnComp in range (indiceComp+1, len(self._compConn)):
                for nodo in self._compConn[nextConnComp]:
                    if nodo not in consParziale:
                        listPotenziale= list(consParziale)
                        listPotenziale.append(nodo)
                        diff=self.calcoloDifferenzaTraVeterani(listPotenziale)
                        if diff<self._bestDiff:
                            consParziale.append(nodo)
                            self.ricorsione(consParziale,nextConnComp)
                            consParziale.pop()

    def calcoloDifferenzaTraVeterani(self, parziale):
        lista=list(parziale)
        lista.sort(key=lambda x:x.oldest_driver_dob)
        diff = (lista[-1].oldest_driver_dob - lista[0].oldest_driver_dob).days
        if diff < self._bestDiff:
            return diff
        return inf