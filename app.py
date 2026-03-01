from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Fução cria conexão com banco...
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Cria tabela...
def create_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           descricao TEXT NOT NULL,
           concluida INTEGER DEFAULT 0         
        
        )

    """)
    conn.commit()
    conn.close()
# Read
@app.route("/")
def home():
    conn = get_db_connection()
    tarefas = conn.execute("SELECT * FROM tarefas"). fetchall()

    pendentes = conn.execute(
        "SELECT COUNT(*) FROM tarefas WHERE concluida = 0"
    ).fetchone()[0]

    concluidas = conn.execute(
        "SELECT COUNT(*) FROM tarefas WHERE concluida = 1"
    ).fetchone()[0]

    conn.close()

    return render_template("index.html",tarefas=tarefas, pendentes=pendentes,concluidas=concluidas)

# Create
@app.route("/add", methods=["POST"])
def add():
    descricao = request.form["descricao"]

    conn = get_db_connection()
    conn.execute("INSERT INTO tarefas (descricao) VALUES (?)", (descricao,))
    conn.commit()
    conn.close()

    return redirect("/")

# Delete
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# Update
@app.route("/update/<int:id>")
def update(id):
    conn = get_db_connection()
    conn.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

# Executa
if __name__=="__main__":
    create_table()
    app.run(debug=True)