import tkinter as tk
from ControladorAlarma import ControladorAlarma
from FrontendInterfaz import FrontendInterfaz

# ARCHIVO PRINCIPAL PURO (Cumple sección 3 del Parcial III)
ventana_principal = tk.Tk()
controlador_sistema = ControladorAlarma()
app_alarma = FrontendInterfaz(ventana_principal, controlador_sistema)

ventana_principal.mainloop()