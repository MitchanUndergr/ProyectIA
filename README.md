# Estado del Juego del Buscaminas

Cada celda en el tablero del juego de Buscaminas puede encontrarse en uno de los siguientes estados:

| Estado de la Celda          | Descripción                                                                                   | Representación      |
|-----------------------------|-----------------------------------------------------------------------------------------------|---------------------|
| Celda no revelada           | La celda no ha sido seleccionada por el jugador. Su contenido es desconocido.                 | `?` o un símbolo específico |
| Celda revelada con número   | La celda ha sido seleccionada y muestra el número de minas adyacentes.                        | `1` a `8`           |
| Celda revelada vacía        | La celda ha sido seleccionada y no tiene minas adyacentes. Sus vecinas se revelan automáticamente. | `0` o un espacio vacío     |
| Celda marcada con bandera   | El jugador ha marcado la celda como una posible ubicación de una mina.                        | `F` o un símbolo de bandera  |

La clase `Buscaminas` encapsula la lógica y el estado actual del juego. Los atributos principales de esta clase incluyen:

- `tablero`: Matriz que representa el estado de cada celda del juego.
- `minas`: Ubicación de las minas en el tablero.
- `estado_celda`: Matriz paralela que indica si una celda está revelada, es una bandera o está oculta.
- `minas_encontradas`: Contador de las minas que han sido correctamente identificadas por el jugador.

## Acciones del Agente en el Buscaminas
El agente en el juego de buscaminas tiene un espacio de acciones discreto, ya que las acciones posibles que puede tomar el agente son seleccionar una celda para revelarla o marcar una celda como una posible mina
El agente puede realizar dos tipos de acciones, cada una modificando el estado del tablero:

1. **Revelar celda**: El agente selecciona una celda oculta para revelarla. Si la celda contiene una mina, el juego termina. Si es una celda vacía, se revelan también las celdas adyacentes.
2. **Marcar con bandera**: El agente coloca una bandera en una celda que considera contiene una mina para evitar seleccionarla en el futuro.

El objetivo del agente es revelar todas las celdas que no contienen minas sin detonar ninguna de ellas.


# Características del Ambiente en el Juego del Buscaminas

| Característica            | Descripción en Buscaminas | Estado en Buscaminas |
|---------------------------|---------------------------|----------------------|
| Observable                | Parcialmente observable, ya que solo se conocen las celdas reveladas. | Parcialmente |
| Determinista              | No determinista, debido a que la ubicación de las minas es aleatoria y desconocida. | No |
| Episódico                 | No episódico, ya que las acciones previas afectan el futuro del juego. | No |
| Estático                  | Estático, porque el ambiente no cambia mientras el agente está "pensando". | Sí |
| Discreto                  | Discreto, debido a que el ambiente es una cuadrícula con estados claramente definidos. | Sí |
| Multi-Agente              | Un solo jugador, por lo tanto, no es multi-agente en el modo clásico. | No |


