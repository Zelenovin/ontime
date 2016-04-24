######>>>>>>  LISTOS PARA DESPEGAR <<<<<<###################
# Aplicacion desarrollada para Nasa Space Apps Rosario #####
######>>>>>>   DATOS DE CONTACTO   <<<<<<###################
#      Avila, Leilen      leiavila@gmail.com             ###
# Bolzan, Ana Emilia      anaemiliabolzan@hotmail.com    ###
# Ladreyt, Alejandro      ladreyt.alejandro@hotmail.com  ###
#     Ladreyt, Pablo      pabloladreyt@gmail.com         ###
######>>>>>>     OTROS DATOS     <<<<<<#####################
# Provincia: Sante Fe      Ano: 2016   #####################
# Localidad: Rosario                   #####################
############################################################

import requests
from geomag import *
import ctypes

def getDatosJSON(datos):
    FSkey = "2a772e44848fc7a7bc0a8fa2f13706ef"  # Key FlightStats
    cons = requests.get("https://api.flightstats.com/flex/schedules/rest/v1/json/flight/"
                     + datos[1] + "/" + datos[0] +
                     "/departing/" + "20" + datos[4] +
                      "/" + datos[3] + "/" + datos[2] +
                      "?appId=3f0e5ade&appKey=" + FSkey)
    consJson = cons.json()
    try:
        AeroPartida = consJson['scheduledFlights'][0]['departureAirportFsCode']
        HoraPartida = consJson['scheduledFlights'][0]['departureTime'][11:]       # Hora_Partida
        HoraDestino = consJson['scheduledFlights'][0]['arrivalTime'][11:]         # Hora_Destino
        EsJet = consJson['appendix']['equipments'][0]['jet']                      # Boolean: Es Jet?
        if AeroPartida == consJson['appendix']['airports'][0]['iata']:
            AeroPartida = consJson['appendix']['airports'][0]['icao']             # Aeropuerto_Partida_ICAO
            AeroDestino = consJson['appendix']['airports'][1]['icao']             # Aeropuerto_Destino_ICAO
            LatPartida = consJson['appendix']['airports'][0]['latitude']          # Latitud_Partida
            LngPartida = consJson['appendix']['airports'][0]['longitude']         # Longitud_Partida
            AltPartida = consJson['appendix']['airports'][0]['elevationFeet']     # Altitud_Partida
            LatDestino = consJson['appendix']['airports'][1]['latitude']          # Latitud_Destino
            LngDestino = consJson['appendix']['airports'][1]['longitude']         # Longitud_Destino
            AltDestino = consJson['appendix']['airports'][1]['elevationFeet']     # Altitud_Destino
        else:
            AeroPartida = consJson['appendix']['airports'][1]['icao']             # Aeropuerto_Partida_ICAO
            AeroDestino = consJson['appendix']['airports'][0]['icao']             # Aeropuerto_Destino_ICAO
            LatPartida = consJson['appendix']['airports'][1]['latitude']          # Latitud_Partida
            LngPartida = consJson['appendix']['airports'][1]['longitude']         # Longitud_Partida
            AltPartida = consJson['appendix']['airports'][1]['elevationFeet']     # Altitud_Partida
            LatDestino = consJson['appendix']['airports'][0]['latitude']          # Latitud_Destino
            LngDestino = consJson['appendix']['airports'][0]['longitude']         # Longitud_Destino
            AltDestino = consJson['appendix']['airports'][0]['elevationFeet']     # Altitud_Destino
            gm = geomag.GeoMag("WMM.COF")
        msg = gm.GeoMag(LatPartida, LngPartida, AltPartida)
        OrientacionPistaPartida = round(msg.dec / 10) * 10
        msg = gm.GeoMag(LatDestino, LngDestino, AltDestino)
        OrientacionPistaDestino = round(msg.dec / 10) * 10
        return [AeroPartida, HoraPartida, EsJet, LatPartida, LngPartida,
         AltPartida, OrientacionPistaPartida, AeroDestino, HoraDestino,
         LatDestino, LngDestino, AltDestino, OrientacionPistaDestino]
    except KeyError:
        ctypes.windll.user32.MessageBoxA(0, "Datos invalidos", "Error", 0)
    except IndexError:
        ctypes.windll.user32.MessageBoxA(0, "Datos invalidos", "Error", 0)
