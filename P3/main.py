from website import create_app
import sqlite3

DB_PATH = "foodies.sqlite3"
SCHEMA_PATH = "schema.sql"

def init_db():
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()

    conn = sqlite3.connect(DB_PATH)
    conn.executescript(schema)
    conn.close()
    print("Database initialized from schema.sql.")

#init_db()

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)