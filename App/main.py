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

from Tkinter import *
import xml
import json
import wx
import wx.calendar as cal
from math import *

# alertas= [NroAlerta: [Descripcion, color a mostrar]
alertas = {0: ["El vuelo no presenta problemas climaticos", "#006400"],
           1: ["Vuelo con posibilidad de demoras", "yellow"],
           2: ["Posible cancelacion de vuelo", "red"]}


class Factores:
    def __init__(self, Humedad, Sky, Visibilidad, VientoCruzado):
        self.Humedad = Humedad                # Humedad Relativa
        self.Sky = Sky                        # Condicion climatica
        self.Visibilidad = Visibilidad        # Millas Terrestres
        self.VientoCruzado = VientoCruzado    # Nudos por hora


def EstadoVuelo(Humedad, sky, Visibilidad, VientoCruzado):
# VCTS: Thunderstorm in vicinity, TS: Thunderstorm, IC: Ice Crystals
# SN: Snow, SOG: Snow on the ground, SINICR: snow increasing rapidly
    if (sky == "VCTS" or sky == "TS" or sky == "IC" or    
        sky == "SN" or sky == "SOG" or
        sky == "SNINCR" or Visibilidad < 0.124274):
        Stat = 2
    elif ((abs(VientoCruzado) >= 17) or
         (Visibilidad < 10 and Humedad > 80)):
        Stat = 1
    else:
        Stat = 0
    return Stat


def interfaz():
    #--------------------------- CALENDARIO -------------------------------
    class MyCalendar(wx.Dialog):
        # Definicion de ventana con calendario
        def __init__(self, parent, mytitle):
            wx.Dialog.__init__(self, parent, wx.ID_ANY, mytitle)
            vbox = wx.BoxSizer(wx.VERTICAL)
            self.calendar = cal.CalendarCtrl(self, wx.ID_ANY, wx.DateTime_Now())
            vbox.Add(self.calendar, 0, wx.EXPAND | wx.ALL, border=20)
            self.calendar.Bind(cal.EVT_CALENDAR, self.onCalSelected)
            button = wx.Button(self, wx.ID_ANY, 'Ok')
            vbox.Add(button, 0, wx.ALL | wx.ALIGN_CENTER, border=20)
            self.Bind(wx.EVT_BUTTON, self.onQuit, button)
            self.SetSizerAndFit(vbox)
            self.Show(True)
            self.Centre()
        # Se selecciona un dia

        def onCalSelected(self, event):
            date = self.calendar.GetDate()
            date = str(date)
            entryText.set(date[:8])
            self.onQuit(cal.EVT_CALENDAR_DAY)
        # Se presiona el boton Ok

        def onQuit(self, event):
            self.Destroy()
        # Instanciacion de calendario

    def calendario(event):
        MyCalendar(None, 'Seleccione fecha de partida')
        app.MainLoop()
    global TxtNV
    global TxtFecha
    global TxtAero
    app = wx.App(0)
    menu = Tk()
    menu.title('Menu')
    Label(menu, text="Ingrese su numero de vuelo: ").grid(row=0)
    TxtNV = Entry(menu)
    TxtNV.grid(row=0, column=1)
    Label(menu, text="Ingrese fecha: ").grid(row=1)
    entryText = StringVar()
    TxtFecha = Entry(menu, textvariable=entryText, state="disabled")
    TxtFecha.grid(row=1, column=1)
    Label(menu, text="Ingrese codigo aerolinea: ").grid(row=2)
    TxtAero = Entry(menu)
    TxtAero.grid(row=2, column=1)
    Button(menu, text="Ver estado", padx=60,
          pady=20, command=VerVuelo).grid(row=3, column=1)
    Button(menu, text="Salir", padx=120, pady=20, command=quit).grid(row=3)
    global estadoText
    estadoText = StringVar()
    global LblRespuesta
    LblRespuesta = Label(menu, textvariable=estadoText, font="bold")
    LblRespuesta.grid(row=4)
    TxtFecha.bind('<Button-1>', calendario)


    menu.mainloop()


def VerVuelo():
    datos = []
    if not TxtNV.get() or not TxtFecha.get() or not TxtAero.get():
        print ("Debe completar todos los campos")
        return
    elif not (TxtNV.get()).isdigit():
        print ("El numero de vuelo debe estar conformado por numeros")
        return
    elif len(TxtAero.get()) != 3 or not TxtAero.get().isalpha():
        print ("El codigo de aerolinea debe estar conformado por 3 letras")
        return
    fecha = TxtFecha.get().split("/")
    datos.extend([TxtNV.get(), TxtAero.get().upper(), fecha[1],
                                             fecha[0], fecha[2]])
     # datos [0=NroVuelo, 1=CodAerolinea, 2=Dia, 3=Mes, 4=Ano]
    datosConsJson = json.getDatosJSON(datos)
   # datosConsJson[0=CodAeropuertoICAOPartida, 1=HorarioPartida,
   #               2=TipoAvion(Jet,TurboHelice), 3=LatitudPartida,
   #               4=LongitudPartida, 5=AltitudPartida,
   #               6=OrientacionPistaPartida, 7=CodAeropuertoICAODestino,
   #               8=HorarioDestino, 9=LatitudDestino, 10=LongitudDestino,
   #               11=AltitudDestino, 12=OrientacionPistaDestino]
    if datosConsJson is not None:
        datosConsXML = xml.getDatosXML(datosConsJson[0], datosConsJson[6])
        # datosConsXML[0=Humedad, 1=EstadoClima,
        #              2=Visibilidad(millas), 3=VientoCruzado(kt)]
        Partida = Factores(datosConsXML[0], datosConsXML[1], datosConsXML[2],
                          datosConsXML[3])
        datosConsXML = xml.getDatosXML(datosConsJson[7], datosConsJson[12])
        Destino = Factores(datosConsXML[0], datosConsXML[1], datosConsXML[2],
                          datosConsXML[3])
        EstadoDest = EstadoVuelo(Destino.Humedad, Destino.Sky,
                                   Destino.Visibilidad, Destino.VientoCruzado)
        EstadoPart = EstadoVuelo(Partida.Humedad, Partida.Sky,
                                   Partida.Visibilidad, Partida.VientoCruzado)
        estadoText.set(alertas[max(EstadoDest, EstadoPart)][0])
        LblRespuesta.config(fg=alertas[max(EstadoDest, EstadoPart)][1],
                            font=("Helvetica", 8, "bold"))
interfaz()
