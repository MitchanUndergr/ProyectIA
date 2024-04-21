import unittest
import minesweeper as ms

class TestBuscaminaAI(unittest.TestCase):

    def test_marcar_mina(self):
        sentencia = ms.Sentencia([(0,1), (0,2), (0,3)], 2)

        # Primera celda
        sentencia.marcar_mina((0,1))
        self.assertEqual({(0,2), (0,3)}, sentencia.celdas)

        # Segunda celda
        sentencia.marcar_mina((0,2))
        self.assertEqual({(0,3)}, sentencia.celdas)

        # Celda NO en la sentencia
        sentencia.marcar_mina((2,1))
        self.assertEqual({(0,3)}, sentencia.celdas)

        # Comprobar conteo de minas
        self.assertEqual(0, sentencia.recuento)

    def test_marcar_segura(self):
        sentencia = ms.Sentencia([(0,1), (0,2), (0,3)], 2)

        # Primera celda
        sentencia.marcar_segura((0,1))
        self.assertEqual({(0,2), (0,3)}, sentencia.celdas)

        # Segunda celda
        sentencia.marcar_segura((0,2))
        self.assertEqual({(0,3)}, sentencia.celdas)

        # Celda NO en la sentencia
        sentencia.marcar_segura((2,1))
        self.assertEqual({(0,3)}, sentencia.celdas)

        # Comprobar conteo de minas
        self.assertEqual(2, sentencia.recuento)

    def test_minas_conocidas(self):

        # Todas son minas
        sentencia = ms.Sentencia([(0,1), (0,2), (0,3)], 3)
        self.assertEqual({(0,1), (0,2), (0,3)}, sentencia.minas_conocidas())

        # No se sabe
        sentencia = ms.Sentencia([(0,1), (0,2), (0,3)], 2)
        self.assertIsNone(sentencia.minas_conocidas())

    def test_seguras_conocidas(self):

        # Todas son seguras
        sentencia = ms.Sentencia([(0,1), (0,2), (0,3)], 0)
        self.assertEqual({(0,1), (0,2), (0,3)}, sentencia.seguras_conocidas())

        # No se sabe
        sentencia = ms.Sentencia([(0,1), (0,2), (0,3)], 2)
        self.assertIsNone(sentencia.seguras_conocidas())

    def test_obtener_vecinos_celda(self):
        ai = ms.BuscaminasIA()

        # Vecino de arriba a la izquierda
        celda = (0,0)
        self.assertEqual(
            ai.obtener_vecinos_celda(celda, 0)[0],
            [(0,1), (1,0), (1,1)]
        )

        # Vecino de arriba a la derecha
        celda = (0,7)
        self.assertEqual(
            ai.obtener_vecinos_celda(celda, 0)[0],
            [(0,6), (1,6), (1,7)]
        )

        # Vecino de abajo a la derecha
        celda = (7,7)
        self.assertEqual(
            ai.obtener_vecinos_celda(celda, 0)[0],
            [(6,6), (6,7), (7,6)]
        )

        # Vecino de abajo a la izquierda
        celda = (7,0)
        self.assertEqual(
            ai.obtener_vecinos_celda(celda, 0)[0],
            [(6,0), (6,1), (7,1)]
        )

        # Vecino del centro
        celda = (4,4)
        self.assertEqual(
            ai.obtener_vecinos_celda(celda, 0)[0],
            [(3,3), (3,4), (3,5), (4,3), (4,5), (5,3), (5,4), (5,5)]
        )

    def test_agregar_conocimiento(self):

        # Sin minas en los vecinos
        ai = ms.BuscaminasIA()
        ai.agregar_conocimiento((7,0), 0)
        self.assertEqual(ai.conocimiento, [])

        # Todos los vecinos son minas
        ai = ms.BuscaminasIA()
        ai.agregar_conocimiento((7,7), 3)
        self.assertEqual(ai.conocimiento, [])

        # Desconocido
        ai = ms.BuscaminasIA()
        ai.agregar_conocimiento((0,0), 1)
        sentencia = ms.Sentencia([(0,1),(1,0),(1,1)], 1)
        self.assertEqual(ai.conocimiento, [sentencia])

        # Caso de ejemplo
        ai = ms.BuscaminasIA(3, 3)
        ai.agregar_conocimiento((0,0), 1)
        ai.agregar_conocimiento((0,1), 1)
        ai.agregar_conocimiento((0,2), 1)
        ai.agregar_conocimiento((2,1), 2)
        sentencia = ms.Sentencia({(2,0),(2,2)}, 1)
        self.assertEqual(ai.conocimiento, [sentencia])

    def test_realizar_movimiento_seguro(self):

        # Hay movimientos seguros
        ai = ms.BuscaminasIA(3, 3)
        ai.agregar_conocimiento((0,0), 1)
        ai.agregar_conocimiento((0,1), 1)
        ai.agregar_conocimiento((0,2), 1)
        ai.agregar_conocimiento((2,1), 2)
        self.assertIsNotNone(ai.hacer_movimiento_seguro())

        # No hay movimientos seguros
        ai = ms.BuscaminasIA()
        ai.agregar_conocimiento((7,7), 3)
        self.assertIsNone(ai.hacer_movimiento_seguro())

    def test_realizar_movimiento_aleatorio(self):

        # Cualquier movimiento
        ai = ms.BuscaminasIA(3, 3)
        ai.agregar_conocimiento((0,0), 1)
        ai.agregar_conocimiento((0,1), 1)
        ai.agregar_conocimiento((0,2), 1)
        ai.agregar_conocimiento((2,1), 2)
        movimiento = ai.hacer_movimiento_aleatorio()
        self.assertIsNotNone(movimiento)


if __name__ == "__main__":
    unittest.main()
