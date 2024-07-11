import random
import heapq

class Buscaminas():
    """
    Representación del juego Buscaminas
    """

    def __init__(self, alto=8, ancho=8, minas=8):

        # Establecer el alto, ancho y número inicial de minas
        self.alto = alto
        self.ancho = ancho
        self.minas = set()

        # Inicializar un campo vacío sin minas
        self.tablero = []
        for i in range(self.alto):
            fila = []
            for j in range(self.ancho):
                fila.append(False)
            self.tablero.append(fila)

        # Añadir minas de forma aleatoria
        while len(self.minas) != minas:
            i = random.randrange(alto)
            j = random.randrange(ancho)
            if not self.tablero[i][j]:
                self.minas.add((i, j))
                self.tablero[i][j] = True

        # Al principio, el jugador no ha encontrado minas
        self.minas_encontradas = set()

    def imprimir(self):
     """
     Imprime una representación en texto
     de dónde están ubicadas las minas.
     """
     for i in range(self.alto):
         print("--" * self.ancho + "-")
         for j in range(self.ancho):
             if self.tablero[i][j]:
                 print("|X", end="")
             else:
                 print("| ", end="")
         print("|")
     print("--" * self.ancho + "-")

   
    def es_mina(self, celda):
        i, j = celda
        return self.tablero[i][j]

    def minas_cercanas(self, celda):
        """
        Devuelve el número de minas que están
        dentro de una fila y columna de una celda dada,
        sin incluir la celda misma.
        """

        # Mantener un conteo de minas cercanas
        conteo = 0

        # Recorrer todas las celdas dentro de una fila y columna
        for i in range(celda[0] - 1, celda[0] + 2):
            for j in range(celda[1] - 1, celda[1] + 2):

                # Ignorar la celda misma
                if (i, j) == celda:
                    continue

                # Actualizar conteo si la celda está dentro de los límites y es una mina
                if 0 <= i < self.alto and 0 <= j < self.ancho:
                    if self.tablero[i][j]:
                        conteo += 1

        return conteo

    def ganaste(self):
        """
        Comprueba si todas las minas han sido marcadas.
        """
        return self.minas_encontradas == self.minas

class BusquedaBuscaminas():
    def __init__(self, ia, seguras, movimientos_realizados, conocimiento, alto, ancho):
        self.ia = ia
        self.seguras = seguras
        self.movimientos_realizados = movimientos_realizados
        self.conocimiento = conocimiento
        self.alto = alto
        self.ancho = ancho
        
    def hacer_movimiento_seguro_aleatorio(self):
        """
        Devuelve una celda segura para elegir en el tablero de Buscaminas.
        El movimiento debe ser conocido como seguro y no debe ser un movimiento
        que ya se haya realizado.

        Esta función puede usar el conocimiento en self.minas, self.seguras
        y self.movimientos_realizados, pero no debe modificar ninguno de esos valores.
        """
        celdas_seguras = self.seguras - self.movimientos_realizados
        if not celdas_seguras:
            return None
        # print(f"Pool: {celdas_seguras}")
        movimiento = celdas_seguras.pop()
        return movimiento

    def hacer_movimiento_seguro_estrella(self):
        """
        Devuelve una celda segura para elegir en el tablero de Buscaminas utilizando A*.
        """
        celdas_seguras = self.ia.seguras - self.ia.movimientos_realizados
        if not celdas_seguras:
            return None
        return self.a_estrella(celdas_seguras)

    def a_estrella(self, celdas_seguras):
        # Utilizar una cola de prioridad para implementar A*
        heap = []
        starting_cell = random.choice(tuple(celdas_seguras))
        heapq.heappush(heap, (0 + self.heuristica(starting_cell), 0, starting_cell))  # (F cost, G cost, cell)
    
        while heap:
            f_cost, g_cost, celda = heapq.heappop(heap)
            if celda not in self.ia.movimientos_realizados:
                return celda  # Found the next cell to reveal
    
            for vecino in self.ia.obtener_vecinos_celda(celda):
                if vecino not in self.ia.movimientos_realizados:
                    new_g_cost = g_cost + 1  # Assuming uniform cost for simplicity
                    new_f_cost = new_g_cost + self.heuristica(vecino)
                    heapq.heappush(heap, (new_f_cost, new_g_cost, vecino))

        return None
    
    def hacer_movimiento_seguro_heuristicas(self):
        celdas_seguras = self.ia.seguras - self.ia.movimientos_realizados
        if not celdas_seguras:
            return None
        return self.heuristica(celdas_seguras)
    
    def heuristica(self, celdas_seguras):
        heap = []
        heapq.heappush(heap, (0, random.choice(tuple(celdas_seguras))))  # Tupla de (costo acumulado, celda)
        # Initialize the heap
        while heap:
            costo_acumulado, celda = heapq.heappop(heap)
            if celda not in self.ia.movimientos_realizados:
                return celda

            for vecino in self.ia.obtener_vecinos_celda(celda):
                if vecino not in self.ia.movimientos_realizados:
                    # Use calculate_cell_score to determine the priority of this cell
                    score = self.calculate_cell_score(vecino)
                    heapq.heappush(heap, (score, vecino))
        return None

    def calculate_cell_score(self, cell):
        # Prefer cells with more neighbors in 'seguras' and more unrevealed neighbors
        safe_neighbors = 0
        unrevealed_neighbors = 0
        for neighbor in self.ia.obtener_vecinos_celda(cell):
            if neighbor in self.ia.seguras:
                safe_neighbors += 1
            if neighbor not in self.ia.movimientos_realizados:
                unrevealed_neighbors += 1

        # Adjust the weights as necessary based on testing and the specific game dynamics
        score = (safe_neighbors * 2) + unrevealed_neighbors
        return score
    
    #def hacer_movimiento_seguro_csp(self):
          
    
    def hacer_movimiento_seguro(self, tipo_busqueda):
        """
        Devuelve una celda segura para elegir en el tablero de Buscaminas utilizando el tipo de búsqueda especificado.
        """
        if tipo_busqueda == 1:
            return self.hacer_movimiento_seguro_aleatorio()
        elif tipo_busqueda == 2:
            return self.hacer_movimiento_seguro_estrella()
        elif tipo_busqueda == 3:
            return self.hacer_movimiento_seguro_heuristicas()
        #elif tipo_busqueda == 4:
        #    return self.hacer_movimiento_seguro_csp()
        else:
            raise ValueError("tipo_busqueda no válido")

