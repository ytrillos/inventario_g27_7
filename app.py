from flask import *
import sqlite3
from flask_login import LoginManager
import secrets

app = Flask(__name__) 
"""
app.config['SECRET_KEY'] = 'Nj5YZutuRytwkIq7QC3YJd7p1gQrH665SDyWSdVGRnvJXJpJ-DgHjA'
login_manager = LoginManager(app)
"""

@app.route("/ind")  
def index():
    return render_template("index.html");  

@app.route("/dashboard")  
def dashboard():  
    con = sqlite3.connect("inventario.db")
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from usuarios")  
    rows = cur.fetchall()   
    return render_template("dashboard.html",rows = rows);  

@app.route("/usuario")  
def usuario():  
    return render_template("usuario.html");  

@app.route("/proveedor")  
def proveedor():  
    return render_template("proveedor.html");  

@app.route("/producto")  
def producto():  
    return render_template("producto.html");  

@app.route("/generate_key")  
def generate_key():  
    secret_key = secrets.token_urlsafe(40)
    return secret_key;  


if __name__ == "__main__":  
    app.run(debug = True)