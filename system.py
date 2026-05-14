"""
Core system logic for undo/redo functionality.
Uses the custom Deque class to manage action history.

Design decisions:
- 'undo_stack' stores all past actions (most recent at rear for efficient removal)
- 'redo_stack' stores actions that were undone (can be re-applied)
- Performing a new action clears the redo stack (standard undo/redo behavior)
- Each action is a dict with 'name' and optional 'data' for display purposes

Autor: Kilo
"""

from deque import Deque


class UndoRedoSystem:
    """
    Sistema central de gestión de historial con undo/redo.

    Utiliza dos instancias de Deque:
    - undo_stack: acciones realizadas que se pueden deshacer
    - redo_stack: acciones deshechas que se pueden rehacer
    """

    def __init__(self):
        self.undo_stack = Deque()
        self.redo_stack = Deque()
        self._current_state = "Estado inicial"
        self._max_history = 50  # límite para evitar uso excesivo de memoria

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        if not isinstance(value, str):
            raise ValueError("El estado debe ser una cadena de texto")
        if not value.strip():
            raise ValueError("El estado no puede estar vacío")
        self._current_state = value

    def register_action(self, action_name, data=None):
        """
        Registra una nueva acción en el historial.

        Args:
            action_name: Nombre descriptivo de la acción
            data: Datos opcionales asociados a la acción

        Raises:
            ValueError: Si action_name está vacío o no es válido
        """
        if not action_name or not isinstance(action_name, str) or not action_name.strip():
            raise ValueError("El nombre de la acción no puede estar vacío")

        action = {
            "name": action_name.strip(),
            "data": data,
            "state_before": self._current_state
        }

        # Al registrar una nueva acción, se limpia el redo stack
        self.redo_stack.clear()

        # Agregar al historial (por el rear para mantener orden cronológico)
        self.undo_stack.add_rear(action)

        # Aplicar la acción al estado actual
        self._current_state = action_name

        # Respetar el límite de historial
        if self.undo_stack.size() > self._max_history:
            self.undo_stack.remove_front()

    def undo(self):
        """
        Deshace la última acción realizada.

        Returns:
            dict: La acción que fue deshecha

        Raises:
            IndexError: Si no hay acciones para deshacer
        """
        if self.undo_stack.is_empty():
            raise IndexError("No hay acciones para deshacer")

        # Obtener la última acción (del rear)
        action = self.undo_stack.remove_rear()

        # Guardar en redo stack para poder rehacer
        self.redo_stack.add_rear(action)

        # Restaurar estado anterior
        prev_state = action.get("state_before", "Estado inicial")
        self._current_state = prev_state

        return action

    def redo(self):
        """
        Rehace la última acción deshecha.

        Returns:
            dict: La acción que fue rehecha

        Raises:
            IndexError: Si no hay acciones para rehacer
        """
        if self.redo_stack.is_empty():
            raise IndexError("No hay acciones para rehacer")

        # Obtener la última acción deshecha
        action = self.redo_stack.remove_rear()

        # Re-aplicar la acción
        self.undo_stack.add_rear(action)
        self._current_state = action["name"]

        return action

    def get_history(self):
        """Retorna el historial completo de acciones."""
        return self.undo_stack.to_list()

    def get_redo_stack(self):
        """Retorna las acciones disponibles para redo."""
        return self.redo_stack.to_list()

    def can_undo(self):
        """Retorna True si hay acciones para deshacer."""
        return not self.undo_stack.is_empty()

    def can_redo(self):
        """Retorna True si hay acciones para rehacer."""
        return not self.redo_stack.is_empty()

    def get_undo_count(self):
        """Cantidad de acciones disponibles para undo."""
        return self.undo_stack.size()

    def get_redo_count(self):
        """Cantidad de acciones disponibles para redo."""
        return self.redo_stack.size()

    def can_register(self, action_name):
        """Verifica si una acción es válida para registrar."""
        return bool(action_name and isinstance(action_name, str) and action_name.strip())