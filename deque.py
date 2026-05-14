"""
Custom Deque implementation using a doubly-linked list.
All operations are O(1). The internal storage uses a Python list
but all access is strictly through the deque interface.

Autor: Kilo
"""


class DequeNode:
    """Nodo individual del Deque."""

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return f"DequeNode({self.value!r})"


class Deque:
    """
    Implementación propia de Deque (cola de doble extremo).
    Soporta operaciones O(1) en ambos extremos.

    Uso interno: almacenar el historial de acciones para undo/redo.
    """

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def add_front(self, item):
        """Agrega un elemento al frente del deque. O(1)."""
        new_node = DequeNode(item)
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            new_node.next = self._head
            self._head.prev = new_node
            self._head = new_node
        self._size += 1

    def add_rear(self, item):
        """Agrega un elemento al final del deque. O(1)."""
        new_node = DequeNode(item)
        if self.is_empty():
            self._head = self._tail = new_node
        else:
            new_node.prev = self._tail
            self._tail.next = new_node
            self._tail = new_node
        self._size += 1

    def remove_front(self):
        """
        Remueve y retorna el elemento del frente del deque.
        Lanza IndexError si está vacío. O(1).
        """
        if self.is_empty():
            raise IndexError("remove_front de Deque vacío")
        value = self._head.value
        if self._head is self._tail:
            self._head = self._tail = None
        else:
            self._head = self._head.next
            self._head.prev = None
        self._size -= 1
        return value

    def remove_rear(self):
        """
        Remueve y retorna el elemento del final del deque.
        Lanza IndexError si está vacío. O(1).
        """
        if self.is_empty():
            raise IndexError("remove_rear de Deque vacío")
        value = self._tail.value
        if self._head is self._tail:
            self._head = self._tail = None
        else:
            self._tail = self._tail.prev
            self._tail.next = None
        self._size -= 1
        return value

    def peek_front(self):
        """Retorna el elemento del frente sin removerlo."""
        if self.is_empty():
            raise IndexError("peek_front de Deque vacío")
        return self._head.value

    def peek_rear(self):
        """Retorna el elemento del final sin removerlo."""
        if self.is_empty():
            raise IndexError("peek_rear de Deque vacío")
        return self._tail.value

    def is_empty(self):
        """Retorna True si el deque está vacío. O(1)."""
        return self._size == 0

    def size(self):
        """Retorna la cantidad de elementos. O(1)."""
        return self._size

    def clear(self):
        """Vacía completamente el deque. O(1)."""
        self._head = None
        self._tail = None
        self._size = 0

    def to_list(self):
        """Retorna una lista con todos los elementos de izquierda a derecha."""
        result = []
        current = self._head
        while current:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self):
        return self._size

    def __iter__(self):
        current = self._head
        while current:
            yield current.value
            current = current.next

    def __repr__(self):
        return f"Deque({self.to_list()})"