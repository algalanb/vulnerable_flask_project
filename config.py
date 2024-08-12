import os

DATABASE = os.path.join(os.getcwd(), 'users.db')
SECRET_KEY = 'supersecretkey'  # Vulnerabilidad: Clave secreta expuesta

