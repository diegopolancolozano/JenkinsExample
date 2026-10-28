import tempfile
import unittest
from pathlib import Path
from app import app, conexion, inicializar_bd, validar_producto


class TiendaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        app.config.update(TESTING=True, DATABASE=str(Path(self.temp.name) / 'prueba.db'))
        with app.app_context():
            inicializar_bd()
        self.client = app.test_client()

    def tearDown(self):
        self.temp.cleanup()

    def test_inicio_vacio(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Aún no hay productos', response.get_data(as_text=True))

    def test_agregar_y_listar(self):
        response = self.client.post('/productos', data={'nombre': 'Camiseta', 'precio': '12.50'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Camiseta', response.get_data(as_text=True))
        self.assertIn('12.50', response.get_data(as_text=True))

    def test_guarda_centavos_exactos(self):
        self.client.post('/productos', data={'nombre': 'Lapiz', 'precio': '0.10'})
        with app.app_context():
            self.assertEqual(conexion().execute('SELECT precio_centavos FROM productos').fetchone()[0], 10)

    def test_datos_persisten_en_otra_conexion(self):
        self.client.post('/productos', data={'nombre': 'Libro', 'precio': '10'})
        with app.app_context():
            self.assertEqual(conexion().execute('SELECT nombre FROM productos').fetchone()[0], 'Libro')

    def test_inicializacion_no_borra_productos(self):
        self.client.post('/productos', data={'nombre': 'Libro', 'precio': '10'})
        with app.app_context():
            inicializar_bd()
            self.assertEqual(conexion().execute('SELECT count(*) FROM productos').fetchone()[0], 1)

    def test_nombre_vacio(self):
        response = self.client.post('/productos', data={'nombre': '  ', 'precio': '5'})
        self.assertEqual(response.status_code, 400)

    def test_precio_invalido(self):
        for precio in ('', 'abc', '0', '-1', 'NaN', 'Infinity', '1.234', '10000000'):
            with self.subTest(precio=precio):
                response = self.client.post('/productos', data={'nombre': 'Libro', 'precio': precio})
                self.assertEqual(response.status_code, 400)
        with app.app_context():
            self.assertEqual(conexion().execute('SELECT count(*) FROM productos').fetchone()[0], 0)

    def test_recorta_nombre(self):
        self.assertEqual(validar_producto('  Libro  ', '1.20'), ('Libro', 120))

    def test_nombre_muy_largo(self):
        self.assertEqual(self.client.post('/productos', data={'nombre': 'x' * 101, 'precio': '2'}).status_code, 400)

    def test_escapa_html_en_producto(self):
        response = self.client.post('/productos', data={'nombre': '<script>', 'precio': '2'}, follow_redirects=True)
        self.assertIn('&lt;script&gt;', response.get_data(as_text=True))
        self.assertNotIn('<script>', response.get_data(as_text=True))

    def test_metodo_incorrecto(self):
        self.assertEqual(self.client.get('/productos').status_code, 405)


if __name__ == '__main__':
    unittest.main()
