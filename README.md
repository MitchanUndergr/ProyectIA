El estado del juego se representa mediante una matriz en la que cada celda puede estar en uno de varios estados:

Celda no revelada: Representada por un valor oculto o un símbolo que indica que la celda aún no ha sido seleccionada por el jugador.
Celda revelada con número: Indica que la celda ha sido seleccionada y que contiene el número de minas adyacentes a esa celda.
Celda revelada vacía: Indica que la celda ha sido seleccionada y que no tiene minas adyacentes.
Celda marcada con bandera: Indica que el jugador ha marcado la celda como una posible ubicación de una mina.

La estructura de datos que representa el estado del juego es la clase Buscaminas. Esta clase tiene atributos que representan el tablero del juego, incluyendo la ubicación de las minas, el estado de cada celda (revelada o no revelada), y las minas que han sido encontradas por el jugador.

El agente en el juego de buscaminas tiene un espacio de acciones discreto, ya que las acciones posibles que puede tomar el agente son seleccionar una celda para revelarla o marcar una celda como una posible mina
