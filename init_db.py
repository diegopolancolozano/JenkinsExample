from app import app, inicializar_bd

if __name__ == '__main__':
    with app.app_context():
        inicializar_bd()
    print('Base de datos SQLite preparada.')
