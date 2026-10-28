import unittest
from app import saludo

class SaludoTests(unittest.TestCase):
    def test_devuelve_saludo(self):
        self.assertEqual(saludo("Diego"), "Hola, Diego. Jenkins ejecutó esta aplicación.")

    def test_elimina_espacios(self):
        self.assertEqual(saludo("  Diego  "), saludo("Diego"))

    def test_rechaza_nombre_vacio(self):
        with self.assertRaises(ValueError):
            saludo("   ")

if __name__ == "__main__":
    unittest.main()
