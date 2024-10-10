import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

class TablaControl(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.db_connection = sqlite3.connect('formularioPOP.db')
        self.cursor = self.db_connection.cursor()
        self.resultados = []
        self.crear_widgets()

    def crear_widgets(self):
        self.parent.title("Asistente de evaluación")
        self.pack(fill=tk.BOTH, expand=True)

        # Botón "Fijar" para mantener la ventana siempre arriba
        boton_fijar = tk.Button(self, text="Fijar", command=self.toggle_always_on_top)
        boton_fijar.pack(pady=10, padx=10, anchor='nw')

        # Botón para generar informe
        boton_informe = tk.Button(self, text="GENERAR INFORME", command=self.generar_informe)
        boton_informe.pack(pady=10, padx=10, anchor='nw')

        # Título Principal
        label_titulo = tk.Label(self, text="Requerimientos - Portal de Prestadores", font=("Helvetica", 14, "bold"), anchor="w", justify="left")
        label_titulo.pack(
            pady=(0, 20),
            fill='x',             
            anchor='w')

        # Subtítulo
        label_subtitulo = tk.Label(self, text="Lista:", font=("Helvetica", 12), anchor="w", justify="left")
        label_subtitulo.pack(
            pady=(0, 20),
            fill='x',             
            anchor='w')


        # Crear un Canvas y una barra de desplazamiento vertical
        canvas = tk.Canvas(self)
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
        self.cursor.execute("SELECT * FROM controles ORDER BY ID")
        registros = self.cursor.fetchall()

        grupos = {}
        for registro in registros:
            detalle = registro[3]  # 'DETALLE' es la cuarta columna
            if detalle not in grupos:
                grupos[detalle] = []
            grupos[detalle].append(registro)

        for detalle, items in grupos.items():
            # Frame para cada grupo de 'DETALLE'
            frame_detalle = ttk.LabelFrame(self.scrollable_frame, text=detalle, padding=(10, 5))
            frame_detalle.pack(fill="x", padx=10, pady=5, expand=True)

            for item in items:
                control_text = item[4]  # 'CONTROL' es la quinta columna
                id_resp = item[0]       # 'ID' es la primera columna
                respuesta = item[6]     # 'RESPUESTA' es la séptima columna

                frame_control = ttk.Frame(frame_detalle)
                frame_control.pack(fill="x", pady=2)

                # Label con wraplength dinámico

                var_evaluacion = tk.BooleanVar()
                checkbox = tk.Checkbutton(frame_control, variable=var_evaluacion, command=lambda v=var_evaluacion, r=respuesta: self.toggle_resultado(v, r))
                checkbox.pack(side="left")

                label_control = tk.Label(frame_control, text=control_text, wraplength=150, justify="left")
                label_control.pack(side="left", fill="x", expand=True, padx=(0,10))

                # Text para 'RESULTADO'
                frame_text = ttk.Frame(frame_control)
                frame_text.pack(side="left", padx=10, expand=True)

                text_resultado = tk.Text(frame_text, height=2, width=100, wrap=tk.WORD)
                text_resultado.pack(side="right", fill="both", expand=True)

                # (Opcional) Agregar scrollbar interna al Text widget
                # scroll_text = ttk.Scrollbar(frame_text, orient="vertical", command=text_resultado.yview)
                # scroll_text.pack(side="right", fill="y")
                # text_resultado.config(yscrollcommand=scroll_text.set)

                text_resultado.config(state='disabled')

                # Guardar referencias
                self.resultados.append({'var': var_evaluacion, 'text': text_resultado, 'respuesta': respuesta})

        

        # Vincular el evento de redimensionamiento para ajustar wraplength
        self.parent.bind("<Configure>", self.on_resize)

    def toggle_always_on_top(self):
        # Alternar el atributo 'always on top'
        current = self.parent.attributes("-topmost")
        self.parent.attributes("-topmost", not current)

    def toggle_resultado(self, var, respuesta):
        for res in self.resultados:
            if res['var'] == var:
                if var.get():
                    res['text'].config(state='normal')
                    res['text'].delete('1.0', tk.END)
                    res['text'].insert(tk.END, respuesta)
                else:
                    res['text'].delete('1.0', tk.END)
                    res['text'].config(state='disabled')

    def generar_informe(self):
        # Crear el documento PDF
        doc = SimpleDocTemplate("informe.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título del informe
        story.append(Paragraph("Informe de Evaluación", styles['Title']))
        story.append(Spacer(1, 12))

        # Iterar sobre los resultados y agregar al PDF
        for res in self.resultados:
            if res['var'].get():
                resultado = res['text'].get('1.0', tk.END).strip()
                if resultado:
                    # Agregar cada resultado como un párrafo
                    story.append(Paragraph(resultado, styles['Normal']))
                    story.append(Spacer(1, 12))

        # Construir el PDF
        doc.build(story)
        messagebox.showinfo("Informe", "El informe ha sido generado exitosamente.")

    def on_resize(self, event):
        # Ajustar el wraplength de los labels según el ancho de la ventana
        new_width = self.parent.winfo_width()
        wrap_length = new_width - 200  # Ajusta el valor según la disposición de los widgets
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ttk.LabelFrame):
                for subwidget in widget.winfo_children():
                    if isinstance(subwidget, ttk.Frame):
                        for control_widget in subwidget.winfo_children():
                            if isinstance(control_widget, tk.Label):
                                control_widget.config(wraplength=wrap_length)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x800")  # Tamaño inicial de la ventana
    app = TablaControl(root)
    app.pack(fill="both", expand=True)
    root.mainloop()

