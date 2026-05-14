
import unittest
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from deque import Deque, DequeNode
from system import UndoRedoSystem


# ===================== PRUEBAS DEL DEQUE =====================

class TestDequeCreation(unittest.TestCase):
    """Pruebas de inicialización del Deque."""

    def test_empty_deque(self):
        d = Deque()
        self.assertTrue(d.is_empty())
        self.assertEqual(d.size(), 0)

    def test_deque_repr_empty(self):
        d = Deque()
        self.assertEqual(repr(d), "Deque([])")


class TestDequeAddFront(unittest.TestCase):
    """Pruebas de add_front."""

    def test_add_front_single(self):
        d = Deque()
        d.add_front(10)
        self.assertFalse(d.is_empty())
        self.assertEqual(d.size(), 1)
        self.assertEqual(d.peek_front(), 10)
        self.assertEqual(d.peek_rear(), 10)

    def test_add_front_multiple(self):
        d = Deque()
        d.add_front(1)
        d.add_front(2)
        d.add_front(3)
        self.assertEqual(d.size(), 3)
        self.assertEqual(d.peek_front(), 3)
        self.assertEqual(d.peek_rear(), 1)

    def test_add_front_then_to_list(self):
        d = Deque()
        d.add_front("a")
        d.add_front("b")
        d.add_front("c")
        self.assertEqual(d.to_list(), ["c", "b", "a"])


class TestDequeAddRear(unittest.TestCase):
    """Pruebas de add_rear."""

    def test_add_rear_single(self):
        d = Deque()
        d.add_rear("x")
        self.assertEqual(d.size(), 1)
        self.assertEqual(d.peek_front(), "x")
        self.assertEqual(d.peek_rear(), "x")

    def test_add_rear_multiple(self):
        d = Deque()
        d.add_rear(10)
        d.add_rear(20)
        d.add_rear(30)
        self.assertEqual(d.size(), 3)
        self.assertEqual(d.peek_front(), 10)
        self.assertEqual(d.peek_rear(), 30)

    def test_add_rear_then_to_list(self):
        d = Deque()
        d.add_rear(1)
        d.add_rear(2)
        d.add_rear(3)
        self.assertEqual(d.to_list(), [1, 2, 3])


class TestDequeRemoveFront(unittest.TestCase):
    """Pruebas de remove_front."""

    def test_remove_front_single(self):
        d = Deque()
        d.add_rear(42)
        val = d.remove_front()
        self.assertEqual(val, 42)
        self.assertTrue(d.is_empty())

    def test_remove_front_multiple(self):
        d = Deque()
        for i in range(5):
            d.add_rear(i)
        self.assertEqual(d.remove_front(), 0)
        self.assertEqual(d.remove_front(), 1)
        self.assertEqual(d.size(), 3)

    def test_remove_front_empty_raises(self):
        d = Deque()
        with self.assertRaises(IndexError):
            d.remove_front()


class TestDequeRemoveRear(unittest.TestCase):
    """Pruebas de remove_rear."""

    def test_remove_rear_single(self):
        d = Deque()
        d.add_front(99)
        val = d.remove_rear()
        self.assertEqual(val, 99)
        self.assertTrue(d.is_empty())

    def test_remove_rear_multiple(self):
        d = Deque()
        for i in range(5):
            d.add_rear(i)
        self.assertEqual(d.remove_rear(), 4)
        self.assertEqual(d.remove_rear(), 3)
        self.assertEqual(d.size(), 3)

    def test_remove_rear_empty_raises(self):
        d = Deque()
        with self.assertRaises(IndexError):
            d.remove_rear()


class TestDequePeek(unittest.TestCase):
    """Pruebas de peek_front y peek_rear."""

    def test_peek_empty_raises(self):
        d = Deque()
        with self.assertRaises(IndexError):
            d.peek_front()
        with self.assertRaises(IndexError):
            d.peek_rear()

    def test_peek_after_operations(self):
        d = Deque()
        d.add_rear(1)
        d.add_rear(2)
        d.add_rear(3)
        self.assertEqual(d.peek_front(), 1)
        self.assertEqual(d.peek_rear(), 3)


