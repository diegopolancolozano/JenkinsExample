import unittest
from decimal import Decimal
from app import app, es_palindromo, sumar


class LogicaTests(unittest.TestCase):
    def test_suma_enteros(self):
        self.assertEqual(sumar("2", "3"), Decimal("5"))

    def test_suma_decimales_exactos(self):
        self.assertEqual(sumar("0.1", "0.2"), Decimal("0.3"))

    def test_suma_negativos_y_espacios(self):
        self.assertEqual(sumar(" -4 ", " 2 "), Decimal("-2"))

    def test_suma_rechaza_entrada_invalida(self):
        for valor in ("", "abc", "NaN", "Infinity"):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                sumar(valor, "2")

    def test_palindromo_ignora_tildes_signos_y_mayusculas(self):
        self.assertTrue(es_palindromo("Anita lava la tina"))
        self.assertTrue(es_palindromo("¡Anita, lava la tina!"))
        self.assertTrue(es_palindromo("Ána"))

    def test_no_palindromo(self):
        self.assertFalse(es_palindromo("Jenkins"))

    def test_palindromo_vacio(self):
        for valor in ("", "  ", "!!!"):
            with self.subTest(valor=valor), self.assertRaises(ValueError):
                es_palindromo(valor)


class RutasTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_inicio_muestra_ambos_formularios(self):
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Sumar dos números", respuesta.get_data(as_text=True))
        self.assertIn("Comprobar palíndromo", respuesta.get_data(as_text=True))

    def test_suma_correcta(self):
        respuesta = self.client.post("/sumar", data={"primero": "2.5", "segundo": "3"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Resultado: 5.5", respuesta.get_data(as_text=True))

    def test_suma_invalida(self):
        respuesta = self.client.post("/sumar", data={"primero": "abc", "segundo": "3"})
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn("números válidos", respuesta.get_data(as_text=True))

    def test_suma_campos_ausentes(self):
        self.assertEqual(self.client.post("/sumar", data={}).status_code, 400)

    def test_palindromo_correcto(self):
        respuesta = self.client.post("/palindromo", data={"texto": "Anita lava la tina"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Es un palíndromo", respuesta.get_data(as_text=True))

    def test_palindromo_negativo(self):
        respuesta = self.client.post("/palindromo", data={"texto": "Jenkins"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("No es un palíndromo", respuesta.get_data(as_text=True))

    def test_palindromo_sin_contenido(self):
        respuesta = self.client.post("/palindromo", data={"texto": "!!!"})
        self.assertEqual(respuesta.status_code, 400)

    def test_metodo_incorrecto(self):
        self.assertEqual(self.client.get("/sumar").status_code, 405)
        self.assertEqual(self.client.get("/palindromo").status_code, 405)


if __name__ == "__main__":
    unittest.main()
