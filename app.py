from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pizzaria.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



@app.route('/')
def home():
    return render_template('home.html')



@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')



@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')



@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')



@app.route('/admin')
def admin():
    return render_template('admin.html')
    



if __name__ == '__main__':
    app.run(debug=True)