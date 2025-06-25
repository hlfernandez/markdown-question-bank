Cal destas opcións describe mellor o propósito da función `range(3)` en Python?

- Crea unha lista cos números 1, 2 e 3.
- [X] Crea un iterador que produce os números 0, 1 e 2.
- Crea unha cadea de texto cos caracteres '0', '1', '2'.

---

Dado o código Python de [este anexo](#código-1), indica cales serían o seu comportamento e saída por consola:

- [X] A función inverte a cadea de caracteres.
  A saída sería: `cba`.
- A función elimina a primeira letra e imprime a cadea restante.
  A saída sería: `bc`.
- A función transforma a cadea en maiúsculas.
  A saída sería: `ABC`.

---

Que tipo de estrutura devolve a función `enumerate()` cando se aplica a unha lista?

- [X] Un iterador de tuplas co índice e o elemento correspondente.
- Un dicionario onde cada clave é un índice e o valor un elemento.
- Unha lista co índice seguido do elemento.

---

Cal é o resultado de `len("Python")`?

- 5
- [X] 6
- 7

---

Que produce `print(2 ** 3)` en Python?

- 5
- 6
- [X] 8

---

Que fai `list.append(x)`?

- Engade o elemento `x` ao comezo da lista.
- [X] Engade o elemento `x` ao final da lista.
- Engade o elemento `x` ordenadamente na lista.

---

Que significa que unha función sexa **recursiva**?

- Que chama a outras funcións automaticamente.
- Que se executa en paralelo con outras.
- [X] Que se chama a si mesma.

---

Que produce `True and False`?

- True
- [X] False
- Error

---

Cal é a finalidade de `def` en Python?

- Declarar unha clase.
- [X] Definir unha función.
- Crear unha variable global.

---

Cando se produce unha excepción `IndexError`?

- [X] Cando se tenta acceder a un índice fóra do rango dunha lista.
- Cando se divide por cero.
- Cando se accede a unha clave dun dicionario.

---

Que tipo de dato representa `{"a": 1, "b": 2}`?

- Lista
- [X] Dicionario
- Tupla

| Dificultade | TeachScore |
|-------------|------------|
| Baixa       | 1          |

---

Considerando a asignación inicial da variable A na primeira liña, indica o caso en que se modifica o valor que se mostraría para a variable A despois de executar as outras dúas instrucións:

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


| Dificultade | TeachScore |
|-------------|------------|
| Alta        | 10         |

---

Que fai `"  texto  ".strip()`?

- [X] Elimina os espazos ao principio e ao final.
- Elimina todos os espazos.
- Convirte a maiúsculas.

# Anexos

## Código 1

```python
def misterio(x):
    return x[::-1]

print(misterio("abc"))
```