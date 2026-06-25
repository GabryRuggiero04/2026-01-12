import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillYears(self):
        years= self._model.fillYears()
        for y in years:
            self._view._ddAnno1.options.append(
                ft.dropdown.Option(text=y)
            )
            self._view._ddAnno2.options.append(
                ft.dropdown.Option(text=y)
            )
        self._view.update_page()

    def handleCreaGrafo(self,e):
        self._view.txt_result.controls.clear()
        year1= self._view._ddAnno1.value
        year2 = self._view._ddAnno2.value
        if year1 is None:
            self._view.txt_result.controls.append(
                ft.Text("Inserire anno minimo!!", color="red")
            )
            self._view.update_page()
            return
        if year2 is None:
            self._view.txt_result.controls.append(
                ft.Text("Inserire anno massimo!!", color="red")
            )
            self._view.update_page()
            return
        if int(year1) > int(year2):
            self._view.txt_result.controls.append(
                ft.Text("Il primo numero deve essere minore del secondo", color="red")
            )
            self._view.update_page()
            return
        self._model.buildGraph(year1, year2)
        numEdges, numNodes= self._model.detailsGraph()
        if numEdges<0 or numNodes<0:
            self._view.txt_result.controls.append(
                ft.Text("Grafo vuoto o creato in modo errato!!", color="red")
            )
            self._view.update_page()
            return
        else:
            self._view.txt_result.controls.append(
                ft.Text("Grafo creato correttamente", color="green")
            )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {numNodes}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {numEdges}")
        )
        self._view._btnstampa.disabled= False
        self._view._btnCerca.disabled= False
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()
        grafo= self._model.getGraph()
        edgesList= list(grafo.edges(data=True))
        edgesList.sort(key=lambda x: x[2]["weight"], reverse=True)
        top=3
        if len(edgesList)<3:
            top= len(edgesList)
        self._view.txt_result.controls.append(
            ft.Text("Archi di peso maggiore: ", color="green")
        )
        for e in range(top):
            self._view.txt_result.controls.append(
                ft.Text(f"{edgesList[e][0].name} --> {edgesList[e][1].name} ({edgesList[e][2]["weight"]} piloti condivisi)")
            )

        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumberConnComponents()} componenti connesse", color="green")
        )
        connComp= self._model.getConnectedComponents()
        maxComp=max(connComp, key=len)
        self._view.txt_result.controls.append(
            ft.Text(f"Componente più grande ({len(maxComp)} nodi) : ", color="green")
        )
        nodoDegree=[]
        for n in maxComp:
            self._view.txt_result.controls.append(
                ft.Text(n)
            )
            nodoDegree.append((n,grafo.degree(n)))
        nodoDegree.sort(key=lambda x: x[1], reverse=True)
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa più grande in ordine decrescente di grado : ", color="green")
        )
        for n,degree in nodoDegree:
            self._view.txt_result.controls.append(
                ft.Text(f"{n} --> (grado: {degree})")
            )
        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        k = self._view._txtInK.value
        if k == "":
            self._view.txt_result.controls.append(
                ft.Text("Nessun numero di piloti inserito", color="red")
            )
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except:
            self._view.txt_result.controls.append(
                ft.Text("Inserire un numero intero", color="red")
            )
            self._view.update_page()
            return
        if kInt < 0:
            self._view.txt_result.controls.append(
                ft.Text("Inserire un numero positivo", color="red")
            )
            self._view.update_page()
            return
        listaConstructors, diff= self._model.getRicorsione(kInt)
        if len(listaConstructors) <1:
            self._view.txt_result.controls.append(
                ft.Text("Non esistono insieme di costruttori con la dimensione inserita", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Lo scarto di età è di {diff} giorni", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text("Ecco la lista di costruttori: ", color="green")
        )
        for c in listaConstructors:
            self._view.txt_result.controls.append(
                ft.Text(f"{c}-->({c.oldest_driver_dob})")
            )
        listaConstructors.sort(key=lambda x: x.oldest_driver_dob, reverse=True)
        self._view.txt_result.controls.append(
            ft.Text("I costruttori con il veterano più giovane e più anziano sono rispettivamente: ", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"{listaConstructors[0]} --> ({listaConstructors[0].oldest_driver_dob})")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"{listaConstructors[-1]} --> ({listaConstructors[-1].oldest_driver_dob})")
        )
        self._view.update_page()
