from db.database import create_user_table

def initialize_db():
    create_user_table()
    print("Base de datos inicializada con éxito.")

if __name__ == "__main__":
    initialize_db()
