
import tkinter as tk
from tkinter import ttk, messagebox
from system import UndoRedoSystem


class UndoRedoApp:
    """Aplicación gráfica que consume UndoRedoSystem."""

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Edición - Undo / Redo")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.engine = UndoRedoSystem()

        self._build_ui()
        self._refresh_display()

    # ---- Construcción de la interfaz ----

    def _build_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", font=("Consolas", 12))
        style.configure("Info.TLabel", font=("Segoe UI", 10))
        style.configure("Accion.TButton", font=("Segoe UI", 11))

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(
            main_frame, text="✏️ Sistema de Edición - Undo / Redo",
            style="Title.TLabel"
        ).pack(pady=(0, 15))

        # Estado actual
        state_frame = ttk.LabelFrame(main_frame, text="Estado Actual", padding=10)
        state_frame.pack(fill=tk.X, pady=(0, 10))

        self.state_label = ttk.Label(
            state_frame, text="", style="Status.TLabel",
            foreground="#2c3e50", wraplength=600
        )
        self.state_label.pack()

        # Contadores
        counters_frame = ttk.Frame(main_frame)
        counters_frame.pack(fill=tk.X, pady=(0, 10))

        self.lbl_undo_count = ttk.Label(counters_frame, text="Undo: 0", style="Info.TLabel")
        self.lbl_undo_count.pack(side=tk.LEFT, padx=(0, 20))

        self.lbl_redo_count = ttk.Label(counters_frame, text="Redo: 0", style="Info.TLabel")
        self.lbl_redo_count.pack(side=tk.LEFT)

        # Entrada de nueva acción
        input_frame = ttk.LabelFrame(main_frame, text="Registrar Nueva Acción", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        self.action_entry = ttk.Entry(input_frame, font=("Segoe UI", 12), width=40)
        self.action_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=3)
        self.action_entry.bind("<Return>", lambda e: self._on_add_action())

        btn_add = ttk.Button(
            input_frame, text="Agregar Acción",
            command=self._on_add_action, style="Accion.TButton"
        )
        btn_add.pack(side=tk.LEFT)

        # Botones principales
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.btn_undo = ttk.Button(
            btn_frame, text="⬅ Undo (Ctrl+Z)",
            command=self._on_undo, style="Accion.TButton", width=20
        )
        self.btn_undo.pack(side=tk.LEFT, padx=5)

        self.btn_redo = ttk.Button(
            btn_frame, text="Redo (Ctrl+Y) ➜",
            command=self._on_redo, style="Accion.TButton", width=20
        )
        self.btn_redo.pack(side=tk.LEFT, padx=5)

        # Botones auxiliares
        btn_aux_frame = ttk.Frame(main_frame)
        btn_aux_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(
            btn_aux_frame, text="Mostrar Historial",
            command=self._on_show_history
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_aux_frame, text="Mostrar Estado Actual",
            command=self._on_show_state
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_aux_frame, text="Limpiar Todo",
            command=self._on_clear, style="Accion.TButton"
        ).pack(side=tk.LEFT, padx=5)

        # Textbox de historial
        history_frame = ttk.LabelFrame(main_frame, text="Historial de Acciones", padding=5)
        history_frame.pack(fill=tk.BOTH, expand=True)

        self.history_text = tk.Text(
            history_frame, font=("Consolas", 10),
            height=10, state=tk.DISABLED, bg="#1e1e2e", fg="#cdd6f4",
            insertbackground="white", wrap=tk.WORD, relief=tk.FLAT
        )
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.pack(fill=tk.BOTH, expand=True)

        # Atajos de teclado
        self.root.bind("<Control-z>", lambda e: self._on_undo())
        self.root.bind("<Control-y>", lambda e: self._on_redo())

    # ---- Lógica de interacción ----

    def _on_add_action(self):
        """Maneja la acción de agregar una nueva acción desde la entrada."""
        text = self.action_entry.get().strip()
        try:
            self.engine.register_action(text)
            self.action_entry.delete(0, tk.END)
            self._refresh_display()
        except ValueError as e:
            messagebox.showwarning("Acción inválida", str(e))

    def _on_undo(self):
        """Maneja la acción de undo."""
        try:
            action = self.engine.undo()
            self._refresh_display()
        except IndexError:
            messagebox.showinfo("Undo", "No hay acciones para deshacer.")

    def _on_redo(self):
        """Maneja la acción de redo."""
        try:
            action = self.engine.redo()
            self._refresh_display()
        except IndexError:
            messagebox.showinfo("Redo", "No hay acciones para rehacer.")

    def _on_show_history(self):
        """Muestra el historial completo en el textbox."""
        history = self.engine.get_history()
        redo_items = self.engine.get_redo_stack()

        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete("1.0", tk.END)

        self.history_text.insert(tk.END, "═══ HISTORIAL DE ACCIONES ═══\n\n", "title")

        if not history:
            self.history_text.insert(tk.END, "  (vacío)\n", "dim")
        else:
            for i, action in enumerate(history, 1):
                state_before = action.get("state_before", "—")
                self.history_text.insert(
                    tk.END,
                    f"  {i}. {action['name']}  [desde: {state_before}]\n",
                    "normal"
                )

        if redo_items:
            self.history_text.insert(tk.END, "\n═══ ACCIONES DISPONIBLES PARA REDO ═══\n\n", "title")
            for i, action in enumerate(redo_items, 1):
                self.history_text.insert(
                    tk.END,
                    f"  {i}. {action['name']}\n",
                    "redo"
                )

        self.history_text.config(state=tk.DISABLED)

    def _on_show_state(self):
        """Muestra el estado actual en una ventana emergente."""
        state = self.engine.current_state
        messagebox.showinfo(
            "Estado Actual",
            f"Estado actual del sistema:\n\n{state}"
        )

    def _on_clear(self):
        """Limpia todo el sistema."""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el historial?"):
            self.engine = UndoRedoSystem()
            self._refresh_display()

    # ---- Actualización de la UI ----

    def _refresh_display(self):
        """Actualiza todos los elementos de la interfaz."""
        # Estado actual
        self.state_label.config(text=self.engine.current_state)

        # Contadores
        self.lbl_undo_count.config(text=f"Undo disponibles: {self.engine.get_undo_count()}")
        self.lbl_redo_count.config(text=f"Redo disponibles: {self.engine.get_redo_count()}")

        # Habilitar/deshabilitar botones
        self.btn_undo.config(state=tk.NORMAL if self.engine.can_undo() else tk.DISABLED)
        self.btn_redo.config(state=tk.NORMAL if self.engine.can_redo() else tk.DISABLED)

        # Actualizar historial visual
        self._on_show_history()
