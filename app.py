import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class TablaControl(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        try:
            self.db_connection = sqlite3.connect('formularioPOP.db')
            self.cursor = self.db_connection.cursor()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo conectar a la base de datos: {e}")
            self.parent.destroy()
            return
        self.resultados = []
        self.crear_widgets()
        

    def crear_widgets(self):
        self.parent.title("Asistente de evaluación")
        self.pack(fill=tk.BOTH, expand=True)
        self.pack_propagate(False)
        
        # Configurar el ancho y alto de la ventana
        self.parent.geometry("350x600")  # Ajustado para mejor visualización
        self.parent.maxsize(width=350, height=800)
        self.parent.minsize(width=350, height=400)
        # Crear y empaquetar labelframe1 usando pack
        self.labelframe1 = tk.LabelFrame(self, text='Operaciones')
        self.labelframe1.pack(fill='x', padx=5, pady=10)
        self.operaciones()

        # Título Principal
        label_titulo = tk.Label(
            self,
            text="Requerimientos - Portal de Prestadores",
            font=("Helvetica", 16, "bold"),
            anchor="w",
            justify="left",
            wraplength=380  # Ajustado para la nueva anchura
        )
        label_titulo.pack(pady=(10, 10), fill='x', anchor='w')

        # Subtítulo
        label_subtitulo = tk.Label(
            self,
            text="Documentos requeridos:",
            font=("Helvetica", 14),
            anchor="w",
            justify="left",
            wraplength=380
        )
        label_subtitulo.pack(pady=(0, 10), fill='x', anchor='w')

        # Crear un Canvas y una barra de desplazamiento vertical
        canvas = tk.Canvas(self, width=40)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Obtener los datos de la tabla 'controles'
        try:
            self.cursor.execute("SELECT * FROM controles ORDER BY ID")
            registros = self.cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Consulta", f"No se pudieron obtener los registros: {e}")
            registros = []

        grupos = {}
        for registro in registros:
            detalle = registro[3]  # 'DETALLE' es la cuarta column
            if detalle not in grupos:
                grupos[detalle] = []
            grupos[detalle].append(registro)

        for detalle, items in grupos.items():
            
            # Frame para cada grupo de 'DETALLE'
            frame_detalle = ttk.LabelFrame(self.scrollable_frame, padding=(1, 1))
            frame_detalle.pack(fill="x", padx=5, pady=5, expand=True)
            #titulo de cada frame
            titulo_detalle = tk.Label(frame_detalle, text=detalle, wraplength=280, justify="left")
            titulo_detalle.pack(side="top", fill="x")

            for item in items:
                
                control_text = item[4]  # 'CONTROL' es la quinta columna
                respuesta = item[6]     # 'RESPUESTA' es la séptima columna
                id_control = item[0]    # Asumiendo que el ID es el primer campo

                frame_control = ttk.Frame(frame_detalle, padding=(1, 1), width=30 , height=50)
                frame_control.pack(fill="x", expand=True, pady=2)
                
                var_evaluacion = tk.BooleanVar()
                checkbox = tk.Checkbutton(
                    frame_control,
                    variable=var_evaluacion,
                    command=lambda v=var_evaluacion, r=respuesta, idc=id_control: self.toggle_resultado(v, r, idc)
                )
                checkbox.grid(row=0, column=0, sticky='w')  # Usar grid dentro de frame_control

                label_control = tk.Label(
                    frame_control,
                    text=control_text,
                    justify="left",
                    anchor="w",
                    wraplength=250,
                    width=30# Ajustado para la nueva anchura
                )
                label_control.grid(row=0, column=1, sticky='e', padx=5)

                # Configurar las columnas para que el label_control expanda correctamente
                #frame_control.grid_columnconfigure(1, weight=1)

                # Guardar referencias
                self.resultados.append({
                    'id': id_control,
                    'var': var_evaluacion,
                    'text': None,          # Inicialmente no hay Text widget
                    'frame_text': None,    # Para guardar referencia al frame_text
                    'respuesta': respuesta,
                    'frame_control': frame_control
                })

    def operaciones(self):
        # Botón "Fijar" para mantener la ventana siempre arriba
        boton_fijar = tk.Button(self.labelframe1, text="FIJAR", command=self.toggle_always_on_top)
        boton_fijar.grid(column=0, row=0, padx=5, pady=5 )

        # Botón para generar informe
        boton_informe = tk.Button(self.labelframe1, text="INFORME", command=self.generar_informe)
        boton_informe.grid(column=1, row=0, pady=5, padx=5, sticky='nw')  # Reemplazar 'anchor' por 'sticky'

        # Botón para restaurar valores
        boton_restaurar = tk.Button(self.labelframe1, text="LIMPIAR", command=self.restaurar_valores)
        boton_restaurar.grid(column=2, row=0, pady=5, padx=5)

    def toggle_always_on_top(self):
        # Alternar el atributo 'always on top'
        current = self.parent.attributes("-topmost")
        self.parent.attributes("-topmost", not current)

    def toggle_resultado(self, var, respuesta, idc):
        for res in self.resultados:
            if res['var'] == var and res['id'] == idc:
                if var.get():
                    # Crear frame_text y text_resultado si no existen
                    if res['frame_text'] is None:
                        frame_text = ttk.Frame(res['frame_control'], padding=(5, 5))
                        frame_text.grid(row=1, column=1, sticky='w', pady=2)  

                        text_resultado = tk.Text(
                            frame_text,
                            height=3,
                            wrap=tk.WORD,
                            width=37
                        )
                        text_resultado.pack(fill="both", expand=True, padx=5, pady=5)
                        text_resultado.insert(tk.END, respuesta)
                        text_resultado.bind("<KeyRelease>", self.limit_text_length)

                        res['text'] = text_resultado
                        res['frame_text'] = frame_text
                    else:
                        # Si ya existe, simplemente mostrarlo
                        res['frame_text'].grid(row=1, column=1, sticky='w', pady=2, padx=25)
                else:
                    # Ocultar y destruir el frame_text si existe
                    if res['frame_text'] is not None:
                        res['frame_text'].grid_forget()
                        res['frame_text'].destroy()
                        res['frame_text'] = None
                        res['text'] = None
                break  # Salir del loop una vez encontrado
    def restaurar_valores(self):
  
        for res in self.resultados:
            # Desmarcar el checkbox
            res['var'].set(False)
            
            # Si el Text widget existe, destruirlo
            if res['frame_text'] is not None:
                res['frame_text'].grid_forget()
                res['frame_text'].destroy()
                res['frame_text'] = None
                res['text'] = None

        # Actualizar la interfaz
        self.parent.update_idletasks()
        
    def limit_text_length(self, event):
        """Limitar el ancho del Text widget para que no exceda el ancho máximo."""
        widget = event.widget
        max_chars = 250  # Ajusta según la relación entre caracteres y píxeles
        current_text = widget.get("1.0", tk.END)
        if len(current_text) > max_chars:
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, current_text[:max_chars])

    def generar_informe(self):
        # Solicitar al usuario la ubicación para guardar el PDF
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar Informe Como"
        )
        if not file_path:
            return  # El usuario canceló la operación

        # Crear el documento PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título del informe
        story.append(Paragraph("Informe de Evaluación", styles['Title']))
        story.append(Spacer(1, 12))

        # Iterar sobre los resultados y agregar al PDF
        for res in self.resultados:
            if res['var'].get():
                resultado = res['text'].get('1.0', tk.END).strip() if res['text'] else ""
                if resultado:
                    # Agregar cada resultado como un párrafo
                    story.append(Paragraph(resultado, styles['Normal']))
                    story.append(Spacer(1, 12))

        try:
            # Construir el PDF
            doc.build(story)
            messagebox.showinfo("Informe", "El informe ha sido generado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el informe: {e}")

    def destroy(self):
        # Cerrar la conexión a la base de datos antes de destruir el frame
        self.db_connection.close()
        super().destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TablaControl(root)
    app.pack(fill="both", expand=True)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()