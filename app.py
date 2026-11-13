import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(BASE_DIR, "flore.db")

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao"),
                      DATABASE=DATABASE)
    if test_config:
        app.config.update(test_config)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(error=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def init_db():
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL CHECK(price > 0),
                quantity INTEGER NOT NULL CHECK(quantity >= 0),
                minimum_quantity INTEGER NOT NULL DEFAULT 5 CHECK(minimum_quantity >= 0)
            )
        """)
        db.commit()

    with app.app_context():
        init_db()

    @app.route("/")
    def index():
        db = get_db()
        products = db.execute("SELECT * FROM products ORDER BY name").fetchall()
        low_stock = db.execute(
            "SELECT * FROM products WHERE quantity <= minimum_quantity ORDER BY name"
        ).fetchall()
        return render_template("index.html", products=products, low_stock=low_stock)

    @app.route("/produtos/novo", methods=["GET", "POST"])
    def new_product():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            category = request.form.get("category", "").strip()
            try:
                price = float(request.form.get("price", ""))
                quantity = int(request.form.get("quantity", ""))
                minimum = int(request.form.get("minimum_quantity", "5"))
            except ValueError:
                flash("Informe preço e quantidades válidos.", "error")
                return render_template("product_form.html")
            if not name or not category or price <= 0 or quantity < 0 or minimum < 0:
                flash("Confira os campos. Preço deve ser maior que zero e quantidades não podem ser negativas.", "error")
                return render_template("product_form.html")
            db = get_db()
            db.execute(
                "INSERT INTO products (name, category, price, quantity, minimum_quantity) VALUES (?, ?, ?, ?, ?)",
                (name, category, price, quantity, minimum)
            )
            db.commit()
            flash("Produto cadastrado com sucesso!", "success")
            return redirect(url_for("index"))
        return render_template("product_form.html")

    @app.route("/produtos/movimentar/<int:product_id>", methods=["POST"])
    def move_stock(product_id):
        try:
            amount = int(request.form.get("amount", ""))
        except ValueError:
            flash("Informe uma quantidade inteira válida.", "error")
            return redirect(url_for("index"))
        movement = request.form.get("movement")
        if amount <= 0 or movement not in ("entrada", "saida"):
            flash("Movimentação inválida.", "error")
            return redirect(url_for("index"))
        db = get_db()
        product = db.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if product is None:
            flash("Produto não encontrado.", "error")
        elif movement == "saida" and amount > product["quantity"]:
            flash("A saída não pode ser maior que o estoque disponível.", "error")
        else:
            delta = amount if movement == "entrada" else -amount
            db.execute("UPDATE products SET quantity = quantity + ? WHERE id = ?", (delta, product_id))
            db.commit()
            flash("Estoque atualizado com sucesso!", "success")
        return redirect(url_for("index"))

    @app.route("/produtos")
    def search_products():
        term = request.args.get("q", "").strip()
        db = get_db()
        products = db.execute(
            "SELECT * FROM products WHERE name LIKE ? OR category LIKE ? ORDER BY name",
            (f"%{term}%", f"%{term}%")
        ).fetchall()
        return render_template("index.html", products=products, low_stock=[])

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
