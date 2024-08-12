import os

DATABASE = os.path.join(os.getcwd(), 'users.db')
SECRET_KEY = os.urandom(24)
