# tarea-5
# Sistema de Edición con Undo/Redo

## Descripción

Aplicación en Python que simula un sistema de edición con funcionalidades de **undo** y **redo**, implementado con una estructura de datos **Deque** propia (cola de doble extremo).

## Arquitectura

El proyecto sigue una separación clara de responsabilidades:

```
┌─────────────────────────────────┐
│          ui.py (Interfaz)       │  ← Tkinter, solo consume las clases
├─────────────────────────────────┤
│    system.py (Lógica)           │  ← UndoRedoSystem, encapsula undo/redo
├─────────────────────────────────┤
│     deque.py (Estructura)       │  ← Deque propia con nodos enlazados
└─────────────────────────────────┘
```

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `deque.py` | Implementación propia de Deque con nodos doblemente enlazados. Operaciones O(1): `add_front`, `add_rear`, `remove_front`, `remove_rear`, `is_empty`, `size`, `clear`, `peek_front`, `peek_rear`, `to_list`. |
| `system.py` | Clase `UndoRedoSystem` que usa dos Deques (undo_stack y redo_stack) para gestionar el historial. Permite registrar, deshacer y rehacer acciones. |
| `ui.py` | Interfaz gráfica con Tkinter. Consume `UndoRedoSystem` sin mezclar lógica. Incluye campo de texto, botones y atajos de teclado (Ctrl+Z, Ctrl+Y). |
| `main.py` | Punto de entrada de la aplicación. |
| `tests.py` | Pruebas unitarias con `unittest`: pruebas del Deque, undo, redo, casos límite. |
| `README.md` | Este archivo. |

## Cómo usar

```bash
# Ejecutar la aplicación
python main.py

# Ejecutar las pruebas
python -m unittest tests -v
```

## Funcionalidades

- **Registrar acción**: Escribe un nombre de acción y presiona "Agregar" o Enter.
- **Undo (Ctrl+Z)**: Deshace la última acción realizada.
- **Redo (Ctrl+Y)**: Rehace la última acción deshecha.
- **Mostrar historial**: Muestra todas las acciones en el panel inferior.
- **Mostrar estado actual**: Muestra el estado actual en un diálogo.
- **Limpiar todo**: Reinicia el sistema.

## Decisiones de diseño

### ¿Por qué Deque?

El Deque es ideal para undo/redo porque necesitamos operaciones eficientes en ambos extremos:
- **undo**: remover del final del historial (remove_rear)
- **redo**: remover del final del redo stack (remove_rear)
- **registrar**: agregar al historial (add_rear)

Todas estas operaciones son **O(1)** con nodos doblemente enlazados.

### ¿Por qué dos pilas (Deques)?

Se usan dos Deques separados:
1. **undo_stack**: almacena todas las acciones realizadas (el más reciente está al rear)
2. **redo_stack**: almacena las acciones que se deshicieron por undo

Cuando se registra una nueva acción, el redo_stack se limpia (comportamiento estándar de editores).

### Implementación interna del Deque

Aunque se usa una lista enlazada internamente, el acceso está encapsulado estrictamente a través de la interfaz del Deque (add_front, add_rear, remove_front, remove_rear), sin exponer los nodos internos.

### Validaciones implementadas

- No se puede registrar una acción vacía o inválida (`ValueError`)
- No se puede hacer undo cuando no hay acciones (`IndexError`)
- No se puede hacer redo cuando no hay acciones disponibles (`IndexError`)
- Los botones se deshabilitan dinámicamente según el estado del sistema
- Límite de historial configurable (por defecto 50 acciones)

## Requisitos

- Python 3.12+ (funciona con versiones anteriores también)
- Sin dependencias externas (solo usa `tkinter` y `unittest`, ambos incluidos en la biblioteca estándar)
