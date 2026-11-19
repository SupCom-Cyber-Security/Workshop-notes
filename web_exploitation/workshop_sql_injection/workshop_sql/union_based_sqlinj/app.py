import os
from flask import Flask, request, render_template_string, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'ctf_secret_key_demo'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.environ.get('DB_FILE', '/tmp/shop.db')
def init_db():
    """Initialise la base de données avec deux tables : products et flags."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Table des utilisateurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Table des produits (publique)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL
        )
    """)


    # Réinitialisation des données par défaut
    cursor.execute("DELETE FROM products")

    cursor.executemany("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", [
        ('Clavier Mécanique', 'Clavier RGB switch red', 49.99),
        ('Souris Sans Fil', 'Souris ergonomique 16000 DPI', 29.99),
        ('Écran 24 pouces', 'Dalle IPS 144Hz Full HD', 149.99),
        ('Casque Audio', 'Casque surround 7.1 avec micro', 59.99)
    ])

    cursor.execute("INSERT INTO users (username, password) VALUES ('FLAG_CHALLENGE', 'SC2{un10n_b4s3d_sqli_3xp101t}')")

    conn.commit()
    conn.close()

init_db()

# --- TEMPLATES HTML ---

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"><title>Inscription</title>
    <style>
        body { margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; background: #f1f5f9; font-family: Arial; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 300px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #2563eb; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .msg { color: #ef4444; text-align: center; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="text-align:center;">Inscription</h2>
        {% if msg %}<div class="msg">{{ msg }}</div>{% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Nom d'utilisateur" required>
            <input type="password" name="password" placeholder="Mot de passe" required>
            <button type="submit">S'inscrire</button>
        </form>
        <p style="text-align:center;"><a href="/login">Déjà un compte ? Connexion</a></p>
    </div>
</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"><title>Connexion</title>
    <style>
        body { margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; background: #f1f5f9; font-family: Arial; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 300px; }
        input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #16a34a; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .msg { color: #ef4444; text-align: center; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="text-align:center;">Connexion</h2>
        {% if msg %}<div class="msg">{{ msg }}</div>{% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Nom d'utilisateur" required>
            <input type="password" name="password" placeholder="Mot de passe" required>
            <button type="submit">Se connecter</button>
        </form>
        <p style="text-align:center;"><a href="/register">Pas encore de compte ? Inscription</a></p>
    </div>
</body>
</html>
'''

PRODUCTS_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8"><title>Boutique</title>
    <style>
        body { font-family: Arial; margin: 40px; background-color: #f8fafc; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
        .search-box { margin-bottom: 30px; }
        input[type="text"] { padding: 10px; width: 300px; border: 1px solid #cbd5e1; border-radius: 5px; }
        button { padding: 10px 15px; background: #2563eb; color: white; border: none; border-radius: 5px; cursor: pointer; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background-color: #1e293b; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Bienvenue, {{ user }} !</h2>
        <a href="/logout" style="color: #ef4444; text-decoration: none; font-weight: bold;">Déconnexion</a>
    </div>

    <div class="search-box">
        <form method="GET" action="/products">
            <input type="text" name="search" placeholder="Rechercher un produit..." value="{{ search_query }}">
            <button type="submit">Rechercher</button>
        </form>
    </div>

    <h3>Catalogue des produits</h3>
    <table>
        <thead>
            <tr>
                <th>Nom du Produit</th>
                <th>Description</th>
                <th>Prix (€)</th>
            </tr>
        </thead>
        <tbody>
            {% for item in products %}
            <tr>
                <td>{{ item[0] }}</td>
                <td>{{ item[1] }}</td>
                <td>{{ item[2] }}</td>
            </tr>
            {% else %}
            <tr>
                <td colspan="3" style="text-align: center; color: #64748b;">Aucun produit trouvé.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
'''

# --- ROUTES ---

@app.route('/')
def home():
    if 'user' in session:
        return redirect('/products')
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            msg = "Nom d'utilisateur déjà pris."
            
    return render_template_string(REGISTER_TEMPLATE, msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['user'] = username
            return redirect('/products')
        else:
            msg = "Identifiants incorrects."
            
    return render_template_string(LOGIN_TEMPLATE, msg=msg)

@app.route('/products', methods=['GET'])
def products():
    if 'user' not in session:
        return redirect('/login')

    search_query = request.args.get('search', '')
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # VULNÉRABILITÉ : Concaténation directe de la recherche dans la clause WHERE
    sql = f"SELECT name, description, price FROM products WHERE name LIKE '%{search_query}%'"

    try:
        cursor.execute(sql)
        items = cursor.fetchall()
    except Exception as e:
        items = []

    conn.close()
    return render_template_string(PRODUCTS_TEMPLATE, user=session['user'], products=items, search_query=search_query)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)