class BuscaminasIA():
    """
    Jugador del juego Buscaminas
    """
    def __init__(self, alto=8, ancho=8):
        self.alto = alto
        self.ancho = ancho
        self.movimientos_realizados = set()
        self.minas = set()
        self.seguras = set()
        self.conocimiento = []  # Aquí se guarda el conocimiento
        self.busqueda = BusquedaBuscaminas(self, self.seguras, self.movimientos_realizados, self.conocimiento, self.alto, self.ancho)


    def marcar_mina(self, celda):
        """
        Marca una celda como mina y actualiza todo el conocimiento
        para marcar esa celda como mina también.
        """
        self.minas.add(celda)
        for sentencia in self.conocimiento:
            sentencia.marcar_mina(celda)

    def marcar_segura(self, celda):
        """
        Marca una celda como segura y actualiza todo el conocimiento
        para marcar esa celda como segura también.
        """
        self.seguras.add(celda)
        for sentencia in self.conocimiento:
            sentencia.marcar_segura(celda)

    def agregar_conocimiento(self, celda, recuento):
        """
        Llamado cuando el tablero de Buscaminas nos dice, para una celda segura dada,
        cuántas celdas vecinas tienen minas en ellas.

        Esta función debe:
            1) marcar la celda como un movimiento realizado
            2) marcar la celda como segura
            3) agregar una nueva sentencia a la base de conocimiento de la IA
               basada en el valor de `celda` y `recuento`
            4) marcar cualquier celda adicional como segura o como mina
               si se puede concluir en función de la base de conocimiento de la IA
            5) agregar cualquier nueva sentencia a la base de conocimiento de la IA
               si se pueden inferir a partir del conocimiento existente
        """
        # Marcar celda como segura y agregar a movimientos_realizados
        self.marcar_segura(celda)
        self.movimientos_realizados.add(celda)

        # Crear y agregar sentencia al conocimiento
        vecinos, recuento = self.obtener_vecinos_celda(celda, recuento)
        sentencia = Sentencia(vecinos, recuento)
        self.conocimiento.append(sentencia)

        # Conclusiones
        nuevas_inferencias = []
        for s in self.conocimiento:
            if s == sentencia:
                continue
            elif s.celdas.issuperset(sentencia.celdas):
                setDiferencia = s.celdas-sentencia.celdas
                # Seguras conocidas
                if s.recuento == sentencia.recuento:
                    for seguraEncontrada in setDiferencia:
                        self.marcar_segura(seguraEncontrada)
                # Minas conocidas
                elif len(setDiferencia) == s.recuento - sentencia.recuento:
                    for minaEncontrada in setDiferencia:
                        self.marcar_mina(minaEncontrada)
                # Inferencia conocida
                else:
                    nuevas_inferencias.append(
                        Sentencia(setDiferencia, s.recuento - sentencia.recuento)
                    )
            elif sentencia.celdas.issuperset(s.celdas):
                setDiferencia = sentencia.celdas-s.celdas
                # Seguras conocidas
                if s.recuento == sentencia.recuento:
                    for seguraEncontrada in setDiferencia:
                        self.marcar_segura(seguraEncontrada)
                # Minas conocidas
                elif len(setDiferencia) == sentencia.recuento - s.recuento:
                    for minaEncontrada in setDiferencia:
                        self.marcar_mina(minaEncontrada)
                # Inferencia conocida
                else:
                    nuevas_inferencias.append(
                        Sentencia(setDiferencia, sentencia.recuento - s.recuento)
                    )

        self.conocimiento.extend(nuevas_inferencias)
        self.eliminar_duplicados()
        self.eliminar_seguras()

    def hacer_movimiento(self, tipo_busqueda):
        return self.busqueda.hacer_movimiento_seguro(tipo_busqueda)
          
            
    def hacer_movimiento_aleatorio(self):
       """
       Devuelve un movimiento para realizar en el tablero de Buscaminas.
       Debería elegir aleatoriamente entre celdas que:
           1) no hayan sido elegidas todavía, y
           2) no se sabe que son minas
    
       """
       todos_movimientos = set()
       for i in range(self.alto):
           for j in range(self.ancho):
               if (i,j) not in self.minas and (i,j) not in self.movimientos_realizados:
                   todos_movimientos.add((i,j))
       if len(todos_movimientos) == 0:
           return None
       movimiento = random.choice(tuple(todos_movimientos))
       return movimiento
               
           
    def obtener_vecinos_celda(self, celda, recuento):
        i, j = celda
        vecinos = []

        for fila in range(i-1, i+2):
            for col in range(j-1, j+2):
                if (fila >= 0 and fila < self.alto) \
                and (col >= 0 and col < self.ancho) \
                and (fila, col) != celda \
                and (fila, col) not in self.seguras \
                and (fila, col) not in self.minas:
                    vecinos.append((fila, col))
                if (fila, col) in self.minas:
                    recuento -= 1

        return vecinos, recuento

    def eliminar_duplicados(self):
        conocimiento_unico = []
        for s in self.conocimiento:
            if s not in conocimiento_unico:
                conocimiento_unico.append(s)
        self.conocimiento = conocimiento_unico

    def eliminar_seguras(self):
        conocimiento_final = []
        for s in self.conocimiento:
            conocimiento_final.append(s)
            if s.minas_conocidas():
                for minaEncontrada in s.minas_conocidas():
                    self.marcar_mina(minaEncontrada)
                conocimiento_final.pop(-1)
            elif s.seguras_conocidas():
                for seguraEncontrada in s.seguras_conocidas():
                    self.marcar_segura(seguraEncontrada)
                conocimiento_final.pop(-1)
        self.conocimiento = conocimiento_final

