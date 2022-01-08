from utils import obtener_coordenadas_wowhead, crear_plot
from tsp_solver import optimizar_recorrido

def obtener_mapa_optimizado(id_objeto, id_zona):
    # Obtener coordenadas de wowhead
    coordenadas = obtener_coordenadas_wowhead(id_objeto, id_zona)

    # Optimizar recorrido
    ordered_coords = optimizar_recorrido(coordenadas)

    # Crear plot
    crear_plot(ordered_coords, id_zona)


if __name__ == '__main__':
    # Parsear argumentos
    id_objeto = 1618 # Flor de paz
    id_zona = 141 # Tierras del interior

    # Ejecutar rutina
    obtener_mapa_optimizado(id_objeto, id_zona)