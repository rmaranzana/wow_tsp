import requests
from bs4 import BeautifulSoup
import json
import re
import urllib.request as urllib2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def obtener_coordenadas_wowhead(id_objeto:int, id_zona:int) -> list:
    """Función que devuelve coordenadas de objetos de classic.wowhead.com

    Args:
        id_objeto (int): ID del objeto en classic.wowhead.com
        id_zona (int): ID de la zona en classic.wowhead.com

    Returns:
        list: diccionario de coordenadas
    """
    # Obtener parseo de página:
    r = requests.get(f'https://classic.wowhead.com/object={id_objeto}')
    soup = BeautifulSoup(r.text, 'html.parser')

    # Buscar datos geoespaciales:
    pattern = re.compile(r'\bg_mapperData\b', re.MULTILINE | re.DOTALL)
    raw = soup.find_all('script', text=pattern)[0]

    # Convertir en estructura de diccionarios:
    json_string = re.findall(r'({.*})', raw.contents[0])[0]
    json_content = json.loads(json_string)

    # Recuperar coordenadas:
    coords = json_content[str(id_zona)][0]['coords']

    return coords


def obtener_imagen_mapa(id_zona:int) -> np.ndarray:
    """Retorna la imagen de un mapa del WoW segun su ID de zona.

    Args:
        id_zona (int): ID de la zona en classic.wowhead.com

    Returns:
        numpy.ndarray: Imagen un un Numpy array.
    """
    mapa = urllib2.urlopen(f'https://wow.zamimg.com/images/wow/classic/maps/eses/original/{id_zona}.jpg')
    
    return plt.imread(mapa, format='jpeg')


def obtener_imagen_pin() -> np.ndarray:
    """Retorna la imagen del pin del mapa del WoW.

    Returns:
        numpy.ndarray: Imagen un un Numpy array.
    """
    pinurl = urllib2.urlopen(f'https://wow.zamimg.com/images/Mapper/pin-yellow.png')

    return plt.imread(pinurl, format='jpg')


def crear_plot(ordered_coords:int, id_zona:int) -> None:
    """Crea un plot con el recorrido optimizado y lo muestra.

    Args:
        ordered_coords (int): coordenadas ordenadas por el solver
        id_zona (int): ID de la zona en classic.wowhead.com
    """
    # Deszippear coordeandas
    x, y = np.array(list(map(list, zip(*(ordered_coords)))))

    # Obtener mapa y sus dimensiones
    maparead = obtener_imagen_mapa(id_zona)
    dpi = 100
    w = maparead.shape[:2][0] / dpi
    l = maparead.shape[:2][1] / dpi

    # Escalar
    x *= l
    y *= w

    # Crear plot
    _, ax = plt.subplots(figsize=(l, w), dpi=dpi)

    # Plottear recorrido
    ax.plot(x, y, color='r', linewidth=2.)

    # Obtener imagen de pin y ubicarla en plot
    pinimg = obtener_imagen_pin()
    pinimg = OffsetImage(pinimg, zoom=.7)

    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(pinimg, (x0, y0), frameon=False)
        ax.add_artist(ab)
    
    # Ubicar mapa de fondo
    ax.imshow(maparead)

    # Plottear
    plt.show()
