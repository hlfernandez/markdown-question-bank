¿Cuál de las siguientes opciones describe mejor el propósito de la función `range(3)` en Python?

- Crea una lista con los números 1, 2 y 3.
- [X] Crea un iterador que produce los números 0, 1 y 2.
- Crea una cadena de texto con los caracteres '0', '1', '2'.

---

Dado el código Python de [este anexo](#código-1), indica cuáles serían su comportamento y salida por consola:

- [X] La función invierte la cadena de caracteres.
  La salida sería: `cba`.
- La función elimina la primera letra e imprime la cadena restante.
  La salida sería: `bc`.
- La función transforma la cadena en mayúsculas.
  La salida sería: `ABC`.

---

¿Qué tipo de estructura devuelve la función `enumerate()` al aplicarse a una lista?

- [X] Un iterador de tuplas con el índice y el elemento correspondiente.
- Un diccionario donde cada clave es un índice y el valor un elemento.
- Una lista con el índice seguido del elemento.

---

¿Cuál es el resultado de `len("Python")`?

- 5
- [X] 6
- 7

---

¿Qué produce `print(2 ** 3)` en Python?

- 5
- 6
- [X] 8

---

¿Qué hace `list.append(x)`?

- Agrega el elemento `x` al inicio de la lista.
- [X] Agrega el elemento `x` al final de la lista.
- Agrega el elemento `x` ordenadamente en la lista.

---

¿Qué significa que una función sea **recursiva**?

- Que llama automáticamente a otras funciones.
- Que se ejecuta en paralelo con otras.
- [X] Que se llama a sí misma.

---

¿Qué produce `True and False`?

- True
- [X] False
- Error

---

¿Cuál es el propósito de `def` en Python?

- Declarar una clase.
- [X] Definir una función.
- Crear una variable global.

---

¿Cuándo se produce una excepción `IndexError`?

- [X] Cuando se intenta acceder a un índice fuera del rango de una lista.
- Cuando se divide por cero.
- Cuando se accede a una clave de un diccionario.

---

¿Qué tipo de dato representa `{"a": 1, "b": 2}`?

- Lista
- [X] Diccionario
- Tupla

| Dificultad  | TeachScore |
|-------------|------------|
| Baja        | 1          |

---

Considerando la asignación inicial de la variable A en la primera línea, indica el caso en el que se modifica el valor que se mostraría para la variable A después de ejecutar las otras dos instrucciones:

- 
    ```python
    A = 'Programación II'
    B = A
    B = '2025'
    ```
- [X]
    ```python
    A= ['Programación II']
    B = A
    B[0] = '2025'
    ```
- 
    ```python
    A= ['Programación II']
    B = A[:]
    B[0] = '2025'
    ```

| Dificultad  | TeachScore |
|-------------|------------|
| Alta        | 10         |

# Anexos

## Código 1

```python
def misterio(x):
    return x[::-1]

print(misterio("abc"))
```