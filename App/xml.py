######>>>>>>  LISTOS PARA DESPEGAR <<<<<<###################
# Aplicacion desarrollada para Nasa Space Apps Rosario #####
######>>>>>>   DATOS DE CONTACTO   <<<<<<###################
#      Avila, Leilen      leilenavila@gmail.com          ###
# Bolzan, Ana Emilia      anaemiliabolzan@hotmail.com    ###
# Ladreyt, Alejandro      ladreyt.alejandro@hotmail.com  ###
#     Ladreyt, Pablo      pabloladreyt@gmail.com         ###
######>>>>>>     OTROS DATOS     <<<<<<#####################
# Provincia: Sante Fe      Ano: 2016   #####################
# Localidad: Rosario                   #####################
############################################################

import requests
import math
from lxml import etree

def getDatosXML(AeroPartida, OrientacionPista):
    xmlcontenido = requests.get('https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=' + AeroPartida + '&hoursBeforeNow=24&mostRecent=true')
    xmltemporal = str(xmlcontenido.content).replace('\n', "")
    xmltemporal = xmltemporal.replace('<?xml version="1.0" encoding="UTF-8"?>',"")
    xmltemporal = xmltemporal.replace(' /', '/')
    xml = open('xml.xml', 'wb')
    xml.write(xmltemporal)
    xml.close()
    doc = etree.parse('xml.xml')
    root = doc.getroot()
    METAR = root.find("data/METAR")
    for child in METAR:
        if child.tag == "temp_c":
            Temperatura = float(child.text)
        if child.tag == "dewpoint_c":
            TemperaturaRocio = float(child.text)
        if child.tag == "wind_dir_degrees":
            AnguloViento = child.text
        if child.tag == "wind_speed_kt":
            VelocidadViento = child.text
        if child.tag == "visibility_statute_mi":
            Visibilidad = child.text
        if child.tag == "sky_condition":
            EstadoClima = child.attrib['sky_cover']
    Humedad = 100 * (math.exp((17.625 * TemperaturaRocio) / (243.04 +
              TemperaturaRocio)) / math.exp((17.625 * Temperatura) /
              (243.04 + Temperatura)))
    VientoCruzado = (float(VelocidadViento) *
                     math.sin(int(AnguloViento) - int(OrientacionPista)))
    return [Humedad, EstadoClima, Visibilidad, VientoCruzado]