class TestDequeClear(unittest.TestCase):
    """Pruebas de clear."""

    def test_clear_populated(self):
        d = Deque()
        for i in range(10):
            d.add_rear(i)
        d.clear()
        self.assertTrue(d.is_empty())
        self.assertEqual(d.size(), 0)

    def test_clear_empty(self):
        d = Deque()
        d.clear()
        self.assertTrue(d.is_empty())


class TestDequeIteration(unittest.TestCase):
    """Pruebas de iteración."""

    def test_iter_empty(self):
        d = Deque()
        items = list(d)
        self.assertEqual(items, [])

    def test_iter_with_items(self):
        d = Deque()
        d.add_rear(10)
        d.add_rear(20)
        d.add_rear(30)
        items = list(d)
        self.assertEqual(items, [10, 20, 30])


class TestDequeMixedOperations(unittest.TestCase):
    """Pruebas de operaciones mezcladas en ambos extremos."""

    def test_mixed_operations(self):
        d = Deque()
        d.add_rear(1)
        d.add_rear(2)
        d.add_front(0)
        d.add_rear(3)
        self.assertEqual(d.to_list(), [0, 1, 2, 3])

        self.assertEqual(d.remove_front(), 0)
        self.assertEqual(d.remove_rear(), 3)
        self.assertEqual(d.remove_front(), 1)
        self.assertEqual(d.remove_rear(), 2)
        self.assertTrue(d.is_empty())

    def test_len(self):
        d = Deque()
        d.add_front("a")
        d.add_front("b")
        d.add_rear("c")
        self.assertEqual(len(d), 3)
        d.remove_front()
        self.assertEqual(len(d), 2)


# ===================== PRUEBAS DEL SISTEMA UNDO/REDO =====================

class TestUndoRedoCreation(unittest.TestCase):
    """Pruebas de inicialización del sistema."""

    def test_initial_state(self):
        sys = UndoRedoSystem()
        self.assertEqual(sys.current_state, "Estado inicial")
        self.assertFalse(sys.can_undo())
        self.assertFalse(sys.can_redo())
        self.assertEqual(sys.get_undo_count(), 0)
        self.assertEqual(sys.get_redo_count(), 0)
        self.assertEqual(sys.get_history(), [])


class TestUndoRedoRegisterAction(unittest.TestCase):
    """Pruebas de registro de acciones."""

    def test_register_single_action(self):
        sys = UndoRedoSystem()
        sys.register_action("Escribir 'hola'")
        self.assertTrue(sys.can_undo())
        self.assertFalse(sys.can_redo())
        self.assertEqual(sys.current_state, "Escribir 'hola'")
        self.assertEqual(sys.get_undo_count(), 1)

    def test_register_multiple_actions(self):
        sys = UndoRedoSystem()
        sys.register_action("Acción 1")
        sys.register_action("Acción 2")
        sys.register_action("Acción 3")
        self.assertEqual(sys.get_undo_count(), 3)
        self.assertEqual(sys.current_state, "Acción 3")

    def test_register_clears_redo(self):
        """Al registrar una nueva acción después de undo, se pierde el redo."""
        sys = UndoRedoSystem()
        sys.register_action("A")
        sys.register_action("B")
        sys.undo()
        self.assertTrue(sys.can_redo())
        sys.register_action("C")
        self.assertFalse(sys.can_redo())

    def test_register_empty_raises(self):
        sys = UndoRedoSystem()
        with self.assertRaises(ValueError):
            sys.register_action("")
        with self.assertRaises(ValueError):
            sys.register_action("   ")
        with self.assertRaises(ValueError):
            sys.register_action(None)

    def test_action_content(self):
        sys = UndoRedoSystem()
        sys.register_action("Borrar línea", {"line": 5})
        history = sys.get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["name"], "Borrar línea")
        self.assertEqual(history[0]["data"], {"line": 5})
        self.assertEqual(history[0]["state_before"], "Estado inicial")


