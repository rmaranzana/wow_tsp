from ortools.constraint_solver.pywrapcp import RoutingIndexManager, RoutingModel
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from typing import Tuple, List

"""
Este código está basado en la documentación de Google OR-Tools.
https://developers.google.com/optimization/routing/tsp
"""

def crear_callback_distancia(desde_index:int, hasta_index:int, \
    manager:RoutingIndexManager, matriz_nn:np.ndarray) -> float:
    """Devuelve la distancia entre dos nodos dados índices de OR-Tools

    Args:
        desde_index (int): Índice de nodo OR-Tools de origen.
        hasta_index (int): Índice de nodo OR-Tools de destino.
        matriz_nn (np.ndarray): Matriz Nodo-Nodo.

    Returns:
        float: Distancia entre dos nodos.
    """

    desde_nodo = manager.IndexToNode(desde_index)
    hasta_nodo = manager.IndexToNode(hasta_index)

    return matriz_nn[desde_nodo][hasta_nodo]

def optimizar_recorrido(coord:List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """Optimiza un problema de TSP dado un conjunto de coordenadas usando OR-Tools.

    Args:
        coord (List[List[float]]): Lista de coordenadas.

    Returns:
        List[List[float]]: Lista e coordenadas ordenadas.
    """

    # Cantidad de nodos.
    N = len(coord)

    # Crear el manager de ruteo.
    manager = RoutingIndexManager(N, 1, 0) # nodos, vehículos, punto de partida.

    # Crear modelo de ruteo.
    routing = RoutingModel(manager)

    # Crear Matriz Nodo-Nodo.
    eu_nn = euclidean_distances(coord)

    # Callback
    callback_distancia = lambda x, y: crear_callback_distancia(x, y, manager, eu_nn)
    callback_transit_registro = routing.RegisterTransitCallback(callback_distancia)

    # Definir costo de arcos
    routing.SetArcCostEvaluatorOfAllVehicles(callback_transit_registro)

    # Resolver el problema de TSP.
    solucion = routing.Solve()

    # Recuperar la lista ordenada de coordenadas de la solución:
    index = routing.Start(0)
    ruta_ordenada = [coord[manager.IndexToNode(index)]]

    while not routing.IsEnd(index):
        index = solucion.Value(routing.NextVar(index))
        ruta_ordenada.append(coord[manager.IndexToNode(index)])

    # Retornar ruta ordenada
    return ruta_ordenada


