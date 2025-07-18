# db/create_tables.py
from .db import engine, init_db

if __name__ == "__main__":
    init_db()
    print("Tables created")