class TestUndoRedoUndo(unittest.TestCase):
    """Pruebas de la funcionalidad de undo."""

    def test_undo_single(self):
        sys = UndoRedoSystem()
        sys.register_action("Acción A")
        action = sys.undo()
        self.assertEqual(action["name"], "Acción A")
        self.assertEqual(sys.current_state, "Estado inicial")
        self.assertFalse(sys.can_undo())
        self.assertTrue(sys.can_redo())

    def test_undo_multiple(self):
        sys = UndoRedoSystem()
        sys.register_action("A")
        sys.register_action("B")
        sys.register_action("C")
        sys.undo()
        self.assertEqual(sys.current_state, "B")
        sys.undo()
        self.assertEqual(sys.current_state, "A")
        sys.undo()
        self.assertEqual(sys.current_state, "Estado inicial")
        self.assertFalse(sys.can_undo())

    def test_undo_empty_raises(self):
        sys = UndoRedoSystem()
        with self.assertRaises(IndexError):
            sys.undo()

    def test_undo_moves_to_redo(self):
        sys = UndoRedoSystem()
        sys.register_action("X")
        sys.undo()
        # La acción debe estar en redo
        redo = sys.get_redo_stack()
        self.assertEqual(len(redo), 1)
        self.assertEqual(redo[0]["name"], "X")


class TestUndoRedoRedo(unittest.TestCase):
    """Pruebas de la funcionalidad de redo."""

    def test_redo_single(self):
        sys = UndoRedoSystem()
        sys.register_action("Acción 1")
        sys.undo()
        action = sys.redo()
        self.assertEqual(action["name"], "Acción 1")
        self.assertEqual(sys.current_state, "Acción 1")
        self.assertTrue(sys.can_undo())
        self.assertFalse(sys.can_redo())

    def test_redo_multiple(self):
        sys = UndoRedoSystem()
        sys.register_action("A")
        sys.register_action("B")
        sys.register_action("C")
        sys.undo()
        sys.undo()
        sys.redo()
        self.assertEqual(sys.current_state, "B")
        sys.redo()
        self.assertEqual(sys.current_state, "C")

    def test_redo_empty_raises(self):
        sys = UndoRedoSystem()
        with self.assertRaises(IndexError):
            sys.redo()

    def test_redo_after_new_action_is_blocked(self):
        sys = UndoRedoSystem()
        sys.register_action("A")
        sys.register_action("B")
        sys.undo()
        sys.register_action("C")
        self.assertFalse(sys.can_redo())


class TestUndoRedoHistory(unittest.TestCase):
    """Pruebas del historial."""

    def test_history_order(self):
        sys = UndoRedoSystem()
        sys.register_action("Primera")
        sys.register_action("Segunda")
        sys.register_action("Tercera")
        history = sys.get_history()
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]["name"], "Primera")
        self.assertEqual(history[1]["name"], "Segunda")
        self.assertEqual(history[2]["name"], "Tercera")

    def test_history_empty_initially(self):
        sys = UndoRedoSystem()
        self.assertEqual(sys.get_history(), [])


class TestUndoRedoEdgeCases(unittest.TestCase):
    """Casos límite y validaciones."""

    def test_undo_then_redo_cycle(self):
        """Ciclo completo: registrar, undo, redo, undo."""
        sys = UndoRedoSystem()
        sys.register_action("Editar título")
        sys.undo()
        self.assertEqual(sys.current_state, "Estado inicial")
        sys.redo()
        self.assertEqual(sys.current_state, "Editar título")
        sys.undo()
        self.assertEqual(sys.current_state, "Estado inicial")

    def test_multiple_undo_past_initial(self):
        sys = UndoRedoSystem()
        sys.register_action("A")
        sys.undo()
        with self.assertRaises(IndexError):
            sys.undo()

    def test_multiple_redo_past_limit(self):
        sys = UndoRedoSystem()
        sys.register_action("A")
        sys.undo()
        sys.redo()
        with self.assertRaises(IndexError):
            sys.redo()

    def test_can_register_method(self):
        sys = UndoRedoSystem()
        self.assertTrue(sys.can_register("Nueva acción"))
        self.assertFalse(sys.can_register(""))
        self.assertFalse(sys.can_register("  "))
        self.assertFalse(sys.can_register(None))


class TestDequeNode(unittest.TestCase):
    """Pruebas del nodo del Deque."""

    def test_node_creation(self):
        n = DequeNode(42)
        self.assertEqual(n.value, 42)
        self.assertIsNone(n.next)
        self.assertIsNone(n.prev)

    def test_node_repr(self):
        n = DequeNode("test")
        self.assertEqual(repr(n), "DequeNode('test')")


if __name__ == "__main__":
    unittest.main()
