# ai_test_runner.py
from buscaminas import Buscaminas, BuscaminasIA

def initialize_game(ALTO, ANCHO, MINAS):
    juego = Buscaminas(alto=ALTO, ancho=ANCHO, minas=MINAS)
    ia = BuscaminasIA(alto=ALTO, ancho=ANCHO)
    return juego, ia

def play_game_automatically(juego, ia):
    perdido = False
    while not juego.juego_terminado():
        move = ia.decide_next_move()
        if move is None:
            perdido = True
            break
        juego.realizar_movimiento(move)
        if juego.es_mina(move):
            perdido = True
            break
    return not perdido

def run_tests(ALTO, ANCHO, MINAS, num_tests=100):
    wins = 0
    for _ in range(num_tests):
        juego, ia = initialize_game(ALTO, ANCHO, MINAS)
        if play_game_automatically(juego, ia):
            wins += 1
    win_rate = wins / num_tests
    print(f"Win rate: {win_rate * 100}%")

if __name__ == "__main__":
    ALTO, ANCHO, MINAS = 10, 10, 20  # Example dimensions and mine count
    run_tests(ALTO, ANCHO, MINAS)