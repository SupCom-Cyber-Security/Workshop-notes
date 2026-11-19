import os
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# Utilise le dossier réinscriptible /data/ dédié dans le container
DB_FILE = os.environ.get('DB_FILE', '/data/database.db')

def init_db():
    """Initialise la base de données SQLite dans /data."""
    db_dir = os.path.dirname(DB_FILE)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'p@ssw0rd_sup3r_secur3_12345')")
    conn.commit()
    conn.close()

init_db()

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTF Challenge</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f1f5f9;
            font-family: Arial, sans-serif;
        }
        .login-card {
            background: white;
            padding: 35px 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            width: 340px;
        }
        .login-card h2 {
            margin-top: 0;
            text-align: center;
            color: #1e293b;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 0.85rem;
            color: #64748b;
            margin-bottom: 20px;
        }
        .error {
            color: #ef4444;
            background: #fee2e2;
            padding: 10px;
            border-radius: 6px;
            font-size: 0.9rem;
            text-align: center;
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: bold;
            color: #475569;
            font-size: 0.9rem;
        }
        input {
            width: 100%;
            padding: 10px;
            margin-bottom: 18px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            box-sizing: border-box;
            font-size: 1rem;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background-color: #1d4ed8;
        }
    </style>
    <script>
        function verifwaf(event) {
            const usernameInput = document.getElementById('username').value;
            const passwordInput = document.getElementById('password').value;
            
            const blacklist = ["'", '"', "OR", "or", "=", "--", "SELECT", "UNION", "#"];
            
            for (let item of blacklist) {
                if (usernameInput.includes(item) || passwordInput.includes(item)) {
                    alert("⚠️ WAF Bloqué : Caractère ou mot-clé interdit détecté ('" + item + "') !");
                    event.preventDefault();
                    return false;
                }
            }
            return true;
        }
    </script>
</head>
<body>
    <div class="login-card">
        <h2>Connexion Securisée</h2>
        
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        <form method="POST" onsubmit="return verifwaf(event)">
            <label for="username">Nom d'utilisateur :</label>
            <input type="text" id="username" name="username" required autocomplete="off">
            
            <label for="password">Mot de passe :</label>
            <input type="password" id="password" name="password">
            
            <button type="submit">Se connecter</button>
        </form>
    </div>
</body>
</html>
'''

FLAG_TEMPLATE = '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flag CTF</title>
    <style>
        body {
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0f172a;
            font-family: Arial, sans-serif;
        }
        .flag-box {
            text-align: center;
            background-color: #1e293b;
            padding: 50px 70px;
            border-radius: 16px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            border: 1px solid #334155;
        }
        h1 {
            color: #4ade80;
            margin-top: 0;
            margin-bottom: 25px;
            font-size: 2rem;
        }
        code {
            font-size: 1.6rem;
            background: #0f172a;
            color: #38bdf8;
            padding: 14px 24px;
            border-radius: 8px;
            display: inline-block;
            border: 1px solid #0284c7;
            letter-spacing: 1px;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="flag-box">
        <h1>Connexion Réussie !</h1>
        <code>SC2{cl13nt_s1d3_w4f_1s_n0t_s3cur3}</code>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()

            if user:
                return render_template_string(FLAG_TEMPLATE)
            else:
                error = "Identifiants incorrects."
        except Exception:
            conn.close()
            error = "Erreur SQL dans la requête."

    return render_template_string(LOGIN_TEMPLATE, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=False)