class Sentencia():
    """
    Declaración lógica sobre un juego de Buscaminas.
    Una sentencia consiste en un conjunto de celdas del tablero
    y un recuento del número de esas celdas que son minas.
    """

    def __init__(self, celdas, recuento):
        self.celdas = set(celdas)
        self.recuento = recuento

    def __eq__(self, other):
        return self.celdas == other.celdas and self.recuento == other.recuento

    def __str__(self):
        return f"{self.celdas} = {self.recuento}"

    def minas_conocidas(self):
        """
        Devuelve el conjunto de todas las celdas en self.celdas que se sabe que son minas.
        """
        if len(self.celdas) == self.recuento:
            return self.celdas
        return None

    def seguras_conocidas(self):
        """
        Devuelve el conjunto de todas las celdas en self.celdas que se sabe que son seguras.
        """
        if self.recuento == 0:
            return self.celdas
        return None

    def marcar_mina(self, celda):
        """
        Actualiza la representación de conocimiento interno dado el hecho de que
        una celda se sabe que es una mina.
        """
        nuevas_celdas = set()
        for item in self.celdas:
            if item != celda:
                nuevas_celdas.add(item)
            else:
                self.recuento -= 1
        self.celdas = nuevas_celdas

    def marcar_segura(self, celda):
        """
        Actualiza la representación de conocimiento interno dado el hecho de que
        una celda se sabe que es segura.
        """
        nuevas_celdas = set()
        for item in self.celdas:
            if item != celda:
                nuevas_celdas.add(item)
        self.celdas = nuevas_celdas
