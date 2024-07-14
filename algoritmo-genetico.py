import random


class Buscaminas:
    def __init__(self, ancho, alto, minas):
        self.ancho = ancho
        self.alto = alto
        self.minas = minas
        self.tablero = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.revelado = [[False for _ in range(ancho)] for _ in range(alto)]
        self.colocar_minas()
        self.calcular_numeros()

    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.minas:
            x, y = random.randint(0, self.ancho - 1), random.randint(0, self.alto - 1)
            if self.tablero[y][x] != -1:
                self.tablero[y][x] = -1
                minas_colocadas += 1

    def calcular_numeros(self):
        for y in range(self.alto):
            for x in range(self.ancho):
                if self.tablero[y][x] == -1:
                    continue
                self.tablero[y][x] = sum(
                    1
                    for dx in [-1, 0, 1]
                    for dy in [-1, 0, 1]
                    if 0 <= x + dx < self.ancho
                    and 0 <= y + dy < self.alto
                    and self.tablero[y + dy][x + dx] == -1
                )

    def revelar(self, x, y):
        if not (0 <= x < self.ancho and 0 <= y < self.alto) or self.revelado[y][x]:
            return False
        self.revelado[y][x] = True
        return self.tablero[y][x] != -1

    def esta_resuelto(self):
        return all(
            self.revelado[y][x] or self.tablero[y][x] == -1
            for y in range(self.alto)
            for x in range(self.ancho)
        )

    def imprimir(self):
        for y in range(self.alto):
            for x in range(self.ancho):
                if self.revelado[y][x]:
                    print(
                        self.tablero[y][x] if self.tablero[y][x] != -1 else "X", end=" "
                    )
                else:
                    print(".", end=" ")
            print()


class AgenteGenetico:
    def __init__(
        self,
        ancho,
        alto,
        tam_poblacion=100,
        generaciones=200,
        tasa_mutacion=0.1,
        tasa_elitismo=0.1,
    ):
        self.ancho = ancho
        self.alto = alto
        self.tam_poblacion = tam_poblacion
        self.generaciones = generaciones
        self.tasa_mutacion = tasa_mutacion
        self.tasa_elitismo = tasa_elitismo

    def generar_individuo(self):
        esquinas = [
            (0, 0),
            (0, self.alto - 1),
            (self.ancho - 1, 0),
            (self.ancho - 1, self.alto - 1),
        ]
        centro = [(self.ancho // 2, self.alto // 2)]
        resto = [
            (x, y)
            for y in range(self.alto)
            for x in range(self.ancho)
            if (x, y) not in esquinas and (x, y) not in centro
        ]
        random.shuffle(resto)
        return esquinas + centro + resto

    def fitness(self, individuo, juego):
        juego_copia = Buscaminas(juego.ancho, juego.alto, juego.minas)
        juego_copia.tablero = [fila[:] for fila in juego.tablero]
        juego_copia.revelado = [fila[:] for fila in juego.revelado]

        puntuacion = 0
        for x, y in individuo:
            if juego_copia.revelar(x, y):
                if juego_copia.tablero[y][x] == 0:
                    puntuacion += 1
                else:
                    puntuacion += 2  # Dar más peso a celdas con números
            else:
                break
        return puntuacion

    def seleccion(self, poblacion, fitness):
        total_fitness = sum(fitness)
        if total_fitness == 0:
            return random.sample(poblacion, 2)
        return random.choices(poblacion, weights=fitness, k=2)

    def cruce(self, padre1, padre2):
        punto1, punto2 = sorted(random.sample(range(len(padre1)), 2))
        hijo = padre1[:punto1] + padre2[punto1:punto2] + padre1[punto2:]
        return hijo

    def mutacion(self, individuo):
        if random.random() < self.tasa_mutacion:
            i = random.randint(0, len(individuo) - 2)
            individuo[i], individuo[i + 1] = individuo[i + 1], individuo[i]
        return individuo

    def resolver(self, juego):
        poblacion = [self.generar_individuo() for _ in range(self.tam_poblacion)]

        for _ in range(self.generaciones):
            fitness = [self.fitness(ind, juego) for ind in poblacion]
            poblacion_ordenada = sorted(zip(fitness, poblacion), reverse=True)

            elite_size = int(self.tam_poblacion * self.tasa_elitismo)
            elite = [ind for _, ind in poblacion_ordenada[:elite_size]]

            if fitness[0] == juego.ancho * juego.alto - juego.minas:
                return poblacion_ordenada[0][1]

            nueva_poblacion = elite
            while len(nueva_poblacion) < self.tam_poblacion:
                padres = self.seleccion(poblacion, fitness)
                hijo = self.cruce(*padres)
                hijo = self.mutacion(hijo)
                nueva_poblacion.append(hijo)

            poblacion = nueva_poblacion

        return max(poblacion, key=lambda ind: self.fitness(ind, juego))


def calcular_porcentaje_victorias(dificultad, intentos):
    config = {"fácil": (4, 4, 5), "medio": (8, 8, 10), "difícil": (16, 16, 40)}

    if dificultad not in config:
        raise ValueError("Dificultad no reconocida")

    ancho, alto, minas = config[dificultad]
    victorias = 0

    for _ in range(intentos):
        juego = Buscaminas(ancho, alto, minas)
        agente = AgenteGenetico(ancho, alto)
        solucion = agente.resolver(juego)

        if solucion:
            celdas_reveladas = sum(1 for x, y in solucion if juego.tablero[y][x] != -1)
            if celdas_reveladas == ancho * alto - minas:
                victorias += 1

    return (victorias / intentos) * 100


# Ejecutar 25 intentos para cada dificultad ajustada y calcular el porcentaje de victorias
intentos = 25
dificultades = ["fácil", "medio", "difícil"]
porcentajes_victorias = {
    dificultad: calcular_porcentaje_victorias(dificultad, intentos)
    for dificultad in dificultades
}

# Imprimir los resultados
for dificultad, porcentaje in porcentajes_victorias.items():
    print(f"Dificultad {dificultad.capitalize()}: {porcentaje}% de victorias")
