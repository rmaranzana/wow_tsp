from utils import obtener_coordenadas_wowhead, crear_plot
from tsp_solver import optimizar_recorrido

def obtener_mapa_optimizado(id_objeto, id_zona):
    # Obtener coordenadas de wowhead
    coordenadas = obtener_coordenadas_wowhead(id_objeto, id_zona)

    # Optimizar recorrido
    coordenadas_ord = optimizar_recorrido(coordenadas)

    # Crear plot
    crear_plot(coordenadas_ord, id_zona)


if __name__ == '__main__':
    # Inputs
    id_objeto = 1618 # Flor de paz
    id_zona = 141 # Teldrassil

    # Ejecutar rutina
    obtener_mapa_optimizado(id_objeto, id_zona)