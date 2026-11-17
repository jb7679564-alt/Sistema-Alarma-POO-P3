import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# CLASE FRONTEND DE LA INTERFAZ GRÁFICA
class FrontendInterfaz:
    def __init__(self, ventana, controlador):
        self.ventana = ventana
        self.controlador = controlador

        self.ventana.title("Terminal de Control Avanzada - Alarma Inteligente")
        self.ventana.geometry("1080x680")
        self.ventana.configure(bg="#1b2631")

        # Variables de control de Tkinter
        self.var_nombre = tk.StringVar()
        self.var_tipo_doc = tk.StringVar(value="Cédula de Ciudadanía")
        self.var_num_doc = tk.StringVar()
        self.var_sensibilidad = tk.StringVar(value="Alta")
        self.var_silencioso = tk.BooleanVar(value=False)

        self.id_temporizador_warning = None
        self.segundos_restantes = 0

        self.__crear_menu_superior()
        self.__crear_banner_superior()
        self.__crear_barra_operador()
        self.__crear_barra_controles_extra()
        self.__crear_consola_central()
        self.__crear_tablero_estados()

        self.actualizar_indicadores_visuales()
        self.escribir_en_consola("Sistema listo. Registre sus datos arriba y escriba 'inicio' abajo para armar la alarma.")

    # 1. BARRA DE MENÚ SUPERIOR (Menu + filedialog)
    def __crear_menu_superior(self):
        barra_menu = tk.Menu(self.ventana)
        menu_archivo = tk.Menu(barra_menu, tearoff=0)

        menu_archivo.add_command(label="Ver Base de Datos y Monitoreo", command=self.abrir_ventana_monitoreo)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Abrir archivo Excel...", command=self.accion_abrir_excel)
        menu_archivo.add_command(label="Guardar copia Excel como...", command=self.accion_guardar_como)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.ventana.destroy)

        barra_menu.add_cascade(label="Archivo y Datos", menu=menu_archivo)
        self.ventana.config(menu=barra_menu)

    # 2. BANNER DE BIENVENIDA (Estética de tu diseño)
    def __crear_banner_superior(self):
        frame_banner = tk.Frame(self.ventana, bg="#154360", bd=2, relief="groove")
        frame_banner.pack(fill="x", padx=12, pady=(10, 5))

        tk.Label(
            frame_banner,
            text="¡BIENVENIDO A TU ALARMA INTELIGENTE!",
            font=("Segoe UI", 13, "bold"),
            fg="#48c9b0",
            bg="#154360"
        ).pack(pady=(6, 2))

        tk.Label(
            frame_banner,
            text="Instrucción: Registre sus datos de operador, luego escriba 'inicio' en la consola y presione Enter.",
            font=("Segoe UI", 9, "italic"),
            fg="#d6eaf8",
            bg="#154360"
        ).pack(pady=(0, 6))

    # 3. BARRA DE REGISTRO DE OPERADOR (Sustituye puerto COM por Datos Personales)
    def __crear_barra_operador(self):
        frame_op = tk.Frame(self.ventana, bg="#2c3e50", bd=1, relief="raised")
        frame_op.pack(fill="x", padx=12, pady=4)

        tk.Label(frame_op, text="Nombre:", font=("Segoe UI", 9, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=(10, 4), pady=8)
        entry_nombre = tk.Entry(frame_op, textvariable=self.var_nombre, width=22, font=("Segoe UI", 9))
        entry_nombre.pack(side="left", padx=4)

        tk.Label(frame_op, text="Tipo ID:", font=("Segoe UI", 9, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=(10, 4))
        combo_doc = ttk.Combobox(
            frame_op,
            textvariable=self.var_tipo_doc,
            values=("Cédula de Ciudadanía", "Tarjeta de Identidad"),
            state="readonly",
            width=21
        )
        combo_doc.pack(side="left", padx=4)

        tk.Label(frame_op, text="N° Documento:", font=("Segoe UI", 9, "bold"), fg="white", bg="#2c3e50").pack(side="left", padx=(10, 4))
        entry_doc = tk.Entry(frame_op, textvariable=self.var_num_doc, width=16, font=("Segoe UI", 9))
        entry_doc.pack(side="left", padx=4)

        btn_registrar = tk.Button(
            frame_op,
            text="Guardar Operador",
            command=self.accion_registrar_operador,
            bg="#2980b9",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        )
        btn_registrar.pack(side="left", padx=10)

        # Indicador derecho (Estado de Operador Activo)
        self.lbl_operador_activo = tk.Label(
            frame_op,
            text="SIN OPERADOR",
            font=("Segoe UI", 9, "bold"),
            bg="#566573",
            fg="#d5d8dc",
            width=20,
            relief="sunken"
        )
        self.lbl_operador_activo.pack(side="right", padx=10, pady=6)

    # 4. BARRA DE CONTROLES ADICIONALES (Radiobutton, Checkbutton, Simulación PIR, Progressbar)
    def __crear_barra_controles_extra(self):
        frame_ctrl = tk.Frame(self.ventana, bg="#212f3d")
        frame_ctrl.pack(fill="x", padx=12, pady=3)

        # Radiobuttons de sensibilidad
        tk.Label(frame_ctrl, text="Sensibilidad PIR:", fg="#aed6f1", bg="#212f3d", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(10, 4))
        for nivel in ["Baja", "Media", "Alta"]:
            tk.Radiobutton(
                frame_ctrl,
                text=nivel,
                variable=self.var_sensibilidad,
                value=nivel,
                command=self.accion_cambiar_sensibilidad,
                bg="#212f3d",
                fg="white",
                selectcolor="#154360",
                activebackground="#212f3d",
                activeforeground="white"
            ).pack(side="left", padx=2)

        # Checkbutton modo silencioso
        tk.Checkbutton(
            frame_ctrl,
            text="Modo Silencioso",
            variable=self.var_silencioso,
            command=self.accion_cambiar_silencioso,
            bg="#212f3d",
            fg="#f9e79f",
            selectcolor="#154360",
            activebackground="#212f3d",
            activeforeground="#f9e79f"
        ).pack(side="left", padx=15)

        # Botón para abrir la ventana secundaria de Excel (Toplevel)
        tk.Button(
            frame_ctrl,
            text="📊 Ver Base de Datos (Excel)",
            command=self.abrir_ventana_monitoreo,
            bg="#117a65",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(side="right", padx=10, pady=4)

        # Botón para simular detección del Sensor PIR
        tk.Button(
            frame_ctrl,
            text="🏃 Simular Movimiento PIR",
            command=self.accion_simular_movimiento,
            bg="#d68910",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2"
        ).pack(side="right", padx=6, pady=4)

    # 5. CONSOLA CENTRAL Y ENTRADA CON .bind("<Return>") + ELEMENTO NUEVO (Progressbar)
    def __crear_consola_central(self):
        frame_consola = tk.Frame(self.ventana, bg="#1b2631")
        frame_consola.pack(fill="both", expand=True, padx=12, pady=4)

        header_consola = tk.Frame(frame_consola, bg="#1b2631")
        header_consola.pack(fill="x")

        tk.Label(
            header_consola,
            text="Consola de Monitoreo y Comandos (Escribe abajo y pulsa Enter):",
            font=("Segoe UI", 9, "bold"),
            fg="white",
            bg="#1b2631"
        ).pack(side="left", pady=2)

        # ELEMENTO ADICIONAL INVESTIGADO (ttk.Progressbar para cuenta regresiva WARNING)
        self.lbl_tiempo = tk.Label(header_consola, text="Tiempo límite: --", fg="#f5b041", bg="#1b2631", font=("Segoe UI", 9, "bold"))
        self.lbl_tiempo.pack(side="right", padx=(6, 0))

        self.barra_progreso = ttk.Progressbar(header_consola, orient="horizontal", length=180, mode="determinate")
        self.barra_progreso.pack(side="right", padx=4)

        # Área de historial de consola (solo lectura)
        self.texto_consola = tk.Text(
            frame_consola,
            bg="#141d26",
            fg="#e5e8e8",
            font=("Consolas", 10),
            state="disabled",
            wrap="word",
            bd=2,
            relief="sunken"
        )
        self.texto_consola.pack(fill="both", expand=True, pady=(2, 6))

        # Barra inferior de escritura directa (Usa .bind("<Return>"))
        frame_input = tk.Frame(frame_consola, bg="#1b2631")
        frame_input.pack(fill="x")

        tk.Label(frame_input, text=">>>", font=("Consolas", 11, "bold"), fg="#48c9b0", bg="#1b2631").pack(side="left", padx=(0, 6))
        self.entry_comando = tk.Entry(frame_input, bg="#212f3d", fg="white", insertbackground="white", font=("Consolas", 11))
        self.entry_comando.pack(side="left", fill="x", expand=True, ipady=4)

        # Evento .bind() obligatorio del PDF
        self.entry_comando.bind("<Return>", self.evento_enter_consola)

        tk.Button(
            frame_input,
            text="Enviar",
            command=lambda: self.evento_enter_consola(None),
            bg="#2874a6",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            width=10
        ).pack(side="left", padx=(6, 0), ipady=2)

    # 6. TABLERO DE ESTADOS EN TIEMPO REAL (Los 4 bloques luminosos inferiores)
    def __crear_tablero_estados(self):
        marco_tablero = tk.LabelFrame(
            self.ventana,
            text=" TABLERO DE ESTADOS EN TIEMPO REAL ",
            font=("Segoe UI", 8, "bold"),
            fg="white",
            bg="#1b2631",
            bd=1
        )
        marco_tablero.pack(fill="x", padx=12, pady=(2, 10))

        self.ind_on_off = tk.Label(marco_tablero, text="💡 ON / OFF (APAGADO)", font=("Segoe UI", 10, "bold"), height=2, relief="ridge")
        self.ind_on_off.pack(side="left", fill="x", expand=True, padx=6, pady=6)

        self.ind_inicio = tk.Label(marco_tablero, text="✔ INICIO (ARMADO)", font=("Segoe UI", 10, "bold"), height=2, relief="ridge")
        self.ind_inicio.pack(side="left", fill="x", expand=True, padx=6, pady=6)

        self.ind_warning = tk.Label(marco_tablero, text="⚠ WARNING (CLAVE)", font=("Segoe UI", 10, "bold"), height=2, relief="ridge")
        self.ind_warning.pack(side="left", fill="x", expand=True, padx=6, pady=6)

        self.ind_alarm = tk.Label(marco_tablero, text="🚨 ALARM (ROBO)", font=("Segoe UI", 10, "bold"), height=2, relief="ridge")
        self.ind_alarm.pack(side="left", fill="x", expand=True, padx=6, pady=6)

    # =========================================================
    # MÉTODOS DE INTERACCIÓN Y ACTUALIZACIÓN VISUAL
    # =========================================================
    def escribir_en_consola(self, mensaje):
        self.texto_consola.config(state="normal")
        self.texto_consola.insert(tk.END, mensaje + "\n")
        self.texto_consola.see(tk.END)
        self.texto_consola.config(state="disabled")

    def actualizar_indicadores_visuales(self):
        estado = self.controlador.consultar_estado_actual()

        # Colores apagados por defecto (tenues)
        self.ind_on_off.config(bg="#4d5656", fg="#909497")
        self.ind_inicio.config(bg="#145a32", fg="#52be80")
        self.ind_warning.config(bg="#7e5109", fg="#f5b041")
        self.ind_alarm.config(bg="#641e16", fg="#ec7063")

        # Encender intensamente el indicador correspondiente al estado actual
        if estado == "APAGADO":
            self.ind_on_off.config(bg="#aeb6bf", fg="#17202a")
            self.__detener_temporizador_warning()
        elif estado == "INICIO":
            self.ind_inicio.config(bg="#27ae60", fg="white")
            self.__detener_temporizador_warning()
        elif estado == "WARNING":
            self.ind_warning.config(bg="#f39c12", fg="black")
        elif estado == "ALARM":
            self.ind_alarm.config(bg="#e74c3c", fg="white")
            self.__detener_temporizador_warning()

    def accion_registrar_operador(self):
        try:
            mensaje = self.controlador.configurar_operador(
                self.var_nombre.get(),
                self.var_tipo_doc.get(),
                self.var_num_doc.get()
            )
            self.lbl_operador_activo.config(
                text=self.controlador.obtener_nombre_operador().upper(),
                bg="#27ae60",
                fg="white"
            )
            self.escribir_en_consola(mensaje)
            messagebox.showinfo("Operador Registrado", "Datos guardados correctamente en la base de datos Excel.")
        except ValueError as err:
            messagebox.showerror("Error de Validación", str(err))

    def accion_cambiar_sensibilidad(self):
        msg = self.controlador.cambiar_sensibilidad(self.var_sensibilidad.get())
        self.escribir_en_consola(msg)

    def accion_cambiar_silencioso(self):
        msg = self.controlador.cambiar_modo_silencioso(self.var_silencioso.get())
        self.escribir_en_consola(msg)

    def accion_simular_movimiento(self):
        detectado, mensaje = self.controlador.simular_deteccion_movimiento()
        self.escribir_en_consola(mensaje)
        self.actualizar_indicadores_visuales()
        if detectado:
            self.__iniciar_temporizador_warning()

    def evento_enter_consola(self, event):
        texto = self.entry_comando.get()
        self.entry_comando.delete(0, tk.END)
        if texto.strip():
            self.escribir_en_consola(f"> {texto}")
            respuestas = self.controlador.procesar_comando_consola(texto)
            for linea in respuestas:
                self.escribir_en_consola(linea)
            self.actualizar_indicadores_visuales()

    # Temporizador visual de 5 segundos para estado WARNING usando Progressbar
    def __iniciar_temporizador_warning(self):
        self.__detener_temporizador_warning()
        total_seg = self.controlador.obtener_tiempo_warning()
        self.segundos_restantes = total_seg
        self.barra_progreso["maximum"] = total_seg
        self.barra_progreso["value"] = total_seg
        self.__tick_warning()

    def __tick_warning(self):
        if self.controlador.consultar_estado_actual() != "WARNING":
            self.__detener_temporizador_warning()
            return

        self.lbl_tiempo.config(text=f"Tiempo límite: {self.segundos_restantes}s")
        self.barra_progreso["value"] = self.segundos_restantes

        if self.segundos_restantes <= 0:
            disparada, msg = self.controlador.disparar_robo_por_tiempo()
            if disparada:
                self.escribir_en_consola(msg)
                self.actualizar_indicadores_visuales()
            return

        self.segundos_restantes -= 1
        self.id_temporizador_warning = self.ventana.after(1000, self.__tick_warning)

    def __detener_temporizador_warning(self):
        if self.id_temporizador_warning is not None:
            self.ventana.after_cancel(self.id_temporizador_warning)
            self.id_temporizador_warning = None
        self.barra_progreso["value"] = 0
        self.lbl_tiempo.config(text="Tiempo límite: --")

    # =========================================================
    # GESTIÓN DE ARCHIVOS EXCEL (filedialog)
    # =========================================================
    def accion_abrir_excel(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar base de datos Excel",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if not ruta:
            return
        try:
            self.controlador.obtener_backend_excel().cambiar_ruta_archivo(ruta)
            messagebox.showinfo("Archivo Cargado", f"Base de datos vinculada:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")

    def accion_guardar_como(self):
        ruta = filedialog.asksaveasfilename(
            title="Guardar copia de base de datos",
            defaultextension=".xlsx",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if not ruta:
            return
        try:
            self.controlador.obtener_backend_excel().guardar_copia_como(ruta)
            messagebox.showinfo("Copia Guardada", "El respaldo en Excel fue guardado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la copia: {e}")

    # =========================================================
    # VENTANA SECUNDARIA (Toplevel) CON PESTAÑAS Y TREEVIEW
    # =========================================================
    def abrir_ventana_monitoreo(self):
        ventana_bd = tk.Toplevel(self.ventana)
        ventana_bd.title("Base de Datos y Monitoreo Histórico (Excel)")
        ventana_bd.geometry("820x480")
        ventana_bd.configure(bg="#1b2631")

        backend = self.controlador.obtener_backend_excel()

        cuaderno = ttk.Notebook(ventana_bd)
        cuaderno.pack(fill="both", expand=True, padx=10, pady=10)

        # PESTAÑA 1: USUARIOS REGISTRADOS
        tab_usuarios = tk.Frame(cuaderno, bg="#212f3d")
        cuaderno.add(tab_usuarios, text="👤 Usuarios Registrados")

        cols_u = ("fecha", "nombre", "tipo", "documento")
        tabla_usuarios = ttk.Treeview(tab_usuarios, columns=cols_u, show="headings", height=12)
        tabla_usuarios.heading("fecha", text="Fecha Registro")
        tabla_usuarios.heading("nombre", text="Nombre Completo")
        tabla_usuarios.heading("tipo", text="Tipo Documento")
        tabla_usuarios.heading("documento", text="N° Documento")

        tabla_usuarios.column("fecha", width=150)
        tabla_usuarios.column("nombre", width=220)
        tabla_usuarios.column("tipo", width=180)
        tabla_usuarios.column("documento", width=140)
        tabla_usuarios.pack(fill="both", expand=True, padx=10, pady=10)

        def cargar_tabla_usuarios():
            for item in tabla_usuarios.get_children():
                tabla_usuarios.delete(item)
            for fila in backend.leer_usuarios():
                tabla_usuarios.insert("", tk.END, values=fila)

        def eliminar_usuario_sel():
            sel = tabla_usuarios.selection()
            if not sel:
                messagebox.showerror("Error", "Seleccione un usuario de la tabla para eliminar.", parent=ventana_bd)
                return
            indice = tabla_usuarios.index(sel[0])
            backend.eliminar_usuario(indice)
            cargar_tabla_usuarios()
            messagebox.showinfo("Eliminado", "Usuario eliminado de Excel.", parent=ventana_bd)

        def actualizar_usuario_sel():
            sel = tabla_usuarios.selection()
            if not sel:
                messagebox.showerror("Error", "Seleccione un usuario para actualizar sus datos.", parent=ventana_bd)
                return
            valores = tabla_usuarios.item(sel[0], "values")
            indice = tabla_usuarios.index(sel[0])

            # Mini diálogo de edición
            win_edit = tk.Toplevel(ventana_bd)
            win_edit.title("Editar Usuario")
            win_edit.geometry("340x210")
            tk.Label(win_edit, text="Nuevo Nombre:").pack(pady=(10, 2))
            e_nom = tk.Entry(win_edit, width=30)
            e_nom.insert(0, valores[1])
            e_nom.pack()

            tk.Label(win_edit, text="Tipo Documento:").pack(pady=(8, 2))
            c_tip = ttk.Combobox(win_edit, values=("Cédula de Ciudadanía", "Tarjeta de Identidad"), state="readonly", width=27)
            c_tip.set(valores[2])
            c_tip.pack()

            tk.Label(win_edit, text="N° Documento:").pack(pady=(8, 2))
            e_doc = tk.Entry(win_edit, width=30)
            e_doc.insert(0, valores[3])
            e_doc.pack()

            def guardar_edicion():
                backend.actualizar_usuario(indice, e_nom.get().strip(), c_tip.get(), e_doc.get().strip())
                cargar_tabla_usuarios()
                win_edit.destroy()
                messagebox.showinfo("Actualizado", "Registro actualizado en Excel.", parent=ventana_bd)

            tk.Button(win_edit, text="Guardar Cambios", command=guardar_edicion, bg="#27ae60", fg="white").pack(pady=12)

        frame_btns_u = tk.Frame(tab_usuarios, bg="#212f3d")
        frame_btns_u.pack(pady=(0, 10))
        tk.Button(frame_btns_u, text="✏️ Actualizar Seleccionado", command=actualizar_usuario_sel, bg="#2980b9", fg="white").pack(side="left", padx=8)
        tk.Button(frame_btns_u, text="🗑️ Eliminar Seleccionado", command=eliminar_usuario_sel, bg="#c0392b", fg="white").pack(side="left", padx=8)

        # PESTAÑA 2: HISTORIAL DE EVENTOS DE ALARMA
        tab_eventos = tk.Frame(cuaderno, bg="#212f3d")
        cuaderno.add(tab_eventos, text="🛡️ Monitoreo de Eventos")

        cols_e = ("fecha", "operador", "estado", "evento")
        tabla_eventos = ttk.Treeview(tab_eventos, columns=cols_e, show="headings", height=12)
        tabla_eventos.heading("fecha", text="Fecha y Hora")
        tabla_eventos.heading("operador", text="Operador")
        tabla_eventos.heading("estado", text="Estado")
        tabla_eventos.heading("evento", text="Detalle del Evento")

        tabla_eventos.column("fecha", width=145)
        tabla_eventos.column("operador", width=150)
        tabla_eventos.column("estado", width=95)
        tabla_eventos.column("evento", width=360)
        tabla_eventos.pack(fill="both", expand=True, padx=10, pady=10)

        def cargar_tabla_eventos():
            for item in tabla_eventos.get_children():
                tabla_eventos.delete(item)
            for fila in backend.leer_eventos():
                tabla_eventos.insert("", tk.END, values=fila)

        def eliminar_evento_sel():
            sel = tabla_eventos.selection()
            if not sel:
                messagebox.showerror("Error", "Seleccione un evento para eliminar.", parent=ventana_bd)
                return
            indice = tabla_eventos.index(sel[0])
            backend.eliminar_evento(indice)
            cargar_tabla_eventos()
            messagebox.showinfo("Eliminado", "Registro de evento eliminado.", parent=ventana_bd)

        tk.Button(tab_eventos, text="🗑️ Eliminar Evento Seleccionado", command=eliminar_evento_sel, bg="#c0392b", fg="white").pack(pady=(0, 10))

        cargar_tabla_usuarios()
        cargar_tabla_eventos()